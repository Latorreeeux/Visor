# Tasks

## 1. Fuente oficial GeoJSON

- [x] 1.1 Consultar la capa ArcGIS REST "Muro Intervenido" y cargar sus puntos GeoJSON; verificar que la respuesta sea un `FeatureCollection` válido y que las coordenadas y atributos vengan del servicio oficial.
- [x] 1.2 Eliminar la generación aleatoria, cachear la fuente entre reruns y usar una instantánea local oficial cuando el servicio no sea accesible; mostrar un error únicamente si fallan ambos orígenes.

## 2. Visualización de datos oficiales

- [x] 2.1 Usar los atributos publicados en los popups compactos y mostrar las imágenes oficiales en el panel de la galería cuando estén disponibles.
- [x] 2.2 Actualizar el sidebar con la atribución SCRD, enlace a la ficha de datos y una nota sobre la cobertura limitada a intervenciones documentadas; verificar que aparezcan en la interfaz.
- [x] 2.3 Mantener HeatMap y MarkerCluster basados en las geometrías oficiales; verificar centro, zoom, cantidad de puntos y detalles en ambas vistas.
- [x] 2.4 En vista de clústeres, mostrar una galería circular en el popup de cada marcador con fotos; verificar navegación de ida, vuelta al inicio y selección de otro punto.

## 3. Integración

- [x] 3.1 Ejecutar `streamlit run app.py` con las dependencias instaladas; verificar que carga registros reales y permite alternar entre densidad y clústeres sin errores.
