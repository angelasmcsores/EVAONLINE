# Study Area Map Generation

This document describes how to generate the study area map showing the 17 cities used in the EVAOnline validation dataset.

## Data Sources

### Official Brazilian Geographic Data

1. **MATOPIBA Region Definition**
   - Source: MAGALHÃES, L. A.; MIRANDA, E. E. de. MATOPIBA: Quadro Natural. Campinas: Embrapa, 2014. (Embrapa. Nota Técnica GITE, 5). 41 p.
   - URL: https://www.infoteca.cnptia.embrapa.br/infoteca/handle/doc/1037412
   - Description: Technical note defining the natural framework of MATOPIBA region

2. **IBGE Climate Map of Brazil**
   - Source: IBGE. 2002. Mapa de Clima do Brasil.
   - Viewer: http://www.visualizador.inde.gov.br/
   - Downloads: https://www.ibge.gov.br/geociencias/informacoes-ambientais/climatologia/15817-clima.html?=&t=downloads
   - Description: Official climate classification and boundaries for Brazil

3. **IBGE Geospatial Data**
   - States boundaries (Maranhão, Tocantins, Piauí, Bahia, São Paulo)
   - Municipalities boundaries
   - Brazilian territory outline

## Study Cities (17 locations)

### MATOPIBA Region (16 cities):

**Maranhão (MA) - 4 cities:**
- Balsas: -7.532, -46.036
- Carolina: -7.334, -47.467
- Imperatriz: -5.526, -47.479
- Tasso Fragoso: -8.513, -46.216

**Tocantins (TO) - 4 cities:**
- Araguaína: -7.191, -48.207
- Campos Lindos: -7.991, -46.866
- Pedro Afonso: -8.969, -48.173
- Porto Nacional: -10.708, -48.417

**Piauí (PI) - 4 cities:**
- Alvorada do Gurguéia: -8.429, -43.774
- Bom Jesus: -9.077, -44.358
- Corrente: -10.439, -45.161
- Uruçuí: -7.234, -44.549

**Bahia (BA) - 4 cities:**
- Barreiras: -12.153, -44.990
- Formosa do Rio Preto: -11.047, -45.195
- Luiz Eduardo Magalhães: -12.095, -45.802
- São Desidério: -12.360, -44.973

### Control Site (1 city):

**São Paulo (SP), Brazil - 1 city:**
- Piracicaba: -22.725, -47.649
  * Located outside MATOPIBA

## Map Requirements

### Essential Elements:
1. Brazilian territory outline
2. MATOPIBA region highlighted (shaded or outlined)
3. State boundaries (MA, TO, PI, BA, SP)
4. 17 city markers with labels
5. Piracicaba (SP) marked differently (control site)
6. Legend
7. Scale bar
8. North arrow
9. Coordinate grid (optional)

## Suggested Tools

### Python Libraries:
```python
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
from matplotlib.patches import Rectangle
```

### R Libraries:
```r
library(ggplot2)
library(sf)
library(rnaturalearth)
library(rnaturalearthdata)
library(ggspatial)
```

### GIS Software:
- QGIS (free, open-source)
- ArcGIS
- Google Earth Engine

## Map Specifications

### For README (Web):
- Format: PNG
- Resolution: 300 DPI
- Width: 800-1200 pixels
- File: `figures/study_area_map.png`

### For Publication (SoftwareX):
- Format: PNG
- Resolution: 300 DPI
- Width: 2244-1806 pixels
- File: `figures/study_area_map_high_res.png`

### For Graphical Abstract (Zenodo):
- Format: PNG
- Resolution: 300 DPI
- Dimensions: 1328 × 531 pixels (or proportionally larger)
- File: `figures/graphical_abstract.png`

## Citations for Map

When using this map in publications, cite:

1. **For MATOPIBA definition:**
   ```
   MAGALHÃES, L. A.; MIRANDA, E. E. de. MATOPIBA: Quadro Natural. 
   Campinas: Embrapa, 2014. (Embrapa. Nota Técnica GITE, 5). 41 p.
   ```

2. **For Brazil boundaries:**
   ```
   IBGE. Mapa de Clima do Brasil. Instituto Brasileiro de Geografia e 
   Estatística, 2002. Disponível em: http://www.visualizador.inde.gov.br/
   ```

3. **For Xavier reference cities:**
   ```
   Xavier, A. C., King, C. W., & Scanlon, B. R. (2016). Daily gridded 
   meteorological variables in Brazil (1980-2013). International Journal 
   of Climatology, 36(6), 2644-2659. https://doi.org/10.1002/joc.4518
   ```
   ```
   Xavier, A. C., Scanlon, B. R., King, C. W., & Alves, A. I. (2022). 
   New improved Brazilian daily weather gridded data (1961–2020). 
   International Journal of Climatology, 42(16), 8390–8404. 
   https://doi.org/10.1002/joc.7731
   ```

## Example Python Script

See `scripts/generate_study_area_map.py` for a complete implementation.

Quick usage:
```bash
# Install dependencies
pip install matplotlib cartopy geopandas

# Generate map
python scripts/generate_study_area_map.py

# Output: figures/study_area_map.png
```

## Notes

- MATOPIBA is Brazil's newest agricultural frontier
- Region encompasses 73 million hectares across 4 states
- Name: **MA**ranhão + **TO**cantins + **PI**auí + **BA**hia
- Piracicaba included as control site due to historical data availability
- All coordinates in WGS84 (EPSG:4326)
- Map projection: Mercator or Plate Carrée recommended for Brazil

---

**Last updated**: November 21, 2025
