# Tasks

## 1. Datos GeoJSON simulados

- [x] 1.1 Implementar en `app.py` la generación de un `FeatureCollection` con al menos 80 puntos, propiedades requeridas y coordenadas concentradas en los dos epicentros; verificar estructura, tipos, propiedades y cantidad mediante una inspección automatizada del resultado.
- [x] 1.2 Conservar el GeoJSON serializado en el estado de sesión para que cambiar el selector no regenere los puntos; verificar que el conjunto se mantenga igual al alternar las dos vistas.

## 2. Interfaz y mapa interactivo

- [x] 2.1 Configurar Streamlit en modo ancho y construir el sidebar con título, descripción y las dos opciones exactas del selector; verificar las etiquetas y que la vista inicial sea el mapa de calor.
- [x] 2.2 Construir el mapa Folium centrado en Bogotá con zoom 12 y la capa base CartoDB Dark Matter; verificar centro, zoom y capa en ambas vistas.
- [x] 2.3 Añadir la capa HeatMap a partir de las coordenadas GeoJSON y verificar que incluya las ubicaciones simuladas.
- [x] 2.4 Añadir MarkerCluster con un marcador por entidad y popups HTML con artista, tipo y localidad; verificar que los detalles correspondan a las propiedades del punto.
- [x] 2.5 Renderizar el mapa en el área principal con `st_folium` y dimensiones amplias; verificar la interacción y visualización en ambas opciones.

## 3. Integración de la aplicación

- [x] 3.1 Ejecutar `streamlit run app.py` con Streamlit, Folium y `streamlit-folium` instalados; verificar que la aplicación abra sin errores y que se pueda alternar entre densidad y clústeres.
