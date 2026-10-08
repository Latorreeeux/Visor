"""Mapa interactivo de intervenciones de arte urbano documentadas en Bogotá."""

import html
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

import folium
import streamlit as st
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium


CENTRO_BOGOTA = [4.6097, -74.0817]
URL_CAPA_OFICIAL = (
    "https://serviciosgis.catastrobogota.gov.co/arcgis/rest/services/"
    "recreaciondeporte/arteurbanoresponsable/MapServer/1/query"
)
URL_FICHA_DATOS = "https://datosabiertos.bogota.gov.co/dataset/muros-intervenidos"
URL_MAPA_MUROS_DISPONIBLES = (
    "https://sdcrd.maps.arcgis.com/apps/dashboards/"
    "3bf6088e56054662af6d88880dd809df"
)
RUTA_INSTANTANEA_OFICIAL = Path(__file__).parent / "data" / "muros_intervenidos.geojson"
FECHA_INSTANTANEA_OFICIAL = "2026-10-07"


def validar_geojson(coleccion):
    """Filtra puntos con coordenadas válidas de un FeatureCollection."""
    if not isinstance(coleccion, dict) or coleccion.get("type") != "FeatureCollection":
        raise ValueError("La respuesta no es un FeatureCollection GeoJSON.")

    puntos_validos = []
    for feature in coleccion.get("features", []):
        geometria = feature.get("geometry") or {}
        coordenadas = geometria.get("coordinates")
        if (
            geometria.get("type") == "Point"
            and isinstance(coordenadas, list)
            and len(coordenadas) >= 2
            and isinstance(coordenadas[0], (int, float))
            and isinstance(coordenadas[1], (int, float))
        ):
            puntos_validos.append(feature)

    if not puntos_validos:
        raise ValueError("La fuente no contiene puntos con coordenadas válidas.")
    return {"type": "FeatureCollection", "features": puntos_validos}


@st.cache_data(ttl=3600, show_spinner="Cargando intervenciones oficiales...")
def cargar_geojson_oficial():
    """Consulta la capa SCRD; usa su instantánea oficial si no hay red."""
    parametros = urlencode(
        {
            "where": "1=1",
            "outFields": "*",
            "returnGeometry": "true",
            "resultRecordCount": "2000",
            "f": "geojson",
        }
    )
    solicitud = Request(
        f"{URL_CAPA_OFICIAL}?{parametros}",
        headers={
            "Accept": "application/geo+json, application/json",
            "User-Agent": "VisorArteUrbanoBogota/1.0",
        },
    )

    try:
        with urlopen(solicitud, timeout=25) as respuesta:
            coleccion = json.loads(respuesta.read().decode("utf-8-sig"))
        return validar_geojson(coleccion), False
    except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError) as error:
        try:
            with RUTA_INSTANTANEA_OFICIAL.open(encoding="utf-8") as archivo:
                instantanea = validar_geojson(json.load(archivo))
            return instantanea, True
        except (OSError, json.JSONDecodeError, ValueError) as error_instantanea:
            raise RuntimeError(
                "No fue posible consultar la capa oficial ni cargar su copia local. "
                f"Revisa la conexión y abre la ficha de datos. ({error})"
            ) from error_instantanea


def crear_popup(propiedades, indice_feature=0):
    """Construye un panel emergente con metadatos y galería circular."""
    campos = [
        ("Artista", "LECNOMARTI"),
        ("Obra", "LECTITOBRA"),
        ("Año", "LECANIO"),
        ("Localidad", "LECNOMLOC"),
        ("Formato", "LECTIPOFOR"),
        ("Temática", "LECTEMATIC"),
    ]
    filas = []
    for etiqueta, campo in campos:
        valor = propiedades.get(campo)
        if valor is None or not str(valor).strip():
            continue
        filas.append(
            f"<strong>{etiqueta}:</strong> {html.escape(str(valor))}"
        )

    contenido = "<div class='datos-intervencion'>" + "<br>".join(filas) + "</div>"
    urls = obtener_urls_imagen(propiedades)
    if urls:
        id_galeria = f"galeria-{indice_feature}"
        radios = []
        diapositivas = []
        reglas_css = []
        titulo = html.escape(str(propiedades.get("LECTITOBRA") or "Intervención"), quote=True)

        for indice, url in enumerate(urls):
            id_radio = f"{id_galeria}-foto-{indice}"
            anterior = f"{id_galeria}-foto-{(indice - 1) % len(urls)}"
            siguiente = f"{id_galeria}-foto-{(indice + 1) % len(urls)}"
            url_segura = html.escape(url, quote=True)
            radios.append(
                f"<input type='radio' name='{id_galeria}' id='{id_radio}'"
                f"{' checked' if indice == 0 else ''}>"
            )
            diapositivas.append(
                f"<div class='diapositiva' id='{id_radio}-panel'>"
                f"<a href='{url_segura}' target='_blank' rel='noopener noreferrer'>"
                f"<img src='{url_segura}' alt='{titulo} — foto {indice + 1}'></a>"
                "<div class='navegacion'>"
                f"<label for='{anterior}' title='Foto anterior'>&#8592;</label>"
                f"<span>Foto {indice + 1} de {len(urls)}</span>"
                f"<label for='{siguiente}' title='Foto siguiente'>&#8594;</label>"
                "</div></div>"
            )
            reglas_css.append(
                f"#{id_radio}:checked ~ .diapositivas #{id_radio}-panel "
                "{display:block}"
            )

        contenido += (
            f"<section class='galeria' id='{id_galeria}'>"
            f"{''.join(radios)}<div class='diapositivas'>{''.join(diapositivas)}</div></section>"
            "<style>"
            ".galeria input{display:none}"
            ".diapositiva{display:none;text-align:center}"
            ".diapositiva img{width:100%;height:210px;object-fit:contain;background:#f2f2f2}"
            ".navegacion{display:flex;align-items:center;justify-content:space-between;padding:6px 14px}"
            ".navegacion label{cursor:pointer;font-size:24px;font-weight:bold;padding:0 12px;user-select:none}"
            ".navegacion label:hover{color:#1388d3}"
            ".navegacion span{font-size:12px}"
            + "".join(reglas_css)
            + "</style>"
        )
    return "<div style='min-width: 180px; max-width: 300px'>" + contenido + "</div>"


