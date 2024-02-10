from resources_ren import Resource
from utils_ren import Singleton, images_path, normalize_color, join_path, or_default

"""renpy
init -1 python in gallerynpy:
"""
from store import ui, config, Solid, persistent


class Properties(Singleton):
    def __init__(self):
        self.__not_found = None
        self.__play_hover = None
        self.__play_idle = None
        self.__idle = None
        self.__locked = None
        self.__background = None
        self.__menu = None
        self.__menu_bg = None
        self.force_loader = False

        self.not_found = images_path("not_found.png")
        self.play_hover = images_path("play_hover_overlay.png")
        self.play_idle = images_path("play_idle_overlay.png")
        self.idle = images_path("idle_overlay.png")
        self.locked = images_path("locked.png")
        self.background = images_path("background_overlay.png")
        self.__version = "2.0"

        self.thumbnails_folder = images_path("gallerynpy", "thumbnails", from_renpy=True)
        self.font_size = 20
        self.font = join_path("gallerynpy", "fonts", "JetBrainsMono-Bold.ttf", for_renpy=True)
        self.color = "#fff"
        self.hover_color = "#99ccff"
        self.selected_color = "#99ccff"
        self.insensitive_color = "#ffffff99"

        # frame options properties
        self.frame_color = "#0005"
        self.frame_yalign = 0.992
        self.frame_xsize = 420
        self.frame_position = 'l'
        self.frame_xpos = 45
        self.frame_content_spacing = 10

        # item properties
        self.item_xspacing = 10

        self.spacing = 5
        self.navigation_xpos = 45

        self.pages_spacing = 0
        self.pages_ysize = 120
        self.adjustment = ui.adjustment()
        self.animation_slide = 'animations'
        self.show_pages_bar = False

        self.pages_bar_position = 'r'
        self.pages_bar_style = 'vscrollbar'  # No longer used
        self.pages_bar_xsize = 20
        if config.screen_width <= 1280:
            self.pages_bar_xsize = 15
        self.pages_bar_xpos = self.pages_bar_xsize * 2

        if config.screen_width <= 1280:
            self.pages_bar_xpos += 10

        self.menu_bg = Solid("#ffffff00")
        self.menu = Solid("#ffffff00")
        self.sort_slides = False
        self.rescale_images = True

        self.with_speed = persistent.gallerynpy_with_speed
        self.animation_speed = persistent.gallerynpy_animation_speed

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
        self.__not_found = self.__set_resource_attribute(self.__not_found,  displayable)

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
    def background(self) -> Resource:
        return self.__background

    @background.setter
    def background(self, displayable):
        self.__background = self.__set_resource_attribute(self.__background, displayable)

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
    def frame_color(self):
        return self.__frame_color

    @frame_color.setter
    def frame_color(self, color: str):
        self.__frame_color = normalize_color(color)

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
    def pages_bar_position(self):
        return self.__pages_bar_position

    @pages_bar_position.setter
    def pages_bar_position(self, position: str):
        position = str(position).lower()
        if position not in ("l", "r"):
            position = "r"
        self.__pages_bar_position = position

    @property
    def frame_position(self):
        return self.__frame_position

    @frame_position.setter
    def frame_position(self, position: str):
        position = str(position).lower()
        if position not in ("l", "r"):
            position = "r"
        self.__frame_position = position

    @property
    def frame_yalign(self):
        return self.__frame_yalign

    @frame_yalign.setter
    def frame_yalign(self, yalign: float):
        yalign = float(yalign)
        if yalign < 0 or yalign > 1:
            yalign = 0.90
        self.__frame_yalign = yalign

    @property
    def animation_slide(self):
        return self.__animation_slide

    @animation_slide.setter
    def animation_slide(self, name: str):
        self.__animation_slide = str(name)

    @property
    def item_xspacing(self):
        return self.__item_xspacing

    @item_xspacing.setter
    def item_xspacing(self, xspacing: int):
        xspacing = int(xspacing)
        if xspacing < 0:
            xspacing = 10
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
        value = int(or_default(value, 1))
        if value < 1:
            value = 1
        self.__animation_speed = value
        persistent.gallerynpy_animation_speed = True

    @property
    def force_loader(self):
        return self.__force_loader

    @force_loader.setter
    def force_loader(self, value: bool):
        self.__force_loader = or_default(value, False)

    def __getattribute__(self, item):
        return object.__getattribute__(self, item)
