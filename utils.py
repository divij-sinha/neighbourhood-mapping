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
        # tiles='https://stamen-tiles.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}.png',
        # attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.',
        
        tiles = "https://api.mapbox.com/styles/v1/divij-uc/clg184vco000401lhvagjhq3i/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZGl2aWotdWMiLCJhIjoiY2xnMTgyYWFvMTZ6MTNkbGF5NmlzN2t3diJ9.JRc_lHJ_6yomrmsTC2AY3A",
        attr = '© <a href="https://www.mapbox.com/about/maps/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> <strong><a href="https://www.mapbox.com/map-feedback/" target="_blank">Improve this map</a></strong>',

        height=450,
        width='100%',
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