# validate_evaonline_vs_xavier.py
import pandas as pd
import numpy as np
from scipy.stats import linregress
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
from pathlib import Path

# ================== CONFIGURAÇÃO ==================
xavier_folder = Path(
    "validation/data_validation/data/csv/BRASIL/ETo/"
)  # CSVs do Xavier (1991-2024)
temp = Path("temp")  # Seus CSVs com et0_mm
output_folder = Path("validation/final_results")
output_folder.mkdir(exist_ok=True)

# Suas cidades
cities = [
    "Alvorada_do_Gurgueia_PI",
    # "Araguaina_TO",
    # "Balsas_MA",
    # "Barreiras_BA",
    # "Bom_Jesus_PI",
    # "Campos_Lindos_TO",
    # "Carolina_MA",
    # "Corrente_PI",
    # "Formosa_do_Rio_Preto_BA",
    # "Imperatriz_MA",
    # "Luiz_Eduardo_Magalhaes_BA",
    # "Pedro_Afonso_TO",
    # "Piracicaba_SP",
    # "Porto_Nacional_TO",
    # "Sao_Desiderio_BA",
    # "Tasso_Fragoso_MA",
    # "Urucui_PI",
]

results = []

for city in cities:
    print(f"\n{'='*60}")
    print(f"VALIDANDO: {city}")

    # 1. Lê Xavier
    xavier_csv = xavier_folder / "Alvorada_do_Gurgueia_PI.csv"
    if not xavier_csv.exists():
        print(f"   Arquivo Xavier não encontrado: {xavier_csv.name}")
        continue
    df_x = pd.read_csv(xavier_csv, parse_dates=["Data"])
    df_x = df_x.set_index("Data")["ETo"]

    # 2. Lê seu ETo
    eva_csv = (
        temp / "df_eto_calculado_completo_1_ano.csv"
    )  # ajuste se o nome for diferente
    if not eva_csv.exists():
        print(f"   Seu arquivo não encontrado: {eva_csv.name}")
        continue

    df_eva = pd.read_csv(eva_csv)
    df_eva.columns = [
        "idx",
        "date",
        "T2M_MAX",
        "T2M_MIN",
        "T2M",
        "RH2M",
        "WS2M",
        "ALLSKY_SFC_SW_DWN",
        "PRECTOTCORR",
        "et0_mm",
    ]
    df_eva = df_eva.drop(columns=["idx"])
    df_eva["date"] = pd.to_datetime(df_eva["date"])
    df_eva = df_eva.set_index("date")["et0_mm"]

    # 3. Junta (período comum)
    df = pd.concat([df_eva, df_x], axis=1, join="inner").dropna()
    if len(df) < 350:
        print(f"   Poucos dias válidos: {len(df)}")
        continue

    # ================== MÉTRICAS ==================
    mae = mean_absolute_error(df["et0_mm"], df["eto_xavier"])
    rmse = np.sqrt(mean_squared_error(df["et0_mm"], df["eto_xavier"]))
    bias = df["et0_mm"].mean() - df["eto_xavier"].mean()
    r2 = linregress(df["et0_mm"], df["eto_xavier"]).rvalue ** 2

    # KGE (Kling-Gupta Efficiency) - padrão em hidrologia
    r = np.corrcoef(df["et0_mm"], df["eto_xavier"])[0, 1]
    alpha = df["et0_mm"].std() / df["eto_xavier"].std()
    beta = df["et0_mm"].mean() / df["eto_xavier"].mean()
    kge = 1 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)

    # NSE (Nash-Sutcliffe)
    nse = 1 - np.sum((df["et0_mm"] - df["eto_xavier"]) ** 2) / np.sum(
        (df["eto_xavier"] - df["eto_xavier"].mean()) ** 2
    )

    # PBIAS (%)
    pbias = (
        100
        * (df["et0_mm"].sum() - df["eto_xavier"].sum())
        / df["eto_xavier"].sum()
    )

    print(
        f"   Dias: {len(df)} | MAE: {mae:.3f} | RMSE: {rmse:.3f} | R²: {r2:.3f}"
    )
    print(
        f"   KGE: {kge:.3f} | NSE: {nse:.3f} | Bias: {bias:+.3f} | PBIAS: {pbias:+.2f}%"
    )

    results.append(
        {
            "city": city,
            "days": len(df),
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
            "KGE": kge,
            "NSE": nse,
            "Bias": bias,
            "PBIAS_%": pbias,
        }
    )

    # Gráfico
    plt.figure(figsize=(8, 7))
    plt.scatter(
        df["eto_xavier"], df["et0_mm"], alpha=0.7, s=20, color="#2E86AB"
    )
    lims = [df.min().min() - 0.5, df.max().max() + 0.5]
    plt.plot(lims, lims, "r--", lw=2, label="1:1")
    plt.xlabel("ETo Xavier et al. (mm/dia)", fontsize=12)
    plt.ylabel("ETo EVAonline (mm/dia)", fontsize=12)
    plt.title(
        f"{city} — 1991\nR² = {r2:.3f} | MAE = {mae:.3f} mm/dia | KGE = {kge:.3f}",
        fontsize=14,
    )
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(
        output_folder / f"{city}_1991_validation.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()

# ================== RESUMO FINAL ==================
df_results = pd.DataFrame(results)
df_results = df_results.round(3)

print("\n" + "=" * 80)
print("VALIDAÇÃO FINAL EVAonline vs Xavier et al. (BR-DWGD) — 1991")
print("=" * 80)
print(
    df_results[["city", "MAE", "R2", "KGE", "NSE", "Bias"]].to_string(
        index=False
    )
)

print(f"\nMÉDIAS FINAIS (17 cidades):")
print(f"   MAE    = {df_results['MAE'].mean():.3f} mm/dia")
print(f"   R²     = {df_results['R2'].mean():.3f}")
print(f"   KGE    = {df_results['KGE'].mean():.3f}")
print(f"   NSE    = {df_results['NSE'].mean():.3f}")
print(f"   Bias   = {df_results['Bias'].mean():+.3f} mm/dia")

# Salvar tudo
df_results.to_csv(output_folder / "validation_summary_1991.csv", index=False)
df_results[["city", "MAE", "R2", "KGE", "NSE", "Bias"]].to_latex(
    output_folder / "validation_table.tex", index=False, float_format="%.3f"
)

print(f"\nResultados salvos em: {output_folder.resolve()}")
print("Tabela LaTeX pronta para SoftwareX!")
