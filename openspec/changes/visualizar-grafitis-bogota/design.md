# Design

## Context

El proyecto no contiene código previo ni especificaciones existentes para reutilizar. La solución se implementará en un único `app.py`, según la propuesta y los requisitos de `specs/visualizacion-espacial-grafitis/spec.md`.

## Goals / Non-Goals

**Goals:**

- Mantener los datos simulados estables mientras el usuario alterna las vistas durante una sesión de Streamlit.
- Separar la generación del GeoJSON y la construcción del mapa en funciones pequeñas dentro del mismo archivo.
- Mostrar ambas representaciones sobre la misma extensión geográfica y capa base.

**Non-Goals:**

- Consultar o almacenar ubicaciones reales de grafitis.
- Añadir persistencia entre sesiones, filtros por localidad o tipo, o edición de puntos.
- Añadir archivos de aplicación adicionales al `app.py` solicitado.

## Decisions

### Generación y conservación del GeoJSON

Se generará un `FeatureCollection` con puntos aleatorios agrupados alrededor de los dos epicentros indicados. Se crearán suficientes puntos en cada epicentro para que ambos sean visibles como concentraciones; las propiedades incluirán identificador, artista, localidad y un tipo de los valores Mural, Tag o Stencil. El GeoJSON se serializará con `json` y se guardará en `st.session_state`; en reruns posteriores se volverá a cargar desde esa cadena, evitando que el cambio de radio regenere las ubicaciones. Se elige este enfoque frente a volver a generar puntos en cada rerun porque conserva la continuidad visual sin mantener una fuente externa.

### Construcción de las vistas

Cada rerun creará un mapa Folium nuevo, centrado en `4.6097, -74.0817`, con zoom 12 y `cartodbdark_matter`. La selección lateral decidirá entre `HeatMap` con pares latitud-longitud y `MarkerCluster` con marcadores y popups HTML. Se usará `st_folium` en el área principal con un tamaño amplio para la interacción.

### Dependencias

Se usarán Streamlit, Folium y `streamlit-folium`, además de `json` y `random` de la biblioteca estándar. No se añadirá un archivo de dependencias separado para respetar el requisito de entregar todo el código de la aplicación en `app.py`; la ejecución presupone que esos paquetes de terceros están instalados.

## Risks / Trade-offs

- Las coordenadas y atributos son ficticios y no representan incidencia real → La interfaz y los nombres de variables deben identificarlos claramente como datos simulados.
- `cartodbdark_matter` y el mapa interactivo requieren acceso a recursos cartográficos en el navegador → La aplicación puede seguir generando las capas, pero el fondo puede no cargar sin conectividad.
- Mantener el dataset en el estado de sesión conserva consistencia durante una sesión, pero produce una muestra distinta al iniciar otra → Es el comportamiento esperado para datos aleatorios simulados.

## Migration Plan

No hay migración: se agregará `app.py` a la raíz y se ejecutará con Streamlit después de instalar las dependencias indicadas.
