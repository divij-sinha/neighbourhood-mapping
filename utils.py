import geojson
import folium
from folium.plugins import Draw
import urllib.parse
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

def get_geojson(input_str: str) -> dict:
    parsed_str = urllib.parse.unquote(input_str)
    if parsed_str.startswith("data:text/json;charset=utf-8,"):
        out_str = parsed_str.replace("data:text/json;charset=utf-8,","")
        return geojson.loads(out_str)
    return None

def get_neighborhood_list() -> list:
    df = pd.read_csv("app/data/neighborhoods233.csv")
    return df["name"].sort_values().to_list()

def get_map_comps(loc: tuple, zoom: int, draw_options: dict) -> tuple:
    m = folium.Map(
        location = loc,
        zoom_start = zoom,        
        tiles = f"https://api.mapbox.com/styles/v1/divij-uc/clg184vco000401lhvagjhq3i/tiles/256/{{z}}/{{x}}/{{y}}@2x?access_token={os.environ['ACCESS_TOKEN']}",
        attr = '© <a href="https://www.mapbox.com/about/maps/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> <strong><a href="https://www.mapbox.com/map-feedback/" target="_blank">Improve this map</a></strong>',

        height='100%',
        width='100%',
        tap = False,
        tapTolerance = 50,
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

    header = header.replace('    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css"/>', "")
    return header, body_html, script