# Visor de arte urbano de Bogotá

**Autora:** Karen Tatiana Latorre Conde  
**Código:** 20251025129

## Proyecto

Aplicación web para explorar espacialmente las intervenciones de arte urbano registradas por la Secretaría Distrital de Cultura, Recreación y Deporte de Bogotá. Presenta los puntos oficiales en un mapa de calor o en clústeres interactivos, con información y fotografías asociadas cuando están disponibles.

Los registros corresponden a intervenciones documentadas por el programa distrital; no representan un inventario completo de todos los grafitis de la ciudad. La aplicación no genera ubicaciones artificiales.

## Requisitos

- Python 3.10 o posterior
- `streamlit`
- `folium`
- `streamlit-folium`

## Ejecución

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install streamlit folium streamlit-folium
streamlit run app.py
```

La aplicación consulta la capa GeoJSON oficial y utiliza una instantánea local incluida en `data/` si la fuente no está disponible.

## Fuente de datos

- [Muros intervenidos — Datos Abiertos Bogotá](https://datosabiertos.bogota.gov.co/dataset/muros-intervenidos)
- Secretaría Distrital de Cultura, Recreación y Deporte. Atribución bajo licencia Creative Commons Attribution 4.0, según la ficha del conjunto de datos.
