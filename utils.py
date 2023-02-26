import geojson
import folium
from folium.plugins import Draw
import urllib.parse


def get_geojson(input_str: str) -> dict:
    parsed_str = urllib.parse.unquote(input_str)
    if parsed_str.startswith("data:text/json;charset=utf-8,"):
        out_str = parsed_str.replace("data:text/json;charset=utf-8,","")
        return geojson.loads(out_str)
    return None


def get_map_comps(loc: tuple, zoom: int, draw_options: dict) -> tuple:
    m = folium.Map(
        location = loc,
        zoom_start = zoom,
#        tiles = "CartoDB", attr = "https://carto.com"
    )
    Draw(
     position="topleft",
     draw_options=draw_options,
     show_geometry_on_click=False
    ).add_to(m)

    m.get_root().render()
    header = m.get_root().header.render()
    body_html = m.get_root().html.render()
    script = m.get_root().script.render()

    return header, body_html, script