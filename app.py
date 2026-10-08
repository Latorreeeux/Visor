"""Visualización interactiva de grafitis simulados en Bogotá."""

import html
import json
import random

import folium
import streamlit as st
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium


CENTRO_BOGOTA = [4.6097, -74.0817]
EPICENTROS = [
    {"localidad": "Puente Aranda", "latitud": 4.628, "longitud": -74.113},
    {"localidad": "La Candelaria", "latitud": 4.596, "longitud": -74.072},
]
ARTISTAS = [
    "Bastardilla",
    "Toxicómano",
    "Ledania",
    "Guache",
    "Erre",
    "Mónica Carrillo",
    "DJ Lu",
    "Cacerolo",
]
TIPOS = ["Mural", "Tag", "Stencil"]


def generar_geojson(cantidad_por_epicentro=40, cantidad_adicional=20):
    """Genera un FeatureCollection con puntos simulados en Bogotá."""
    features = []
    identificador = 1

    for epicentro in EPICENTROS:
        for _ in range(cantidad_por_epicentro):
            latitud = random.gauss(epicentro["latitud"], 0.004)
            longitud = random.gauss(epicentro["longitud"], 0.004)
            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [longitud, latitud],
                    },
                    "properties": {
                        "id": identificador,
                        "artista": random.choice(ARTISTAS),
                        "localidad": epicentro["localidad"],
                        "tipo": random.choice(TIPOS),
                    },
                }
            )
            identificador += 1

    # Algunos puntos adicionales amplían la cobertura del mapa sin ocultar
    # las concentraciones principales de Puente Aranda y La Candelaria.
    for _ in range(cantidad_adicional):
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        random.uniform(-74.16, -74.02),
                        random.uniform(4.55, 4.72),
                    ],
                },
                "properties": {
                    "id": identificador,
                    "artista": random.choice(ARTISTAS),
                    "localidad": "Bogotá",
                    "tipo": random.choice(TIPOS),
                },
            }
        )
        identificador += 1

    return {"type": "FeatureCollection", "features": features}


def obtener_geojson_de_sesion():
    """Conserva la misma muestra simulada durante toda la sesión."""
    clave = "geojson_grafitis_bogota"
    if clave not in st.session_state:
        st.session_state[clave] = json.dumps(
            generar_geojson(), ensure_ascii=False
        )
    return json.loads(st.session_state[clave])


def crear_mapa(geojson, vista):
    """Construye el mapa Folium para la vista seleccionada."""
    mapa = folium.Map(
        location=CENTRO_BOGOTA,
        zoom_start=12,
        tiles="cartodbdark_matter",
    )

    features = geojson["features"]

    if vista == "Mapa de Calor (Densidad)":
        coordenadas = [
            [feature["geometry"]["coordinates"][1], feature["geometry"]["coordinates"][0]]
            for feature in features
        ]
        HeatMap(coordenadas, radius=16, blur=12, min_opacity=0.35).add_to(mapa)
    else:
        cluster = MarkerCluster(name="Grafitis").add_to(mapa)
        for feature in features:
            longitud, latitud = feature["geometry"]["coordinates"]
            propiedades = feature["properties"]
            artista = html.escape(str(propiedades["artista"]))
            tipo = html.escape(str(propiedades["tipo"]))
            localidad = html.escape(str(propiedades["localidad"]))
            popup_html = (
                "<div style='min-width: 160px'>"
                f"<strong>Artista:</strong> {artista}<br>"
                f"<strong>Tipo:</strong> {tipo}<br>"
                f"<strong>Localidad:</strong> {localidad}"
                "</div>"
            )
            folium.Marker(
                location=[latitud, longitud],
                tooltip=f"Grafiti #{propiedades['id']}",
                popup=folium.Popup(popup_html, max_width=300),
            ).add_to(cluster)

    return mapa


def main():
    st.set_page_config(
        page_title="Densidad de Arte Urbano - Bogotá",
        page_icon="🎨",
        layout="wide",
    )

    st.sidebar.title("🎨 Densidad de Arte Urbano - Bogotá")
    st.sidebar.write(
        "Explora la distribución espacial de grafitis simulados en Bogotá. "
        "Compara las zonas de mayor concentración y consulta detalles de cada punto."
    )
    vista = st.sidebar.radio(
        "Vista del mapa:",
        ["Mapa de Calor (Densidad)", "Clústeres (Interactivos)"],
    )

    geojson = obtener_geojson_de_sesion()
    mapa = crear_mapa(geojson, vista)
    st_folium(mapa, width=1000, height=600)


if __name__ == "__main__":
    main()
