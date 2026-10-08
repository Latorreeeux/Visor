# Spec Delta

## Purpose

Permite explorar la distribución espacial de grafitis simulados en Bogotá mediante un mapa interactivo que destaca concentraciones y ofrece detalles de cada punto.

## ADDED Requirements

### Requirement: Generar datos GeoJSON simulados de grafitis
La aplicación SHALL generar un `FeatureCollection` GeoJSON válido con al menos 80 entidades de tipo `Point`, cada una con propiedades `id`, `artista`, `localidad` y `tipo`; los datos SHALL concentrarse principalmente alrededor de Puente Aranda y La Candelaria.

#### Scenario: Conjunto simulado contiene entidades válidas
- **WHEN** la aplicación genera sus datos para una sesión
- **THEN** produce al menos 80 puntos GeoJSON con las cuatro propiedades requeridas y coordenadas cercanas a los epicentros indicados

### Requirement: Presentar el mapa de Bogotá y selector de visualización
La aplicación SHALL mostrar un mapa centrado inicialmente en Bogotá y permitir elegir entre la vista de densidad y la vista de clústeres desde el panel lateral.

#### Scenario: Vista inicial de densidad
- **WHEN** el usuario abre la aplicación por primera vez
- **THEN** ve el panel titulado "🎨 Densidad de Arte Urbano - Bogotá", una descripción breve, la opción "Mapa de Calor (Densidad)" seleccionada y un mapa centrado en Bogotá con zoom 12

#### Scenario: Mapa base oscuro
- **WHEN** se presenta cualquiera de las vistas del mapa
- **THEN** el mapa usa la capa base CartoDB Dark Matter y se muestra en el área principal con tamaño suficiente para explorar la ciudad

### Requirement: Mostrar la concentración como mapa de calor
La aplicación SHALL representar las coordenadas de los grafitis como una capa de calor cuando el usuario elija la vista de densidad.

#### Scenario: Activar mapa de calor
- **WHEN** el usuario selecciona "Mapa de Calor (Densidad)"
- **THEN** el mapa presenta una capa de calor derivada de las latitudes y longitudes de todos los puntos simulados

### Requirement: Explorar grafitis mediante clústeres y detalles
La aplicación SHALL agrupar los grafitis en clústeres interactivos y permitir consultar en cada marcador sus propiedades de artista, tipo y localidad.

#### Scenario: Inspeccionar un grafiti
- **WHEN** el usuario selecciona "Clústeres (Interactivos)" y abre un marcador individual
- **THEN** el mapa muestra una ventana emergente con artista, tipo y localidad de ese grafiti

#### Scenario: Agrupar puntos cercanos
- **WHEN** varios marcadores están próximos en el nivel de zoom actual
- **THEN** el mapa los presenta agrupados y permite interactuar para explorar los puntos individuales