def tiene_imagen(feature):
    """Indica si el registro publica al menos una imagen válida."""
    return bool(obtener_urls_imagen(feature.get("properties") or {}))


def obtener_urls_imagen(propiedades):
    """Devuelve solo enlaces de imagen HTTP(S) del servidor oficial de SCRD."""
    urls = []
    for indice in range(1, 6):
        valor = propiedades.get(f"LECIMAGEN{indice}")
        if not isinstance(valor, str) or valor.strip().lower() in {"", "n.a.", "n.a", "na"}:
            continue
        url = valor.strip()
        partes = urlsplit(url)
        if partes.scheme in {"http", "https"} and partes.hostname == "cultured.scrd.gov.co":
            urls.append(url)
    return urls


def crear_mapa(geojson, vista):
    """Construye la vista Folium seleccionada a partir de puntos oficiales."""
    mapa = folium.Map(
        location=CENTRO_BOGOTA,
        zoom_start=12,
        tiles="OpenStreetMap",
    )
    features = geojson["features"]

    if vista == "Mapa de Calor (Densidad)":
        coordenadas = [
            [
                feature["geometry"]["coordinates"][1],
                feature["geometry"]["coordinates"][0],
            ]
            for feature in features
        ]
        HeatMap(coordenadas, radius=16, blur=12, min_opacity=0.35).add_to(mapa)
    else:
        cluster = MarkerCluster(name="Intervenciones oficiales").add_to(mapa)
        for indice, feature in enumerate(features):
            longitud, latitud = feature["geometry"]["coordinates"][:2]
            propiedades = feature.get("properties") or {}
            identificador = propiedades.get("OBJECTID", "")
            titulo = propiedades.get("LECTITOBRA") or f"Intervención {identificador}"
            marcador = folium.Marker(
                location=[latitud, longitud],
                tooltip=html.escape(str(titulo)),
                popup=folium.Popup(crear_popup(propiedades, indice), max_width=340),
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
        "Explora las intervenciones de arte urbano documentadas por el programa "
        "Distrito Grafiti. Estos registros no representan todos los grafitis de Bogotá."
    )
    st.sidebar.radio(
        "Vista del mapa:",
        ["Mapa de Calor (Densidad)", "Clústeres (Interactivos)"],
        key="vista_mapa",
    )
    vista = st.session_state["vista_mapa"]

    st.sidebar.markdown(
        "**Fuente:** [SCRD / Datos Abiertos Bogotá]("
        f"{URL_FICHA_DATOS}) · Licencia CC BY 4.0."
    )
    st.sidebar.markdown(
        f"[Mapa distrital de muros disponibles]({URL_MAPA_MUROS_DISPONIBLES})"
    )
    st.sidebar.caption("Mapa base: © OpenStreetMap contributors.")
    st.sidebar.caption(
        "La capa muestra muros intervenidos registrados por el Distrito; "
        "los muros disponibles son superficies para futuras intervenciones."
    )

    try:
        with st.spinner("Consultando la capa geográfica oficial..."):
            geojson, es_instantanea = cargar_geojson_oficial()
    except RuntimeError as error:
        st.error(str(error))
        st.link_button("Abrir la ficha de datos", URL_FICHA_DATOS)
        st.stop()

    if es_instantanea:
        st.warning(
            "El servicio oficial no está accesible desde este entorno. "
            f"Se muestra su copia GeoJSON descargada el {FECHA_INSTANTANEA_OFICIAL}; "
            "contiene datos oficiales, no simulados."
        )

    años = sorted(
        {
            str(feature.get("properties", {}).get("LECANIO"))
            for feature in geojson["features"]
            if feature.get("properties", {}).get("LECANIO")
        }
    )
    st.sidebar.metric("Intervenciones cargadas", len(geojson["features"]))
    con_imagen = sum(tiene_imagen(feature) for feature in geojson["features"])
    st.sidebar.caption(f"{con_imagen} registros tienen al menos una imagen enlazada.")
    if años:
        st.sidebar.caption(f"Años registrados en la capa: {', '.join(años)}")

    mapa = crear_mapa(geojson, vista)
    st_folium(mapa, width=1000, height=600, key="mapa_folium")


if __name__ == "__main__":
    main()
