import random
import folium
from typing import List

def create_world_map(data : List):
    world_map = folium.Map(location=[20, 0], zoom_start=2)

    counter = 10
    for attack in data:
        location = attack.get("location", None)
        if location:

            latitude = location.get("lat", None) or location.get("latitude")
            longitude = location.get("lon", None) or location.get("longitude")

            lat = latitude + (0.001 * counter * random.randint(-1, 1))
            lon = longitude + (0.001 * counter * random.randint(-1, 1))
            popup_text = "<br/>".join(
                [f"<h2>{k}: {v}</h3>" for k, v in attack.items() if isinstance(v, (int, str, float))] +
                [f"<h2>{k}: {'<br/>'.join(list(filter(lambda s: isinstance(s, str), v)))} </h2>" for k, v in attack.items() if isinstance(v, list)]
            )

            pup = folium.Popup(popup_text, max_width=300)
            marker = folium.Marker([lat, lon], popup=pup)
            marker.add_to(world_map)
            counter += 10

    return world_map._repr_html_()

