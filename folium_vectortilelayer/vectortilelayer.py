from typing import Optional, Union

from folium.elements import JSCSSMixin
from folium.map import Layer
from jinja2 import Template


class VectorTileLayer(JSCSSMixin, Layer):
    """
    Add vector tile layers based on https://gitlab.com/jkuebart/Leaflet.VectorTileLayer

    Parameters
    ----------
    url: url to tile provider
        e.g. https://free-{s}.tilehosting.com/data/v3/{z}/{x}/{y}.pbf?token={token}
    options: dict or str, VectorTileLayer options
        see: https://gitlab.com/jkuebart/Leaflet.VectorTileLayer#layer-options

        // A function that will be passed a vector-tile feature, the layer
        // name, the number of SVG coordinate units per vector-tile unit
        // and the feature's style object to create each feature layer.
        featureToLayer, // default undefined

        // A function that will be used to decide whether to include a
        // feature or not. If specified, it will be passed the vector-tile
        // feature, the layer name and the zoom level. The default is to
        // include all features.
        filter, // default undefined

        // A function that receives a list of vector-tile layer names and
        // the zoom level and returns the names in the order in which they
        // should be rendered, from bottom to top. The default is to render
        // all layers as they appear in the tile.
        layerOrder, // default undefined

        // An array of vector-tile layer names from bottom to top. Layers
        // that are missing from this list will not be rendered. The
        // default is to render all layers as they appear in the tile.
        layers, // default undefined

        // minimum and maximum boundary of tiles provided by the source
        minDetailZoom, // default undefined
        maxDetailZoom, // default undefined

        // zoom range of the map
        // if minZoom < minDetailZoom, features in minDetailZoom are
        // used until minZoom
        minZoom,
        // if maxZoom > maxDetailZoom, features in maxDetailZoom are
        // used until maxZoom
        maxZoom,

        // Styling options.
        style, // default undefined

        // This works like the same option for `Leaflet.VectorGrid`.
        // Ignored if style is specified.
        vectorTileLayerStyles, // default undefined


    For convenience you can pass VectorTileLayer options as python dictionary or string.
    Strings allow plan JavaScript to be passed, therefor allow for conditional styling (see examples).

    Every layer inside the tile layer has to be styled separately.

    Examples
    --------

    Options as dict:

    >>> m = folium.Map()
    >>> url = "https://free-{s}.tilehosting.com/data/v3/{z}/{x}/{y}.pbf?token={token}"
    >>> options = {
    ...     "token": "af6P2G9dztAt1F75x7KYt0Hx2DJR052G",
    ...     "layers": ["a_layer", "another_layer"],
    ...     "vectorTileLayerStyles": {
    ...         "layer_name_one": {
    ...             "fill": True,
    ...             "weight": 1,
    ...             "fillColor": 'green',
    ...             "color": 'black',
    ...             "fillOpacity":0.6,
    ...             "opacity":0.6
    ...         },
    ...         "layer_name_two": {
    ...             "fill": True,
    ...             "weight": 1,
    ...             "fillColor": 'red',
    ...             "color": 'black',
    ...             "fillOpacity":0.6,
    ...             "opacity":0.6
    ...             }
    ...         }
    ...     }

    >>> VectorTileLayer(url,"layer_name",options).add_to(m)

    Options as string allows to pass functions

    >>> m = folium.Map()
    >>> url = "https://free-{s}.tilehosting.com/data/v3/{z}/{x}/{y}.pbf?token={token}"
    >>> options = '''{
    ... "token": "af6P2G9dztAt1F75x7KYt0Hx2DJR052G",
    ... "layers": ["a_layer", "another_layer"],
    ... "vectorTileLayerStyles": {
    ...     all: function(f) {
    ...         if (f.type === 'parks') {
    ...             return {
    ...                 "fill": true,
    ...                 "weight": 1,
    ...                 "fillColor": 'green',
    ...                 "color": 'black',
    ...                 "fillOpacity":0.6,
    ...                 "opacity":0.6
    ...             };
    ...         }
    ...         if (f.type === 'water') {
    ...             return {
    ...                 "fill": true,
    ...                 "weight": 1,
    ...                 "fillColor": 'purple',
    ...                 "color": 'black',
    ...                 "fillOpacity":0.6,
    ...                 "opacity":0.6
    ...             };
    ...         }
    ...     }
    ... }
    }'''

    >>> VectorTileLayer(url,"layer_name",options).add_to(m)


    For more info, see: https://gitlab.com/jkuebart/Leaflet.VectorTileLayer/-/tree/v0.11.0.
    """

    _template = Template(
        """
            {% macro script(this, kwargs) -%}
            var {{ this.get_name() }} = VectorTileLayer.default(
                "{{ this.url }}",
                {% if this.options is defined %}
                {{ this.options if this.options is string else this.options|tojson }})
                .addTo({{ this._parent.get_name() }});
                {% else %}
                {{ this.options }}).addTo({{ this._parent.get_name() }});
            {% endif %}
            {%- endmacro %}
            """
    )  # noqa

    default_js = [
        (
            "VectorTileLayer",
            "https://unpkg.com/leaflet-vector-tile-layer@latest/dist/VectorTileLayer.umd.js",
        )
    ]

    def __init__(
        self,
        url: str,
        name: Optional[str] = None,
        options: Union[str, dict, None] = None,
        overlay: bool = True,
        control: bool = True,
        show: bool = True,
    ):
        super(VectorTileLayer, self).__init__(
            name=name, overlay=overlay, show=show, control=control
        )
        if options is not None:
            self.options = options

        self.url = url
        self._name = "VectorTileLayer"
