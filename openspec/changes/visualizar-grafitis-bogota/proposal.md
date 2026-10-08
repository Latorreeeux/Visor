# Proposal

## Why

Se necesita una forma rápida e interactiva de explorar cómo se distribuyen los grafitis en Bogotá sin depender de un inventario geográfico real. Una aplicación Streamlit con datos GeoJSON simulados permitirá comparar visualmente las zonas de mayor concentración y explorar puntos individuales.

## What Changes

- Crear una aplicación web de un solo archivo (`app.py`) con Streamlit, Folium y `streamlit-folium`.
- Generar al menos 80 entidades GeoJSON `Point` con propiedades de artista, localidad, tipo e identificador, concentradas principalmente alrededor de Puente Aranda y La Candelaria.
- Permitir alternar entre un mapa de calor y clústeres interactivos, con información emergente para cada grafiti.
- Mantener la vista centrada inicialmente en Bogotá sobre el mapa base CartoDB Dark Matter.

## Capabilities

### New Capabilities

- `visualizacion-espacial-grafitis`: Visualizar datos GeoJSON simulados de grafitis de Bogotá como mapa de calor o como clústeres interactivos.

### Modified Capabilities

Ninguna.

## Impact

- Nuevo archivo `app.py` en la raíz del proyecto.
- Dependencias de ejecución: `streamlit`, `folium` y `streamlit-folium`; `json` y `random` pertenecen a la biblioteca estándar de Python.
- No se integrarán fuentes de datos reales ni servicios geográficos externos; las ubicaciones serán sintéticas y se generarán dentro de la aplicación.
