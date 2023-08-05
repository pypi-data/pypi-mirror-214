import json
import json5

from django import forms
from django.utils.translation import gettext_lazy as _

from django.forms.fields import CharField
from django.forms import HiddenInput, Media
from django.utils.functional import cached_property

from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.core.telepath import register
from wagtail.blocks.field_block import FieldBlockAdapter
from wagtail.core.blocks import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    TextBlock,
    StructBlock,
    StreamBlock,
    URLBlock,
    FieldBlock,
)

from .widgets import (
    JsonEditorField,
    MapCompositionSelect,
    MapProjectionSelect
)


class MapToolsBlock(FieldBlock):
    class Meta:
        default = json.dumps(
            {
                "panelsEnabled": {
                    "composition_browser": True,
                    "toolbar": False,
                    "mobile_settings": False,
                    "draw": False,
                    "datasource_selector": True,
                    "layermanager": True,
                    "legend": True,
                    "info": True,
                    "print": False,
                    "routing": False,
                    "saveMap": False,
                    "language": True,
                    "permalink": False,
                    "feature_crossfilter": False,
                    "feature_table": False,
                    "compositionLoadingProgress": True,
                    "tracking": False,
                    "mapSwipe": True,
                },
                "componentsEnabled": {
                    "guiOverlay": True,
                    "sidebar": True,
                    "toolbar": False,
                    "drawToolbar": False,
                    "searchToolbar": False,
                    "measureToolbar": False,
                    "geolocationButton": True,
                    "defaultViewButton": True,
                    "mapControls": True,
                    "basemapGallery": True,
                    "mapSwipe": False,
                },
                "sidebarClosed": True,
            }
        )

    def __init__(self, required=True, help_text=None, **kwargs):
        self.field_options = {
            "required": required,
            "help_text": help_text,
        }
        super(MapToolsBlock, self).__init__(**kwargs)

    @cached_property
    def field(self):
        field_kwargs = {"widget": JsonEditorField()}
        field_kwargs.update(self.field_options)
        return CharField(**field_kwargs)

    # Tricky part here
    # We strip JSON object from editor to get plain JS objects used in template as map settings
    def value_from_form(self, value):
        return super(MapToolsBlock, self).value_from_form(
            value.replace('"', "").strip("{}")
        )

    # And the we need to convert these JS objects back to JSON so editor can work with it
    def value_for_form(self, value):
        tmp = ""
        if value != self.get_default():
            tmp = json.dumps(json5.loads("{" + value + "}"))
        else:
            tmp = value

        return super(MapToolsBlock, self).value_for_form(tmp)


class WmsLayersBlock(FieldBlock):
    class Meta:
        label = None
        required = False

    def __init__(self, **kwargs):
        self.field_options = kwargs
        super(WmsLayersBlock, self).__init__(**kwargs)

    @cached_property
    def field(self):
        field_kwargs = {"widget": HiddenInput()}
        field_kwargs.update(self.field_options)
        return CharField(**field_kwargs)

    def value_for_form(self, value):
        tmp = super().value_for_form(value)

        if tmp:
            tmp = json.dumps(tmp.split(","))

        return tmp

    def value_from_form(self, value):
        tmp = super().value_from_form(value)

        if tmp:
            tmp = ",".join(json.loads(tmp))

        return tmp


class WmsSourceBlockAdapter(StructBlockAdapter):

    js_constructor = "hslayers.blocks.WmsSourceBlock"

    def js_args(self, block):
        custom_args = {}
        args = super().js_args(block)

        custom_args["loadButtonIdPostfix"] = block.LOAD_BUTTON_ID_POSTFIX

        args.append(custom_args)
        return args

    @cached_property
    def media(self):
        structblock_media = super().media

        return Media(
            js=structblock_media._js + ["hslayers/js/wms-source-block.js"],
            css={"all": ("hslayers/css/wms-source-block.css",)},
        )


class WmsSourceBlock(StructBlock):
    LOAD_BUTTON_ID_POSTFIX = "-load-button"

    url = URLBlock(label="Source URL")
    layers = WmsLayersBlock()

    class Meta:
        form_template = "hslayers/block_forms/wms_source.html"
        template = "hslayers/wms_source_block.html"


register(WmsSourceBlockAdapter(), WmsSourceBlock)


class VectorSourceBlock(StructBlock):
    geoJson = TextBlock(label="Source GeoJSON")
    sld = TextBlock(label="SLD styling", required=False)
    actions = TextBlock(label="Map actions", required=False)

    class Meta:
        template = "hslayers/vector_source_block.html"


class LayerSourceSelectorBlock(StreamBlock):
    wms = WmsSourceBlock(label="WMS")
    vector = VectorSourceBlock(label="Vector")

    class Meta:
        min_num = 1
        max_num = 1


