<br />
<p align="center">
  <h3 align="center">Folium-VectorTileLayer</h3>

  <p align="center">
    VectorTileLayer plugin for Folium
    <br />
    <a href="https://github.com/iwpnd/folium-vectortilelayer/issues">Report Bug</a>
    ·
    <a href="https://github.com/iwpnd/folium-vectortilelayer/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

Follow up on [folium-vectorgrid](https://github.com/iwpnd/folium-vectorgrid) that wraps
[Leaflet.VectorTileLayer](https://gitlab.com/jkuebart/Leaflet.VectorTileLayer) to render
Mapbox vector tiles in folium maps.

Other than [Leaflet.VectorGrid](https://github.com/Leaflet/Leaflet.VectorGrid/), [Leaflet.VectorTileLayer](https://gitlab.com/jkuebart/Leaflet.VectorTileLayer) allows
to "overzoom" and "underzoom".
Even if the tiling provider only provides map tiles for zoom level 5 through 12,
[Leaflet.VectorTileLayer](https://gitlab.com/jkuebart/Leaflet.VectorTileLayer) utilizes
data from these upper and lower bounds to render tiles beyond
zoom level 12 and 5 respectively.

### Built With

-   [folium](https://github.com/python-visualization/folium)
-   [Leaflet.VectorTileLayer](https://gitlab.com/jkuebart/Leaflet.VectorTileLayer)

<!-- GETTING STARTED -->

## Getting Started

### Prerequisite

Install [Poetry](https://python-poetry.org/docs/#installation).

### Installation

#### as dependency

```
poetry add git+https://github.com/iwpnd/folium-vectortilelayer.git
```

```
pip install folium-vectortilelayer
```

#### local development

1. Clone and install
    ```sh
    git clone https://github.com/iwpnd/folium-vectortilelayer.git
    poetry install
    ```
2. Test it!
    ```sh
    poe test  # or poetry run pytest .
    ```

## Usage

```python
from folium_vectortilelayer import VectorTileLayer
import folium

url = "https://free.tilehosting.com/data/v3/{z}/{x}/{y}.pbf?token=my_token"

m = folium.Map()
options = {
    "layers": ["my_layer"], # define layer to be shown
    # min zoom of your map,
    # if minZoom < minDetailZoom features in minDetailZoom level are used
    # for minDetailZoom to minZoom
    "minZoom": 8,
    # max zoom of your map,
    # if maxZoom > maxDetailZoom features in maxDetailZoom level are used
    # for maxDetailZoom to maxZoom
    "maxZoom": 18,
    # min zoom level provided by source
    "minDetailZoom": 10,
    # max zoom level provided by source
    "maxDetailZoom": 13,
    "vectorTileLayerStyles": {
        "my_layer":{
            "fill": True,
            "weight": 1,
            "fillColor": 'green',
            "color": 'black',
            "fillOpacity":0.6,
            "opacity":0.6
        },
    }
}

vc = VectorTileLayer(url, "folium_layer_name", options)
m.add_child(vc)
m
```

Or with conditional styling

```python
import folium
from folium_vectortilelayer import VectorTileLayer

m = folium.Map()
url = "https://free.tilehosting.com/data/v3/{z}/{x}/{y}.pbf?token=my_token"

options = '''{
  "layers": ["my_layer"],
  "vectorTileLayerStyles": {
    "my_layer": function(f) {
      if (f.type === 'parks') {
        return {
          "fill": true,
          "weight": 1,
          "fillColor": 'green',
          "color": 'black',
          "fillOpacity":0.6,
          "opacity":0.6
        };
      }

      if (f.type === 'water') {
        return {
          "fill": true,
          "weight": 1,
          "fillColor": 'purple',
          "color": 'black',
          "fillOpacity":0.6,
          "opacity":0.6
        };
      }
    }
  }
}'''

VectorTileLayer(url,"layer_name",options).add_to(m)
m
```

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Benjamin Ramser - [@imwithpanda](https://twitter.com/imwithpanda) - ahoi@iwpnd.pw  
Project Link: [https://github.com/iwpnd/folium-vector](https://github.com/iwpnd/folium-vectortilelayer)
