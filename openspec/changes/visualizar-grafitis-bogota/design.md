# Design

## Context

El proyecto cuenta con una interfaz inicial que usa datos aleatorios. La fuente oficial consultada es la capa `Muros intervenidos` (capa 1) del servicio ArcGIS REST de Arte Urbano Responsable de la SCRD. Al 7 de octubre de 2026, la consulta devolvió 96 puntos y registros con año 2018 o 2019; el catálogo indica fecha del dato 2025-09-30. Esta cobertura corresponde a intervenciones documentadas, no a todos los grafitis de Bogotá.

## Goals / Non-Goals

**Goals:**

- Sustituir por completo la generación aleatoria por GeoJSON del servicio distrital o por una instantánea local descargada de ese mismo servicio.
- Mantener los puntos cargados mientras el usuario alterna entre calor y clústeres, y evitar consultar el servicio en cada rerun.
- Atribuir claramente la fuente y su alcance limitado en la interfaz.
- Informar cuando se muestre la instantánea por falta de conectividad; nunca usar datos inventados como fallback.

**Non-Goals:**

- Mapear grafitis no registrados por el programa distrital.
- Usar la capa "Muros disponibles", que representa superficies candidatas para futuras intervenciones.
- Mantener un histórico o almacenamiento editable de los registros.

## Decisions

### Fuente y formato

Consultar el endpoint público `https://serviciosgis.catastrobogota.gov.co/arcgis/rest/services/recreaciondeporte/arteurbanoresponsable/MapServer/1/query` con `where=1=1`, `returnGeometry=true` y `f=geojson`. La respuesta conserva las coordenadas y los nombres de campo publicados por ArcGIS. Se elige el GeoJSON del servicio REST frente a descargar un archivo estático para aprovechar futuras actualizaciones de la fuente.

### Campos mostrados

Usar `LECNOMARTI` (artista), `LECTITOBRA` (obra), `LECANIO` (año), `LECNOMLOC` (localidad), `LECTIPOFOR` (formato), `LECTEMATIC` (temática) y `LECIMAGEN1` a `LECIMAGEN5` (fotografías) cuando tengan valor. Omitir en el popup los campos vacíos. Mostrar las imágenes como miniaturas enlazadas al original y aceptar solo enlaces HTTP(S) del dominio oficial `cultured.scrd.gov.co`. No inferir ni crear un tipo de grafiti que la fuente no publique.

### Caché y fallos

Cachear la respuesta GeoJSON por un periodo limitado para estabilizar los reruns de Streamlit y reducir llamadas al servicio. Validar que la respuesta sea un `FeatureCollection` con puntos. Si la red, el servidor o el contenido falla, cargar `data/muros_intervenidos.geojson`, una instantánea oficial versionada, e indicar su fecha en la interfaz. Si la instantánea también falla, detener el mapa con un mensaje claro y un enlace a la fuente. Nunca volver a datos simulados.

### Interfaz y atribución

Conservar el mapa Folium y los modos `HeatMap` y `MarkerCluster`. Usar OpenStreetMap como mapa base, ya que los mosaicos CartoDB Dark Matter requieren una clave de API en el entorno actual. Agregar sus atribuciones y mantener en la barra lateral el enlace a la ficha de datos y la atribución SCRD bajo licencia Creative Commons Attribution 4.0, junto con la aclaración de que se trata de intervenciones registradas.

### Galería de imágenes por intervención

En la vista de clústeres, mostrar los metadatos y la galería dentro del popup del marcador seleccionado. El popup funciona como panel anclado al punto y enseña una imagen a la vez. Usar controles CSS con radios por galería para que las flechas anterior y siguiente recorran las imágenes de forma circular sin depender del canal de eventos Python de `st_folium`. Al abrir otro marcador, su carrusel comienza en la primera imagen. En la vista de calor, conservar el mapa a ancho completo.

## Risks / Trade-offs

- El servicio puede estar temporalmente caído o cambiar de URL → La interfaz muestra la instantánea oficial con aviso de fecha y enlaza a la ficha para consultar la fuente actual.
- Los registros disponibles se concentran en 2018 y 2019 y no son exhaustivos → La aplicación los identifica como intervenciones documentadas por el Distrito, no como todos los grafitis de la ciudad.
- Algunos registros pueden carecer de título, artista u otros atributos → El popup muestra solamente los valores presentes.
- Los enlaces de fotografía pueden no responder → El panel identifica la foto actual y conserva el enlace directo a la imagen original.

## Migration Plan

Se elimina la función generadora de datos sintéticos; la aplicación consulta la fuente oficial al iniciar y la caché mantiene la respuesta entre reruns. La instantánea versionada permite ejecutar el visor en entornos sin acceso de red.
