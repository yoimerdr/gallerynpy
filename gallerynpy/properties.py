# Copyright © 2023-2024, Yoimer Davila. <https://github.com/yoimerdr/gallerynpy>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import gallerynpy

"""renpy
init -3 python in gallerynpy:
# docstring:1
The gallerynpy stored module.
from store import gallerynpy
"""

from store import ui, Solid, persistent


class Properties(gallerynpy.Singleton):
    """
    The gallerynpy properties.
    Stores values for use in the styles, screens and another gallerynpy methods.

    It inherits from Singleton, so there will be only one instance of it.
    """

    def __init__(self):
        self.__not_found = None
        self.__play_hover = None
        self.__play_idle = None
        self.__idle = None
        self.__locked = None
        self.__menu = None
        self.__menu_bg = None
        self.__navigation_background = None

        self.force_loader = False
        """
        If true, forces the `Resource` to load/validate when it is created. 
        Affects only instances created internally by gallerynpy.
        
        Default is False.
        """

        self.not_found = gallerynpy.images_path("not_found.png")
        self.play_hover = gallerynpy.images_path("play_hover.png")
        self.play_idle = gallerynpy.images_path("play_idle.png")
        self.idle = gallerynpy.images_path("idle.png")
        self.locked = gallerynpy.images_path("locked.png")
        self.menu_bg = Solid("#fff5")
        self.menu = gallerynpy.images_path("menu.png")

        self.thumbnails_folder = gallerynpy.images_path("gallerynpy", "thumbnails", from_renpy=True)

        self.font_size = 20
        self.font = gallerynpy.join_path("gallerynpy", "fonts", "JetBrainsMono-Bold.ttf", for_renpy=True)

        self.color = "#fff"
        self.hover_color = "#99ccff"
        self.selected_color = "#99ccff"
        self.insensitive_color = "#ffffff99"

        # item properties
        self.spacing = gallerynpy.width_ratio(0.0078125)
        self.item_xspacing = self.spacing

        self.sort_slides = False
        """
        If true, sorts the names (keys) of each slide/slider in the current slider before displaying them as options.
        
        Default is False.
        """
        self.keep_loaded = False
        """
        If true, the (displayables) elements of the gallery will be stored in the Gallery object. 
        Otherwise, when you exit the gallerynpy screen, the reference to the Gallery object will be removed (`del`) 
        to try to free up space, and it will be re-initialized when you return. 
        
        Default is False.
        """
        self.load_in_put = False

        self.rescale_images = True
        """
        If true, the images will be rescaled to the size of the game screen. 
        Trying to keep the original width / height ratio to avoid deformation.
        
        Default is True.
        """
        self.with_speed = persistent.gallerynpy_with_speed
        self.animation_speed = persistent.gallerynpy_animation_speed

        self.navigation_position = "l"
        self.navigation_xsize = gallerynpy.width_ratio(0.21875)
        self.navigation_yalign = 1.0
        self.navigation_background = Solid("#0005")

        self.navigation_slides_ysize = gallerynpy.width_ratio(0.09)

        self.navigation_slides_show_bar = False
        self.navigation_slides_bar_xpos = 0
        self.navigation_slides_bar_xsize = gallerynpy.width_ratio(0.010416)
        self.navigation_slides_bar_position = "r"

        self.navigation_spacing = gallerynpy.width_ratio(0.00390625)
        self.navigation_slides_adjustment = ui.adjustment()

    def __set_resource_attribute(self, value: gallerynpy.resources.Resource, displayable):
        if value is None:
            return gallerynpy.resources.Resource(displayable, self.force_loader)
        value.resource = displayable
        return value

    @property
    def video_thumbnail_extensions(self):
        """
        Gets the thumbnail extensions accepted for automatically loading video element extensions.
        e.g. `_thumbnail.jpg`.
        """
        return tuple('_thumbnail.' + item for item in ['jpg', 'png'])

    @property
    def not_found(self) -> gallerynpy.resources.Resource:
        """
        Gets the resource `not_found`.

        Used when a thumbnail has not been set for "VIDEO" or "ANIMATION" type items.
        """
        return self.__not_found

    @not_found.setter
    def not_found(self, displayable):
        """
        Sets the resource `not_found`
        :param displayable: The new resource for `not_found`
        """
        self.__not_found = self.__set_resource_attribute(self.__not_found, displayable)

    @property
    def play_hover(self) -> gallerynpy.resources.Resource:
        """
        Sets the resource `play_hover`.

        Used as hover displayable when is hover in `VIDEO` or `ANIMATION` type items.
        """
        return self.__play_hover

    @play_hover.setter
    def play_hover(self, displayable):
        """
        Sets the resource `play_hover`.
        :param displayable: The new resource for `play_hover`
        """
        self.__play_hover = self.__set_resource_attribute(self.__play_hover, displayable)

    @property
    def play_idle(self) -> gallerynpy.resources.Resource:
        """
        Gets the resource `play_idle`.

        Used as idle displayable in `VIDEO` or `ANIMATION` type items.
        """
        return self.__play_idle

    @play_idle.setter
    def play_idle(self, displayable):
        """
        Sets the resource `play_idle`.
        :param displayable: The new resource for `play_idle`
        """
        self.__play_idle = self.__set_resource_attribute(self.__play_idle, displayable)

    @property
    def idle(self) -> gallerynpy.resources.Resource:
        """
        Gets the resource `idle`.

        Used as idle displayable on `IMAGE` or `DISPLAYABLE` type items.
        """
        return self.__idle

    @idle.setter
    def idle(self, displayable):
        """
        Sets the resource `idle`.
        :param displayable: The new resource for `idle`
        """
        self.__idle = self.__set_resource_attribute(self.__idle, displayable)

    @property
    def locked(self) -> gallerynpy.resources.Resource:
        """
        Gets the resource `locked`.

        It is used as a thumbnail on items that have not met the unlock condition they have.
        """
        return self.__locked

    @locked.setter
    def locked(self, displayable):
        """
        Sets the resource `locked`.
        :param displayable: The new resource for `locked`
        """
        self.__locked = self.__set_resource_attribute(self.__locked, displayable)

    @property
    def version(self):
        """
        Gets the current version of Gallerynpy in string format.
        """
        return "2.0"

    @property
    def thumbnails_folder(self):
        """
        Gets the folder where video thumbnails are stored.

        This is where files for thumbnails like `videpath_thumbnail.jpg` will be searched.
        """
        return self.__thumbnails_folder

    @thumbnails_folder.setter
    def thumbnails_folder(self, folder: str):
        """
        Sets the folder where video thumbnails are stored.
        :param folder: The new folder path.
        """
        if folder is None:
            raise ValueError("Folder cannot be None")
        self.__thumbnails_folder = str(folder)

    @property
    def font_size(self):
        """
        Gets the font size.

        Used on styles for text.
        """
        return self.__font_size

    @font_size.setter
    def font_size(self, size: int):
        """
        Sets the font size.
        :param size: The new font size.
        """
        self.__font_size = int(size)

    @property
    def font(self):
        """
        Gets the filepath to the font.

        Used as on styles for text.
        """
        return self.__font

    @font.setter
    def font(self, font: str):
        """
        Sets the filepath to the font
        :param font: The new filepath to the font.
        """
        self.__font = str(font)

    @property
    def color(self):
        """
        Gets the primary color.

        Used on styles for text.
        """
        return self.__color

    @color.setter
    def color(self, color: str):
        """
        Sets the primary color.
        :param color: The new primary color. Must be in hexadecimal format.
        """
        self.__color = gallerynpy.normalize_color(color)

    @property
    def hover_color(self):
        """
        Gets the hover color.

        Used on styles for text.
        """
        return self.__hover_color

    @hover_color.setter
    def hover_color(self, color: str):
        """
        Sets the hover color.
        :param color: The new hover color. Must be in hexadecimal format.
        """
        self.__hover_color = gallerynpy.normalize_color(color)

    @property
    def selected_color(self):
        """
        Gets the selected color.

        Used on styles for text.
        """
        return self.__selected_color

    @selected_color.setter
    def selected_color(self, color: str):
        """
        Sets the selected color.
        :param color: The new hover color. Must be in hexadecimal format.
        """
        self.__selected_color = gallerynpy.normalize_color(color)

    @property
    def insensitive_color(self):
        """
        Gets the insensitive color.

        Used on styles for text.
        """
        return self.__insensitive_color

    @insensitive_color.setter
    def insensitive_color(self, color: str):
        """
        Sets the insensitive color.
        :param color: The new insensitive color. Must be in hexadecimal format.
        """
        self.__insensitive_color = gallerynpy.normalize_color(color)

    @property
    def navigation_background(self):
        """
        Gets the resource `navigation_background`.

        It is used as a displayable background for the navigation section.
        """
        return self.__navigation_background

    @navigation_background.setter
    def navigation_background(self, displayable):
        """
        Sets the resource `navigation_background`.
        :param displayable: The new resource for `navigation_background`
        """
        self.__navigation_background = self.__set_resource_attribute(self.__navigation_background, displayable)

    @property
    def menu_bg(self) -> gallerynpy.resources.Resource:
        """
        Gets the resource `menu_bg`.

        It is used as a displayable background for the main gallerynpy screen.
        """
        return self.__menu_bg

    @menu_bg.setter
    def menu_bg(self, displayable):
        """
        Sets the resource `menu_bg`.
        :param displayable: The new resource for `navigation_background`
        """
        self.__menu_bg = self.__set_resource_attribute(self.__menu_bg, displayable)

    @property
    def menu(self) -> gallerynpy.resources.Resource:
        """
        Gets the resource `menu`.

        It is used as a displayable for the main gallerynpy screen. It's added after `menu_bg`.
        """
        return self.__menu

    @menu.setter
    def menu(self, displayable):
        """
        Sets the resource `menu`.
        :param displayable: The new resource for `navigation_background`
        """
        self.__menu = self.__set_resource_attribute(self.__menu, displayable)

    @property
    def navigation_position(self):
        """
        Gets the position where the navigation section was located.
        """
        return self.__navigation_position

    @navigation_position.setter
    def navigation_position(self, position: str):
        """
        Sets the position where the navigation section will be located.
        :param position: The new position.
        """
        position = str(position).lower()
        if position not in ("l", "r"):
            position = "r"
        self.__navigation_position = position

    @property
    def navigation_slides_bar_position(self):
        """
        Gets the position where the navigation bar was located.
        """
        return self.__navigation_slides_bar_position

    @navigation_slides_bar_position.setter
    def navigation_slides_bar_position(self, position: str):
        """
        Sets the position where the navigation bar will be located.
        :param position: The new position.
        """
        position = str(position).lower()
        if position not in ("l", "r"):
            position = "r"
        self.__navigation_slides_bar_position = position

    @property
    def navigation_yalign(self):
        """
        Gets the yalgin value where the navigation was located.
        """
        return self.__navigation_yalign

    @navigation_yalign.setter
    def navigation_yalign(self, yalign: float):
        """
        Sets the yalgin value where the navigation will be located.
        :param yalign: The new yalign value. The min is 0 and max is 1.
        """
        yalign = float(yalign)
        if yalign < 0 or yalign > 1:
            yalign = 1.0
        self.__navigation_yalign = yalign

    @property
    def spacing(self):
        """
        Gets the spacing between the navigation section and the items section.
        """
        return self.__spacing

    @spacing.setter
    def spacing(self, spacing: int):
        """
        Sets the spacing between the navigation section and the items section.
        :param spacing: The new spacing value. The min is 0.
        """
        spacing = max(int(spacing), 0)
        self.__spacing = spacing

    @property
    def item_xspacing(self):
        """
        Gets the xspacing between each item in the items section.
        """
        return self.__item_xspacing

    @item_xspacing.setter
    def item_xspacing(self, xspacing: int):
        """
        Sets the xspacing between each item in the items section.
        :param xspacing: The new xspacing value. The min is 0.
        """
        xspacing = max(int(xspacing), 0)
        self.__item_xspacing = xspacing

    @property
    def with_speed(self):
        """
        Gets whether gallerynpy slides marked as animation one will display the screen with speed options
        """
        return self.__with_speed

    @with_speed.setter
    def with_speed(self, value: bool | None):
        """
        Sets whether gallerynpy slides marked as animation one will display the screen with speed options.

        It will also be saved in `persistent.gallerynpy_with_speed` variable.
        :param value: The new value.
        """
        if value is None:
            value = False
        self.__with_speed = value
        persistent.gallerynpy_with_speed = False

    @property
    def animation_speed(self):
        """
        Gets the current animation speed.
        """
        return self.__animation_speed

    @animation_speed.setter
    def animation_speed(self, value: int):
        """
        Sets the current animation speed.
        :param value: The new animation speed value. The min is 1.
        """
        value = max(int(gallerynpy.or_default(value, 1)), 1)
        self.__animation_speed = value
        persistent.gallerynpy_animation_speed = True

    @property
    def navigation_xsize(self):
        """
        Gets the current xsize (width) of the navigation section.
        """
        return self.__navigation_xsize

    @navigation_xsize.setter
    def navigation_xsize(self, xsize: int):
        """
        Sets the current xsize (width) of the navigation section.
        :param xsize: The new xsize value. The min is 80.
        """
        xsize = max(int(xsize), 80)
        self.__navigation_xsize = xsize

    @property
    def navigation_slides_ysize(self):
        """
        Gets the current ysize (height) of the button section (slides names) in the navigation section.
        """
        return self.__navigation_slides_ysize

    @navigation_slides_ysize.setter
    def navigation_slides_ysize(self, ysize: int):
        """
        Sets the current ysize (height) of the button section (slides names) in the navigation section.
        :param ysize: The new ysize value. The min is 40.
        """
        ysize = max(int(ysize), 40)
        self.__navigation_slides_ysize = ysize

    @property
    def navigation_slides_bar_xpos(self):
        """
        Gets the current xpos of the navigation bar in the navigation section.
        """
        return self.__navigation_slides_bar_xpos

    @navigation_slides_bar_xpos.setter
    def navigation_slides_bar_xpos(self, xpos: int):
        """
        Sets the current xpos of the navigation bar in the navigation section.
        :param xpos: The new xpos value. The min is 0.
        """
        xpos = max(int(xpos), 0)
        self.__navigation_slides_bar_xpos = xpos

    @property
    def navigation_slides_bar_xsize(self):
        """
        Gets the current xsize (width) of the navigation bar in the navigation section.
        """
        return self.__navigation_slides_bar_xsize

    @navigation_slides_bar_xsize.setter
    def navigation_slides_bar_xsize(self, xsize: int):
        """
        Sets the current xsize (width) of the navigation bar in the navigation section.
        :param xsize: The new xsize value. The min is 5.
        """
        xsize = max(int(xsize), 5)
        self.__navigation_slides_bar_xsize = xsize


properties: Properties | None = None
"""
The only instance for the Properties class. A reassignment is not recommended.
"""
