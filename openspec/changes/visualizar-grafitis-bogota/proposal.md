# Proposal

## Why

Se necesita una forma rápida e interactiva de explorar la distribución espacial del arte urbano documentado oficialmente en Bogotá. La Secretaría Distrital de Cultura publica una capa geográfica de muros intervenidos que permite visualizar registros reales en vez de inventar ubicaciones.

## What Changes

- Crear una aplicación web de un solo archivo (`app.py`) con Streamlit, Folium y `streamlit-folium`.
- Consultar la capa GeoJSON oficial "Muro Intervenido - Distrito Grafiti" de la Secretaría Distrital de Cultura, Recreación y Deporte.
- Mostrar únicamente las intervenciones que devuelve la fuente; no fabricar puntos ni sustituirlos por datos simulados si el servicio falla.
- Permitir alternar entre un mapa de calor y clústeres interactivos, con información emergente para cada grafiti.
- Mostrar las imágenes del punto seleccionado en una galería dentro del popup del marcador, con navegación circular.
- Mantener la vista centrada inicialmente en Bogotá sobre el mapa base CartoDB Dark Matter.
- Atribuir la fuente oficial y explicar que el conjunto documenta intervenciones registradas, no todos los grafitis existentes en la ciudad.

## Capabilities

### New Capabilities

- `visualizacion-espacial-grafitis`: Visualizar como mapa de calor o clústeres las intervenciones de arte urbano georreferenciadas y publicadas por el Distrito.

### Modified Capabilities

Ninguna.

## Impact

- Nuevo archivo `app.py` en la raíz del proyecto.
- Dependencias de ejecución: `streamlit`, `folium` y `streamlit-folium`; la carga GeoJSON usará la biblioteca estándar de Python.
- Fuente: ArcGIS REST de la capa "Muros intervenidos" publicada por la SCRD, capa 1 del servicio Arte Urbano Responsable; licencia Creative Commons Attribution 4.0.
- El conjunto consultado contiene 96 puntos con registros de 2018 y 2019 (consulta del 7 de octubre de 2026; metadatos con fecha del dato 2025-09-30). No representa un inventario exhaustivo de grafitis.