class LayerBlock(StructBlock):
    title = CharBlock(label="Title")
    visible = BooleanBlock(label="Visible", required=False, default=True)
    base = BooleanBlock(lable="Base", required=False)
    removable = BooleanBlock(label="Removable", required=False)
    tiled = BooleanBlock(label="Tiled", required=False, default=True)
    swipe_side = ChoiceBlock(
        choices=[
            ("left", "Left"),
            ("right", "Right"),
        ],
        required=False        
    )

    source = LayerSourceSelectorBlock()

    class Meta:
        icon = "image"
        template = "hslayers/layer_block.html"


class MapLayersBlock(StreamBlock):
    layer = LayerBlock()

    class Meta:
        template = "hslayers/map_layers_block.html"


class MapProjectionAdapter(FieldBlockAdapter):
    js_constructor = "hslayers.blocks.MapProjectionBlock"

    class Media:
        js = [
            "https://cdnjs.cloudflare.com/ajax/libs/slim-select/1.27.1/slimselect.min.js",
            "hslayers/js/map-projection-select.js",
        ]
        css = {
            "all": [
                "https://cdnjs.cloudflare.com/ajax/libs/slim-select/1.27.1/slimselect.min.css",
                "hslayers/css/map-composition-select.css",
            ]
        }


class MapProjectionBlock(FieldBlock):
    def __init__(self, required=True, help_text=None, validators=(), **kwargs):
        self.field_options = {
            "required": required,
            "help_text": help_text,
            "validators": validators,
        }
        super().__init__(**kwargs)

    @cached_property
    def field(self):
        field_kwargs = {"widget": MapProjectionSelect()}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

register(MapProjectionAdapter(), MapProjectionBlock)


class HsLayersAdvSettings(StructBlock):
    """
    Advanced settings for map widgets
    """

    projection = MapProjectionBlock(required=False, label="Map projection", help_text="Select map projection from the EPSG repository.")
    map_style = CharBlock(
        required=False,
        label="Map block HTML style",
        help_text="display: block; height: 500px;",
        default="display: block; height: 100vh;"
    )
    layers = MapLayersBlock(required=False, help_text="Add custom layers to map")
    hsl_tools = MapToolsBlock(
        required=False, label="Map tools", help_text="Choose which panesl enable in map"
    )
    datasources = TextBlock(required=False, label="Data connections", rows=15)

    class Meta:
        form_template = "wagtailadmin/block_forms/base_block_settings_struct.html"
        label = _("Advanced Settings")


class MapCompositionAdapter(FieldBlockAdapter):
    js_constructor = "hslayers.blocks.MapCompositionBlock"

    class Media:
        js = [
            "https://cdnjs.cloudflare.com/ajax/libs/slim-select/1.27.1/slimselect.min.js",
            "hslayers/js/map-composition-select.js",
        ]
        css = {
            "all": [
                "https://cdnjs.cloudflare.com/ajax/libs/slim-select/1.27.1/slimselect.min.css",
                "hslayers/css/map-composition-select.css",
            ]
        }


class MapCompositionBlock(FieldBlock):
    def __init__(self, required=True, help_text=None, validators=(), **kwargs):
        self.field_options = {
            "required": required,
            "help_text": help_text,
            "validators": validators,
        }
        super().__init__(**kwargs)

    @cached_property
    def field(self):
        field_kwargs = {"widget": MapCompositionSelect()}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

class MapBlock(StructBlock):
    class Meta:
        icon = "site"
        label = "HSLayers Map"
        template = "map_block.html"

    advsettings_class = HsLayersAdvSettings

    def __init__(self, local_blocks=None, **kwargs):
        """
        Construct and inject settings block, then initialize normally.
        """

        if not local_blocks:
            local_blocks = ()

        # comma at the end must be there, error occurs otherwise!!!
        local_blocks += (("settings", self.advsettings_class()),)

        super().__init__(local_blocks, **kwargs)

    # def get_context(self, value, parent_context=None):
    #     context = super().get_context(value, parent_context=parent_context)
    #     context['test'] = str(value['dynamic_links']).replace("'", '"')
    #     return context

    # id = CharBlock(required=True, label="ID")

    composition_url = MapCompositionBlock(
        required=False,
        label="Map composition",
        help_text="Select local composition by its title or enter URL of any other map and add it with the plus button",
    )
    map_center = CharBlock(
        required=False,
        label="Map center",
        help_text="Default map center in WGS (Lat, Lon), eg. 17.474129, 52.574",
    )
    map_zoom = CharBlock(
        required=False,
        label="Default map zoom­",
        help_text="1: World, 5: Continents, 10: Cities, 15: Streets, 20: Buildings",
    )
    zoom_with_ctrl = BooleanBlock(required=False, label="Zoom with Ctrl")


register(MapCompositionAdapter(), MapCompositionBlock)



class ClimaMapBlock(StructBlock):
    class Meta:
        icon = "site"
        label = "Agro Clima"
        template = "clima_map_block.html"
