# Spec Delta

## Purpose

Permite explorar la distribución de las intervenciones de arte urbano georreferenciadas que publica el Distrito para Bogotá, con representaciones de densidad y consulta de los registros individuales.

## ADDED Requirements

### Requirement: Cargar registros geográficos oficiales de intervenciones
La aplicación SHALL obtener los registros GeoJSON de la capa oficial "Muro Intervenido - Distrito Grafiti" publicada por la Secretaría Distrital de Cultura, Recreación y Deporte y SHALL usar sus geometrías y atributos sin fabricar ubicaciones.

#### Scenario: El servicio oficial entrega registros
- **WHEN** el servicio REST de la fuente responde con una colección GeoJSON válida
- **THEN** la aplicación visualiza sus puntos reales y conserva los atributos publicados para cada intervención

#### Scenario: El servicio oficial no está disponible
- **WHEN** la fuente no responde, devuelve un error o no entrega una colección GeoJSON válida
- **THEN** la aplicación informa que los datos oficiales no pudieron cargarse y no presenta puntos simulados como sustituto

### Requirement: Comunicar procedencia y cobertura de los datos
La aplicación SHALL atribuir los datos a la SCRD e indicar que representan intervenciones documentadas por el programa, no un inventario exhaustivo de todos los grafitis de Bogotá.

#### Scenario: Usuario consulta la fuente
- **WHEN** el usuario visualiza el mapa
- **THEN** puede identificar la fuente oficial, abrir su ficha de datos y entender el alcance limitado de los registros

### Requirement: Presentar el mapa y selector de visualización
La aplicación SHALL mostrar un mapa inicialmente centrado en Bogotá y permitir elegir la vista de densidad o la vista de clústeres desde el panel lateral.

#### Scenario: Vista inicial de densidad
- **WHEN** el usuario abre la aplicación por primera vez
- **THEN** ve el panel titulado "🎨 Densidad de Arte Urbano - Bogotá", una descripción breve, la opción "Mapa de Calor (Densidad)" seleccionada y un mapa centrado en Bogotá con zoom 12

#### Scenario: Mapa base oscuro
- **WHEN** se presenta cualquiera de las vistas
- **THEN** el mapa usa la capa base CartoDB Dark Matter y se muestra en el área principal con tamaño suficiente para explorar la ciudad

### Requirement: Mostrar la densidad de intervenciones
La aplicación SHALL calcular la capa de calor usando las coordenadas de los puntos válidos devueltos por la fuente oficial.

#### Scenario: Activar mapa de calor
- **WHEN** el usuario selecciona "Mapa de Calor (Densidad)"
- **THEN** el mapa presenta una capa de calor basada en las coordenadas de todas las intervenciones cargadas

### Requirement: Consultar intervenciones mediante clústeres
La aplicación SHALL agrupar los puntos oficiales en clústeres y permitir consultar los atributos publicados de cada intervención.

#### Scenario: Inspeccionar una intervención
- **WHEN** el usuario selecciona "Clústeres (Interactivos)" y abre un marcador
- **THEN** el mapa muestra los valores disponibles de artista, obra, año y localidad para ese registro

#### Scenario: Agrupar puntos cercanos
- **WHEN** varios marcadores están próximos en el nivel de zoom actual
- **THEN** el mapa los presenta agrupados y permite explorar los puntos individuales
