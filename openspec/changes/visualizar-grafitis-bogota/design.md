# Design

## Context

El proyecto cuenta con una interfaz inicial que usa datos aleatorios. La fuente oficial consultada es la capa `Muros intervenidos` (capa 1) del servicio ArcGIS REST de Arte Urbano Responsable de la SCRD. Al 7 de octubre de 2026, la consulta devolvió 96 puntos y registros con año 2018 o 2019; el catálogo indica fecha del dato 2025-09-30. Esta cobertura corresponde a intervenciones documentadas, no a todos los grafitis de Bogotá.

## Goals / Non-Goals

**Goals:**

- Sustituir por completo la generación aleatoria por la descarga de GeoJSON desde el servicio distrital.
- Mantener los puntos cargados mientras el usuario alterna entre calor y clústeres, y evitar consultar el servicio en cada rerun.
- Atribuir claramente la fuente y su alcance limitado en la interfaz.
- Informar errores de consulta sin mostrar datos inventados como fallback.

**Non-Goals:**

- Mapear grafitis no registrados por el programa distrital.
- Usar la capa "Muros disponibles", que representa superficies candidatas para futuras intervenciones.
- Mantener una copia local de los datos o almacenar los registros de manera persistente.

## Decisions

### Fuente y formato

Consultar el endpoint público `https://serviciosgis.catastrobogota.gov.co/arcgis/rest/services/recreaciondeporte/arteurbanoresponsable/MapServer/1/query` con `where=1=1`, `returnGeometry=true` y `f=geojson`. La respuesta conserva las coordenadas y los nombres de campo publicados por ArcGIS. Se elige el GeoJSON del servicio REST frente a descargar un archivo estático para aprovechar futuras actualizaciones de la fuente.

### Campos mostrados

Usar `LECNOMARTI` (artista), `LECTITOBRA` (obra), `LECANIO` (año), `LECNOMLOC` (localidad), `LECTIPOFOR` (formato) y `LECTEMATIC` (temática) cuando tengan valor. Omitir en el popup los campos vacíos. No inferir ni crear un tipo de grafiti que la fuente no publique.

### Caché y fallos

Cachear la respuesta GeoJSON por un periodo limitado para estabilizar los reruns de Streamlit y reducir llamadas al servicio. Validar que la respuesta sea un `FeatureCollection` con puntos. Si la red, el servidor o el contenido falla, detener el mapa con un mensaje claro y un enlace a la fuente; nunca volver a los datos simulados.

### Interfaz y atribución

Conservar el mapa Folium y los modos `HeatMap` y `MarkerCluster`. Agregar a la barra lateral un enlace a la ficha de datos y una nota de atribución SCRD bajo licencia Creative Commons Attribution 4.0, junto con la aclaración de que se trata de intervenciones registradas.

## Risks / Trade-offs

- El servicio puede estar temporalmente caído o cambiar de URL → La interfaz comunica el fallo sin ocultarlo y enlaza a la ficha del conjunto para consultar la fuente.
- Los registros disponibles se concentran en 2018 y 2019 y no son exhaustivos → La aplicación los identifica como intervenciones documentadas por el Distrito, no como todos los grafitis de la ciudad.
- Algunos registros pueden carecer de título, artista u otros atributos → El popup muestra solamente los valores presentes.

## Migration Plan

No hay migración persistente. Se elimina la función generadora de datos sintéticos; la aplicación consulta la fuente oficial al iniciar y la caché mantiene la respuesta entre reruns.
