"""
Test VectorTileLayer
---------------
"""

import json

import folium
from folium.utilities import normalize

from folium_vectortilelayer import VectorTileLayer


def test_vectortilelayer() -> None:
    m = folium.Map(location=(30, 20), zoom_start=4)
    url = "https://free.tilehosting.com/data/v3/{z}/{x}/{y}.pbf?token=my_token"
    vc = VectorTileLayer(url, "test").add_to(m)
    out = normalize(m._parent.render())

    expected = normalize(VectorTileLayer._template.render(this=vc))
    assert expected in out

    script = f'<script src="{VectorTileLayer.default_js[0][1]}"></script>'
    assert script in out
    assert url in out
    assert "VectorTileLayer.default" in out


def test_vectortilelayer_str_options() -> None:
    m = folium.Map(location=(30, 20), zoom_start=4)
    url = "https://free.tilehosting.com/data/v3/{z}/{x}/{y}.pbf?token=my_token"
    options = """{
        "layers": ["all"],
        "vectorTileLayerStyles": {
            "all": {
                "fill": true,
                "weight": 1,
                "fillColor": "green",
                "color": "black",
                "fillOpacity": 0.6,
                "opacity": 0.6
                }
            }
        }"""

    vc = VectorTileLayer(url, "test", options)
    m.add_child(vc)

    dict_options = json.loads(options)

    out = normalize(m._parent.render())
    script = f'<script src="{VectorTileLayer.default_js[0][1]}"></script>'

    assert script in out
    assert "VectorTileLayer.default" in out

    for k, v in dict_options["vectorTileLayerStyles"]["all"].items():
        # if type(v) == bool:
        if isinstance(v, bool):
            assert f'"{k}": {str(v).lower()}' in out
            continue
        if isinstance(v, str):
            assert f'"{k}": "{v}"' in out
            continue

        assert f'"{k}": {v}' in out


def test_vectortilelayer_dict_options() -> None:
    m = folium.Map(location=(30, 20), zoom_start=4)
    url = "https://free.tilehosting.com/data/v3/{z}/{x}/{y}.pbf?token=my_token"
    options = {
        "layers": ["all"],
        "vectorTileLayerStyles": {
            "all": {
                "fill": True,
                "weight": 1,
                "fillColor": "grey",
                "color": "purple",
                "fillOpacity": 0.3,
                "opacity": 0.6,
            }
        },
    }

    vc = VectorTileLayer(url, "test", options)
    m.add_child(vc)

    out = normalize(m._parent.render())
    script = f'<script src="{VectorTileLayer.default_js[0][1]}"></script>'

    assert script in out
    assert url in out
    assert "VectorTileLayer.default" in out

    for k, v in options["vectorTileLayerStyles"]["all"].items():  # type: ignore[index]
        if isinstance(v, bool):
            assert f'"{k}": {str(v).lower()}' in out
            continue
        if isinstance(v, str):
            assert f'"{k}": "{v}"' in out
            continue

        assert f'"{k}": {v}' in out
