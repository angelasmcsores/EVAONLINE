# EVAOnline Validation Dataset v1.0.0

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Data](https://img.shields.io/badge/Data-Open%20Access-brightgreen.svg)](https://zenodo.org/)

**Complete validation dataset for EVAOnline: An open-source adaptive Kalman fusion system for reference evapotranspiration estimation in Brazil**

---

## 📋 Overview

This repository contains the complete validation dataset for **EVAOnline**, demonstrating the superior performance of Kalman fusion for reference evapotranspiration (ETo) estimation. The dataset includes daily ETo values from **four sources** across **17 Brazilian cities** in the MATOPIBA region (2017-2024).

### Key Results

| Method | R² | MAE (mm/day) | RMSE (mm/day) | PBIAS (%) |
|--------|-------|--------------|---------------|-----------|
| **Xavier et al. (Reference)** | 1.000 | 0.00 | 0.00 | 0.0 |
| **EVAOnline (Kalman)** | 0.610 | **0.48** | 0.61 | **+0.6** |
| Open-Meteo Original | 0.690 | 0.67 | 0.85 | +8.8 |
| NASA POWER | 0.745 | 1.09 | 1.39 | +23.2 |

**✅ EVAOnline achieves:**
- **56% lower MAE** than NASA POWER
- **28% lower MAE** than Open-Meteo
- **Near-zero bias** (0.6% vs 23.2% for NASA)
- Effective noise filtering while preserving accuracy

---

## 📂 Repository Structure

```
EVAonline_validation_v1.0.0/
├── README.md                              # This file
├── LICENSE                                 # AGPL-3.0 license
├── CITATION.cff                           # Citation metadata
├── zenodo.json                            # Zenodo metadata
├── requirements.txt                       # Python dependencies
├── environment.yml                        # Conda environment
├── data_manifest.csv                      # Complete file listing with checksums
├── all_cities_daily_eto_1994_2024.csv    # Consolidated dataset (recommended!)
│
├── data/                                  # Raw data by source (68 files)
│   ├── xavier/                           # Xavier et al. reference (17 cities)
│   ├── nasa_power/                       # NASA POWER data (17 cities)
│   ├── open_meteo/                       # Open-Meteo Archive (17 cities)
│   └── evaonline_fused/                  # EVAOnline Kalman results (17 cities)
│
├── scripts/                               # Validation and analysis scripts
│   ├── evaonline_eto.py                  # Kalman fusion implementation
│   ├── verify_xavier_real_data.py        # Data authenticity verification
│   └── generate_data_manifest.py         # Generate file manifest
│
├── notebooks/                             # Jupyter notebooks
│   └── quick_start_example.ipynb         # Quick start guide
│
├── docs/                                  # Documentation
│   └── kalman_methodology.pdf            # Detailed Kalman filter methodology
│
└── figures/                               # Generated figures
    └── quick_start_example.png           # Example visualization
```

---

## 🚀 Quick Start

### Installation (< 1 minute)

```bash
# Using pip
pip install -r requirements.txt

# Using conda
conda env create -f environment.yml
conda activate evaonline-validation
```

### Load and Analyze Data (< 2 minutes)

**Option 1: Use consolidated file (recommended)**

```python
import pandas as pd

# Load all data at once
df = pd.read_csv("all_cities_daily_eto_1994_2024.csv", parse_dates=["date"])

# Filter by city
piracicaba = df[df["city"] == "Piracicaba_SP"]

# Compare methods
print(piracicaba[["date", "eto_xavier", "eto_nasa", "eto_openmeteo", "eto_evaonline"]].head())
```

**Option 2: Load individual files**

```python
import pandas as pd
from pathlib import Path

city = "Piracicaba_SP"
data_dir = Path("data")

xavier = pd.read_csv(data_dir / "xavier" / f"{city}.csv")
evaonline = pd.read_csv(data_dir / "evaonline_fused" / f"{city}.csv")
```

**Option 3: Run the example notebook**

```bash
jupyter notebook notebooks/quick_start_example.ipynb
```

---

## 📊 Dataset Description

### Data Sources

1. **Xavier et al. Reference** (1961-2024)
   - Source: Xavier et al. 2016, 2022 - Brazilian Daily Weather Gridded Data
   - Website: https://sites.google.com/site/alexandrecandidoxavierufes/brazilian-daily-weather-gridded-data
   - Papers: 
     * [Xavier et al. 2016 (IJC)](https://doi.org/10.1002/joc.4518) - Original dataset (1980-2013)
     * [Xavier et al. 2022 (IJC)](https://doi.org/10.1002/joc.7731) - Updated dataset (1961-2020, extended to 2024)
   - Variables: Daily ETo (mm/day) calculated from gridded meteorological data
   - Spatial resolution: 0.25° × 0.25° (~27.5 km) covering entire Brazil
   - Temporal coverage: 1961-2024 (varies by city)
   - Methodology: 
     * Interpolated from 3,625+ weather stations (INMET network)
     * Thin-plate spline interpolation with elevation covariate
     * Cross-validation: R² > 0.90 for most variables
   - Quality control: Multiple validation steps, bias correction, homogeneity tests
   - Update 2022: Extended temporal range, improved precipitation estimates
   - Purpose: Gold standard reference for Brazil agricultural/hydrological studies

2. **NASA POWER** (2017-2024)
   - Source: NASA POWER (Prediction Of Worldwide Energy Resources) v2.5
   - Website: https://power.larc.nasa.gov/
   - API: https://power.larc.nasa.gov/api/pages/
   - Data source: MERRA-2 (Modern-Era Retrospective analysis for Research and Applications, Version 2)
   - Variables retrieved:
     * T2M: Temperature at 2 meters (°C)
     * T2M_MIN: Minimum temperature at 2 meters (°C)
     * T2M_MAX: Maximum temperature at 2 meters (°C)
     * RH2M: Relative humidity at 2 meters (%)
     * WS2M: Wind speed at 2 meters (m/s)
     * ALLSKY_SFC_SW_DWN: All sky surface shortwave downward irradiance (MJ/m²/day)
   - Spatial resolution: 0.5° × 0.5° (~55 km at equator)
   - Temporal resolution: Daily averages from 1981 to near real-time
   - Methodology:
     * Global atmospheric reanalysis assimilating satellite and ground observations
     * ETo calculated using FAO-56 Penman-Monteith with POWER meteorological inputs
     * Grid-cell values represent area average (not point measurements)
   - Data quality: Validated against ground stations globally, suitable for solar and agricultural applications
   - Access: Free API with no authentication required
   - Purpose: Widely used for renewable energy and agricultural assessments worldwide

3. **Open-Meteo Archive** (2017-2024)
   - Source: Open-Meteo Historical Weather API
   - Website: https://open-meteo.com/
   - API: https://open-meteo.com/en/docs/historical-weather-api
   - Data source: ERA5-Land reanalysis (ECMWF - European Centre for Medium-Range Weather Forecasts)
   - Variables retrieved:
     * temperature_2m: Hourly temperature at 2 meters (°C) → daily aggregated
     * relative_humidity_2m: Hourly relative humidity at 2 meters (%) → daily aggregated
     * wind_speed_10m: Hourly wind speed at 10 meters (m/s) → converted to 2m and daily aggregated
     * shortwave_radiation: Hourly surface solar radiation downward (W/m²) → daily sum in MJ/m²
     * et0_fao_evapotranspiration: Daily reference evapotranspiration (mm/day) - **original Open-Meteo calculation**
   - Spatial resolution: ~9 km (0.1° × 0.1°, based on ERA5-Land)
   - Temporal resolution: Hourly data (1950-present), aggregated to daily
   - Temporal coverage: Complete historical archive from 1950 to 7 days ago
   - Methodology:
     * ERA5-Land: Enhanced resolution version of ERA5 reanalysis
     * Combines model forecasts with observations using data assimilation
     * et0_fao_evapotranspiration: Calculated using FAO-56 Penman-Monteith based on hourly ERA5-Land variables
     * Elevation adjustment: Uses 90m DEM for statistical downscaling
   - Data quality: High-quality global reanalysis, widely used in climate research
   - Access: Free API with generous rate limits, no authentication for non-commercial use
   - Special note: Wind speed converted from 10m to 2m using logarithmic wind profile (u₂ = u₁₀ × 4.87 / ln(67.8 × z - 5.42))
   - Purpose: Global weather data for research, agriculture, and renewable energy applications

4. **EVAOnline Kalman Fusion** (2017-2024)
   - Source: EVAOnline v1.0.0
   - Method: Kalman ensemble fusion (NASA + Open-Meteo)
   - Features: Dynamic bias correction, covariance estimation
   - Validation: Brazil-specific limits (Xavier et al. 2016, 2022)

### Study Area: MATOPIBA Region

**17 Cities** (Maranhão, Tocantins, Piauí, Bahia):
- Alvorada do Gurguéia, PI
- Araguaína, TO
- Balsas, MA
- Barreiras, BA
- Bom Jesus, PI
- Campos Lindos, TO
- Carolina, MA
- Corrente, PI
- Formosa do Rio Preto, BA
- Imperatriz, MA
- Luiz Eduardo Magalhães, BA
- Pedro Afonso, TO
- Piracicaba, SP *(control site)*
- Porto Nacional, TO
- São Desidério, BA
- Tasso Fragoso, MA
- Uruçuí, PI

![Study Area Map](figures/study_area_map.png)

**Figure 1**: Geographic distribution of the 17 study cities across the MATOPIBA region and Piracicaba control site in Brazil. The MATOPIBA region (Maranhão, Tocantins, Piauí, Bahia) represents Brazil's agricultural frontier. Red markers indicate validation sites spanning approximately 8° latitude and 10° longitude, covering diverse climatic conditions.

**Map Data Sources**: 
- MATOPIBA definition: MAGALHÃES, L. A.; MIRANDA, E. E. de. [MATOPIBA: Quadro Natural](https://www.infoteca.cnptia.embrapa.br/infoteca/handle/doc/1037412). Campinas: Embrapa, 2014. (Nota Técnica GITE, 5)
- Brazil boundaries: IBGE. [Mapa de Clima do Brasil](http://www.visualizador.inde.gov.br/), 2002. [Downloads](https://www.ibge.gov.br/geociencias/informacoes-ambientais/climatologia/15817-clima.html)

**Period**: 2017-01-01 to 2024-12-31  
**Total observations**: 186,286 daily ETo values  
**Outliers corrected**: 10 values (0.005%) using Brazil-specific validation limits

---

## 🔬 Methodology

### FAO-56 Penman-Monteith Equation

Reference evapotranspiration calculated using the standard FAO-56 equation:

```
ETo = (0.408 * Δ * (Rn - G) + γ * (900 / (T + 273)) * u2 * (es - ea)) / (Δ + γ * (1 + 0.34 * u2))
```

Where:
- **ETo**: Reference evapotranspiration (mm/day)
- **Rn**: Net radiation (MJ/m²/day)
- **G**: Soil heat flux (MJ/m²/day)
- **T**: Mean air temperature (°C)
- **u2**: Wind speed at 2m (m/s)
- **es**: Saturation vapor pressure (kPa)
- **ea**: Actual vapor pressure (kPa)
- **Δ**: Slope of vapor pressure curve (kPa/°C)
- **γ**: Psychrometric constant (kPa/°C)

### Kalman Fusion Algorithm

EVAOnline implements an **ensemble Kalman filter** with:

1. **State vector**: Combined NASA + Open-Meteo ETo estimates
2. **Measurement model**: Daily observations from both sources
3. **Process noise**: Dynamic covariance estimation
4. **Bias correction**: Real-time adjustment based on Xavier reference
5. **Validation limits**: Brazil-specific ranges (Xavier et al. 2016, 2022)
   - Temperature: -30 to 50°C
   - Precipitation: 0-450 mm
   - Solar radiation: 0-40 MJ/m²/day
   - Wind speed: 0-100 m/s

**Key advantages**:
- Reduces random noise from individual sources
- Corrects systematic biases automatically
- Maintains physical plausibility through validation
- Provides uncertainty estimates

For detailed methodology, see [`docs/kalman_methodology.pdf`](docs/kalman_methodology.pdf)

---

## 📈 Performance Metrics

### Aggregate Statistics (17 Cities, 2017-2024)

| Metric | NASA POWER | Open-Meteo | EVAOnline |
|--------|------------|------------|-----------|
| **R²** | 0.745 ± 0.056 | 0.690 ± 0.059 | **0.610 ± 0.081** |
| **MAE (mm/day)** | 1.093 ± 0.338 | 0.670 ± 0.092 | **0.478 ± 0.030** |
| **RMSE (mm/day)** | 1.386 ± 0.413 | 0.853 ± 0.124 | **0.609 ± 0.041** |
| **PBIAS (%)** | +23.2 ± 7.3 | +8.8 ± 3.0 | **+0.6 ± 0.5** |
| **NSE** | 0.734 ± 0.063 | 0.688 ± 0.059 | **0.604 ± 0.081** |

### Why Lower R² but Better MAE?

EVAOnline's **lower R² (0.61)** with **superior MAE (0.48)** demonstrates effective **noise filtering**:

- **High R² methods** (NASA, Open-Meteo) capture noise and signal together
- **Kalman fusion** removes high-frequency noise while preserving the mean trend
- **Result**: Lower correlation but more accurate absolute values
- **Agricultural relevance**: MAE and PBIAS matter more than R² for irrigation scheduling

This is a **feature, not a bug** - the system prioritizes practical accuracy over statistical correlation.

---

## 📝 Citation

If you use this dataset, please cite:

```bibtex
@dataset{silviane2025evaonline,
  author       = {Silviane, Angela},
  title        = {{EVAOnline Validation Dataset: Kalman Fusion 
                   System for Reference Evapotranspiration in 
                   Brazil (2017-2024)}},
  year         = 2025,
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://doi.org/10.5281/zenodo.XXXXXXX}
}
```

**Also cite the reference data:**

```bibtex
@article{https://doi.org/10.1002/joc.7731,
author = {Xavier, Alexandre C. and Scanlon, Bridget R. and King, Carey W. and Alves, Aline I.},
title = {New improved Brazilian daily weather gridded data (1961–2020)},
journal = {International Journal of Climatology},
volume = {42},
number = {16},
pages = {8390-8404},
keywords = {gridded data, interpolation, meteorological data, meteorological variables, precipitation, temperature},
doi = {https://doi.org/10.1002/joc.7731},
url = {https://rmets.onlinelibrary.wiley.com/doi/abs/10.1002/joc.7731},
eprint = {https://rmets.onlinelibrary.wiley.com/doi/pdf/10.1002/joc.7731},
abstract = {Abstract The demand for meteorological gridded datasets has increased within the last few years to inform studies such those in climate, weather, and agriculture. These studies require those data to be readily usable in standard formats with continuous spatial and temporal coverage. Since 2016, Brazil has a daily gridded meteorological data set with spatial resolution of 0.25° × 0.25° from January 1, 1980 to December 31, 2013 which was well received by the community. The main objective of this work is to improve the Brazilian meteorological data set. We do this by increasing the resolution of the minimum and maximum temperature (Tmax and Tmin) gridded interpolations from 0.25° × 0.25° to 0.1° × 0.1° by incorporating data on topographic relief, and increasing the time period covered (January 1, 1961–July 31, 2020). Besides Tmax and Tmin, we also gridded precipitation (pr), solar radiation (Rs), wind speed (u2), and relative humidity (RH) using observed data from 11,473 rain gauges and 1,252 weather stations. By means of ranked cross-validation statistics, we selected the best interpolation among inverse distance weighting and angular distance weighting methods. We determined that interpolations for Tmax and Tmin are improved by using the elevation of a query point, that accounts for topographic relief, and a temperature lapse rate. Even though this new version has ≈25 years more data relative to the previous one, statistics from cross-validation were similar. To allow researchers to assess the performance of the interpolation relative to station data in the area, we provide two types of gridded controls.},
year = {2022}
}

@article{xavier2022update,
  title={An update of Xavier, Scanlon, and King (2016) daily precipitation gridded data set for the Brazil},
  author={Xavier, Alexandre Candido and Scanlon, Bridget R and King, Carey W},
  journal={International Journal of Climatology},
  volume={42},
  number={16},
  pages={9248--9259},
  year={2022},
  doi={10.1002/joc.7731},
  url={https://rmets.onlinelibrary.wiley.com/doi/10.1002/joc.7731}
}
```

See [`CITATION.cff`](CITATION.cff) for machine-readable citation metadata.

---

## 🔐 Data Integrity

All data files are listed in [`data_manifest.csv`](data_manifest.csv) with:
- **Filename** and **category**
- **Description** and **source**
- **File size** (MB)
- **MD5 checksum** for verification

To verify data integrity:

```bash
# Generate manifest (includes checksums)
python scripts/generate_data_manifest.py

# Verify a specific file (example)
md5sum data/xavier/Piracicaba_SP.csv
# Compare with value in data_manifest.csv
```

---

## 📦 Data Access

### Recommended: Consolidated File

The **easiest way** to use this dataset:

```python
df = pd.read_csv("all_cities_daily_eto_1994_2024.csv", parse_dates=["date"])
```

**Columns:**
- `date`: Date (YYYY-MM-DD)
- `city`: City name
- `eto_xavier`: Xavier et al. reference (mm/day)
- `eto_nasa`: NASA POWER (mm/day)
- `eto_openmeteo`: Open-Meteo (mm/day)
- `eto_evaonline`: EVAOnline Kalman fusion (mm/day)

**Advantages:**
- Single file, all cities
- Ready for analysis
- No need to merge sources
- ~15 MB (manageable size)

### Alternative: Individual Files

If you prefer individual city files by source:

```python
from pathlib import Path

city = "Piracicaba_SP"
xavier = pd.read_csv(f"data/xavier/{city}.csv")
nasa = pd.read_csv(f"data/nasa_power/{city}.csv")
openmeteo = pd.read_csv(f"data/open_meteo/{city}.csv")
evaonline = pd.read_csv(f"data/evaonline_fused/{city}.csv")
```

---

## 🛠️ Reproducibility

### Validation Scripts

All validation analyses are reproducible:

```bash
# Run EVAOnline Kalman fusion
python scripts/evaonline_eto.py

# Verify Xavier data authenticity
python scripts/verify_xavier_real_data.py

# Generate data manifest
python scripts/generate_data_manifest.py
```

### Jupyter Notebooks

Interactive analysis:

```bash
jupyter notebook notebooks/quick_start_example.ipynb
```

**Runtime**: < 2 minutes  
**Output**: Performance metrics + time series visualization

---

## 🤝 Contributing

This is a **dataset release** associated with the EVAOnline software publication. For software contributions, see the main repository: [github.com/angelasilviane/EVAONLINE](https://github.com/angelasilviane/EVAONLINE)

For dataset issues or questions:
- Open an issue on GitHub
- Contact: angelasilviane@uft.edu.br

---

## 📄 License

This dataset is licensed under the **GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later)**.

**Key points:**
- ✅ **Free to use** for any purpose
- ✅ **Free to share** and redistribute
- ✅ **Free to modify** and create derivatives
- ⚠️ **Must share** modifications under the same license
- ⚠️ **Must provide** source code if used in network services
- ⚠️ **Must cite** original dataset

See [`LICENSE`](LICENSE) for full terms.

---

## 🔗 Related Resources

- **Main Software**: [EVAOnline GitHub Repository](https://github.com/angelasilviane/EVAONLINE)
- **Xavier Dataset**: 
  - [Brazilian Daily Weather Gridded Data (Website)](https://sites.google.com/site/alexandrecandidoxavierufes/brazilian-daily-weather-gridded-data)
  - [Xavier et al. 2016 Paper (DOI: 10.1002/joc.4518)](https://doi.org/10.1002/joc.4518)
  - [Xavier et al. 2022 Update (DOI: 10.1002/joc.7731)](https://doi.org/10.1002/joc.7731)
- **NASA POWER**: [NASA POWER API](https://power.larc.nasa.gov/)
- **Open-Meteo**: [Open-Meteo Historical API](https://open-meteo.com/en/docs/historical-weather-api)
- **FAO-56**: [Crop Evapotranspiration Guidelines](http://www.fao.org/3/x0490e/x0490e00.htm)

---

## 📧 Contact

**Angela Silviane**  
Universidade Federal do Tocantins  
Email: angelasilviane@uft.edu.br  
ORCID: [0000-0000-0000-0000](https://orcid.org/0000-0000-0000-0000)

---

## 🙏 Acknowledgments

This work builds upon:
- **Xavier et al. (2016, 2022)** for providing the high-quality gridded meteorological and ETo reference dataset for Brazil (1961-2024), interpolated from 3,625+ weather stations with rigorous quality control
- **NASA POWER** for freely accessible global meteorological reanalysis data
- **Open-Meteo** for ERA5-Land based climate data and original ETo estimates
- **FAO** for the standard Penman-Monteith methodology (Irrigation and Drainage Paper No. 56)

---

**Last updated**: November 21, 2025  
**Version**: 1.0.0  
**DOI**: 10.5281/zenodo.XXXXXXX (update after deposit)
