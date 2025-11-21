# Data Consolidation Scripts

This directory contains scripts for consolidating and processing the EVAonline validation datasets.

## Available Scripts

### `consolidate_all_data.py`

Merges data from Xavier, NASA POWER, and Open-Meteo sources for all 17 cities into a single consolidated CSV file.

**Input files:**
- `data/nasa_power_raw/*_1991-01-01_2020-12-31_NASA_RAW.csv` - NASA POWER MERRA-2 data (1991-2020)
- `data/open_meteo_raw/*_1991-01-01_2020-12-31_OpenMeteo_RAW.csv` - Open-Meteo ERA5-Land data (1991-2020)
- `data/eto_xavier/*.csv` - Xavier et al. reference dataset (1961-2024)
- `data/eto_open_meteo/*_OpenMeteo_ETo.csv` - Open-Meteo ERA5-Land data (1991-2020)
- `data/eto_evaonline_fused/*_ETo_EVAonline.csv` - EVAonline adaptive Kalman fusion (1991-2020)

**Output:**
- `all_cities_daily_eto_1994_2024.csv` - Consolidated dataset

**Output format:**
```csv
date,city,eto_xavier,eto_nasa,eto_openmeteo,eto_evaonline
1994-01-01,Alvorada do Gurguéia,4.606299,4.123,4.92,4.648
```

**Usage:**
```bash
cd EVAonline_validation_v1.0.0
python scripts/consolidate_all_data.py
```

**Time:** ~30-60 seconds depending on system

**Notes:**
- Xavier data is used as the baseline (most complete temporal coverage)
- NASA POWER ETo is calculated using simplified Hargreaves-Samani approximation
- Open-Meteo provides native FAO-56 ETo calculations
- EVAonline data comes from adaptive Kalman fusion of NASA POWER and Open-Meteo
- Common period: 1994-2024 (Xavier starts earlier, others start 1991)
- All 17 cities are consolidated into a single file for easy analysis

---

### `generate_data_manifest.py`

Generates a CSV manifest with MD5 checksums for all data files.

**Output:**
- `data_manifest.csv` - Complete file listing with checksums

**Usage:**
```bash
python scripts/generate_data_manifest.py
```

---

## City Name Mapping

All datasets use consistent city naming:

| File Name | Display Name |
|-----------|--------------|
| `Alvorada_do_Gurgueia_PI` | Alvorada do Gurguéia |
| `Araguaina_TO` | Araguaína |
| `Balsas_MA` | Balsas |
| `Barreiras_BA` | Barreiras |
| `Bom_Jesus_PI` | Bom Jesus |
| `Campos_Lindos_TO` | Campos Lindos |
| `Carolina_MA` | Carolina |
| `Corrente_PI` | Corrente |
| `Formosa_do_Rio_Preto_BA` | Formosa do Rio Preto |
| `Imperatriz_MA` | Imperatriz |
| `Luiz_Eduardo_Magalhaes_BA` | Luiz Eduardo Magalhães |
| `Pedro_Afonso_TO` | Pedro Afonso |
| `Piracicaba_SP` | Piracicaba |
| `Porto_Nacional_TO` | Porto Nacional |
| `Sao_Desiderio_BA` | São Desidério |
| `Tasso_Fragoso_MA` | Tasso Fragoso |
| `Urucui_PI` | Uruçuí |

---

## Data Quality Notes

- **Xavier**: Reference dataset, 0.25° resolution, 3,625+ stations
- **NASA POWER**: MERRA-2 reanalysis, 0.5° resolution, global coverage
- **Open-Meteo**: ERA5-Land reanalysis, ~9 km resolution, native FAO-56 ETo
- **EVAonline**: Kalman fusion with bias correction and noise filtering

See main README.md for detailed methodology and data source documentation.
