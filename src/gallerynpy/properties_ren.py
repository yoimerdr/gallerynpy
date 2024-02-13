from resources_ren import Resource
from utils_ren import Singleton, images_path, normalize_color, join_path, or_default

"""renpy
init -1 python in gallerynpy:
"""
from store import ui, config, Solid, persistent


def width_ratio(ratio: float) -> int:
    return int(config.screen_width * ratio)


class Properties(Singleton):

    def __init__(self):
        self.__not_found = None
        self.__play_hover = None
        self.__play_idle = None
        self.__idle = None
        self.__locked = None
        self.__menu = None
        self.__menu_bg = None
        self.__navigation_background = None
        self.__version = "2.0"

        self.force_loader = False
        self.not_found = images_path("not_found.png")
        self.play_hover = images_path("play_hover_overlay.png")
        self.play_idle = images_path("play_idle_overlay.png")
        self.idle = images_path("idle_overlay.png")
        self.locked = images_path("locked.png")
        self.menu_bg = Solid("#fff5")
        self.menu = images_path("background_overlay.png")

        self.thumbnails_folder = images_path("gallerynpy", "thumbnails", from_renpy=True)

        self.font_size = 20
        self.font = join_path("gallerynpy", "fonts", "JetBrainsMono-Bold.ttf", for_renpy=True)

        self.color = "#fff"
        self.hover_color = "#99ccff"
        self.selected_color = "#99ccff"
        self.insensitive_color = "#ffffff99"

        # item properties
        self.spacing = width_ratio(0.0078125)
        self.item_xspacing = self.spacing

        self.sort_slides = False
        self.rescale_images = True
        self.with_speed = persistent.gallerynpy_with_speed
        self.animation_speed = persistent.gallerynpy_animation_speed

        self.navigation_position = "l"
        self.navigation_xsize = width_ratio(0.21875)
        self.navigation_yalign = 1.0
        self.navigation_background = Solid("#0005")

        self.navigation_slides_ysize = width_ratio(0.09)

        self.navigation_slides_bar_xpos = 0
        self.navigation_slides_bar_xsize = width_ratio(0.010416)
        self.navigation_slides_bar_position = "r"

        self.navigation_spacing = width_ratio(0.00390625)
        self.navigation_slides_adjustment = ui.adjustment()

    def __set_resource_attribute(self, value: Resource, displayable):
        if value is None:
            return Resource(displayable, self.force_loader)
        value.resource = displayable
        return value

    @property
    def video_thumbnail_extensions(self):
        return tuple('_thumbnail.' + item for item in ['jpg', 'png'])

    @property
    def common_slides(self):
        return "videos", "animations", "images"

    @property
    def not_found(self) -> Resource:
        return self.__not_found

    @not_found.setter
    def not_found(self, displayable):
        self.__not_found = self.__set_resource_attribute(self.__not_found, displayable)

    @property
    def play_hover(self) -> Resource:
        return self.__play_hover

    @play_hover.setter
    def play_hover(self, displayable):
        self.__play_hover = self.__set_resource_attribute(self.__play_hover, displayable)

    @property
    def play_idle(self) -> Resource:
        return self.__play_idle

    @play_idle.setter
    def play_idle(self, displayable):
        self.__play_idle = self.__set_resource_attribute(self.__play_idle, displayable)

    @property
    def idle(self) -> Resource:
        return self.__idle

    @idle.setter
    def idle(self, displayable):
        self.__idle = self.__set_resource_attribute(self.__idle, displayable)

    @property
    def locked(self) -> Resource:
        return self.__locked

    @locked.setter
    def locked(self, displayable):
        self.__locked = self.__set_resource_attribute(self.__locked, displayable)

    @property
    def version(self):
        return self.__version

    @property
    def thumbnails_folder(self):
        return self.__thumbnails_folder

    @thumbnails_folder.setter
    def thumbnails_folder(self, folder: str):
        self.__thumbnails_folder = str(folder)

    @property
    def font_size(self):
        return self.__font_size

    @font_size.setter
    def font_size(self, size: int):
        self.__font_size = int(size)

    @property
    def font(self):
        return self.__font

    @font.setter
    def font(self, font: str):
        self.__font = str(font)

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color: str):
        self.__color = normalize_color(color)

    @property
    def hover_color(self):
        return self.__hover_color

    @hover_color.setter
    def hover_color(self, color: str):
        self.__hover_color = normalize_color(color)

    @property
    def selected_color(self):
        return self.__selected_color

    @selected_color.setter
    def selected_color(self, color: str):
        self.__selected_color = normalize_color(color)

    @property
    def navigation_background(self):
        return self.__navigation_background

    @navigation_background.setter
    def navigation_background(self, displayable):
        self.__navigation_background = self.__set_resource_attribute(self.__navigation_background, displayable)

    @property
    def menu_bg(self) -> Resource:
        return self.__menu_bg

    @menu_bg.setter
    def menu_bg(self, displayable):
        self.__menu_bg = self.__set_resource_attribute(self.__menu_bg, displayable)

    @property
    def menu(self) -> Resource:
        return self.__menu

    @menu.setter
    def menu(self, displayable):
        self.__menu = self.__set_resource_attribute(self.__menu, displayable)

    @property
    def navigation_position(self):
        return self.__navigation_position

    @navigation_position.setter
    def navigation_position(self, position: str):
        position = str(position).lower()
        if position not in ("l", "r"):
            position = "r"
        self.__navigation_position = position

    @property
    def navigation_slides_bar_position(self):
        return self.__navigation_slides_bar_position

    @navigation_slides_bar_position.setter
    def navigation_slides_bar_position(self, position: str):
        position = str(position).lower()
        if position not in ("l", "r"):
            position = "r"
        self.__navigation_slides_bar_position = position

    @property
    def navigation_yalign(self):
        return self.__navigation_yalign

    @navigation_yalign.setter
    def navigation_yalign(self, yalign: float):
        yalign = float(yalign)
        if yalign < 0 or yalign > 1:
            yalign = 1.0
        self.__navigation_yalign = yalign

    @property
    def spacing(self):
        return self.__spacing

    @spacing.setter
    def spacing(self, spacing: int):
        spacing = max(int(spacing), 0)
        self.__spacing = spacing

    @property
    def item_xspacing(self):
        return self.__item_xspacing

    @item_xspacing.setter
    def item_xspacing(self, xspacing: int):
        xspacing = max(int(xspacing), 0)
        self.__item_xspacing = xspacing

    @property
    def with_speed(self):
        return self.__with_speed

    @with_speed.setter
    def with_speed(self, value: bool | None):
        if value is None:
            value = False
        self.__with_speed = value
        persistent.gallerynpy_with_speed = False

    @property
    def animation_speed(self):
        return self.__animation_speed

    @animation_speed.setter
    def animation_speed(self, value: int):
        value = max(int(or_default(value, 1)), 1)
        self.__animation_speed = value
        persistent.gallerynpy_animation_speed = True

    @property
    def force_loader(self):
        return self.__force_loader

    @force_loader.setter
    def force_loader(self, value: bool):
        self.__force_loader = or_default(value, False)

    @property
    def navigation_xsize(self):
        return self.__navigation_xsize

    @navigation_xsize.setter
    def navigation_xsize(self, xsize: int):
        xsize = max(int(xsize), 80)
        self.__navigation_xsize = xsize

    @property
    def navigation_spacing(self):
        return self.__navigation_spacing

    @navigation_spacing.setter
    def navigation_spacing(self, spacing: int):
        spacing = max(int(spacing), 0)
        self.__navigation_spacing = spacing

    @property
    def navigation_slides_ysize(self):
        return self.__navigation_slides_ysize

    @navigation_slides_ysize.setter
    def navigation_slides_ysize(self, ysize: int):
        ysize = max(int(ysize), 40)
        self.__navigation_slides_ysize = ysize

    @property
    def navigation_slides_bar_xpos(self):
        return self.__navigation_slides_bar_xpos

    @navigation_slides_bar_xpos.setter
    def navigation_slides_bar_xpos(self, xpos: int):
        xpos = max(int(xpos), 0)
        self.__navigation_slides_bar_xpos = xpos

    @property
    def navigation_slides_bar_xsize(self):
        return self.__navigation_slides_bar_xsize

    @navigation_slides_bar_xsize.setter
    def navigation_slides_bar_xsize(self, xsize: int):
        xsize = max(int(xsize), 5)
        self.__navigation_slides_bar_xsize = xsize
