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
init -1 python in gallerynpy:
# docstring:1
The gallerynpy stored module.
from store import gallerynpy
"""
from store import Button, Function, Gallery, dissolve, Call, Play, Stop, Null, config, Return, NullAction


def init():
    """
    Initializes (or validates) important gallerynpy objects for proper operation.

    This method will be called automatically, but if it must be called, it must be done in a normal `init python` block
    or with a wait value greater than or equal to one (e.g. `init 1 python`), and it must be done before
    trying to access some gallerynpy methods.
    """
    if not isinstance(gallerynpy.db, gallerynpy.SizesDb):
        gallerynpy.db = gallerynpy.SizesDb("images.json", gallerynpy.join_path("gallerynpy", "db"))
    if not isinstance(gallerynpy.screen_size, gallerynpy.Size):
        gallerynpy.screen_size = gallerynpy.Size(config.screen_width, config.screen_height)
    if not isinstance(gallerynpy.properties, gallerynpy.Properties):
        gallerynpy.properties = gallerynpy.Properties()
    if not isinstance(gallerynpy.handler, gallerynpy.Handler):
        gallerynpy.handler = gallerynpy.Handler()


class Handler(gallerynpy.Singleton):
    """
    The gallerynpy handler.
    Handles the methods related to the gallery.

    It inherits from Singleton, so there will be only one instance of it.
    """

    def __init__(self):
        self.__start = 0
        self.__end = 0
        self.__rows = 0
        self.__cols = 0

        self.__thumbnail_size = None
        self.__gallery_released = False
        self.__gallery = Gallery()
        self.__gallery.transition = dissolve

        self.change_distribution(4, 4)
        self.__page = 0
        self.__tooltip = ""

        self.__sliders = gallerynpy.Slider("base")
        self.__current_slider = self.__sliders
        self.__current_name = ""
        self.__item_id = 0

    def __change_tooltip(self, tooltip: str):
        """
        Change tooltip current tooltip text.
        :param tooltip: The new tooltip text.
        """
        self.__tooltip = str(tooltip)

    def __add_to_gallery(self, item: gallerynpy.Item):
        """
        Adds the given item to the gallerynpy gallery
        :param item: The item to add to the gallery.
        """
        if not gallerynpy.is_item(item):
            return

        self.__gallery.button(item.name)
        if item.resource.is_image_type:
            image = item.resource.resource
            if gallerynpy.properties.rescale_images:
                image = item.resource.composite_to(gallerynpy.screen_size)
            self.__gallery.image(image)
        else:
            self.__gallery.image(item.resource.resource)
        if item.condition:
            self.__gallery.condition(item.condition)

    def __change_current_slider(self, name: str, slider: gallerynpy.Slider):
        """
        Changes the current slider to the one with the given name in the slider param
        :param name: The slider name. A key in the slider param.
        :param slider: The slider where the new slider is.
        :return: True if the current slider was changed, False otherwise
        """
        slider = slider[name]
        if gallerynpy.is_slider(slider):
            self.__current_slider = slider
            return True
        return False

    def __add_slide_to_gallery(self, slide: gallerynpy.Slide):
        """
        Adds all the items in the given slide to the gallerynpy gallery.
        :param slide: The slide with the items to add.
        """
        if not gallerynpy.is_slide(slide):
            return
        for item in slide:
            self.__add_to_gallery(item)

    def __slide_like_to_gallery(self, slider: gallerynpy.Slider | gallerynpy.Slide):
        """
        Adds all the items in the slide (or slider) to the gallerynpy gallery.

        This method could call itself recursively, so be aware of the possible RecursionError
        :param slider: The slide or slider with the items to add.
        """
        if gallerynpy.is_slider(slider):
            for (_, slide) in slider:
                if gallerynpy.is_slider(slide):
                    self.__slide_like_to_gallery(slide)
                else:
                    self.__add_slide_to_gallery(slide)

        else:
            self.__add_slide_to_gallery(slider)

    def __change_to_parent(self):
        """
        Changes the current slider to its parent if it has one.
        """
        self.__current_slider = self.__current_slider.parent
        if self.__current_slider is None:
            self.__current_slider = self.__sliders

        self.to_first_slide(gallerynpy.properties.sort_slides)

    def __init_gallery(self):
        """
        Initializes the gallerynpy gallery if it is necessary.
        """
        if not self.__gallery_released or gallerynpy.properties.keep_loaded:
            return

        self.__gallery = Gallery()
        self.__gallery.transition = dissolve
        self.__gallery_released = False
        if gallerynpy.properties.load_in_put:
            self.__slide_like_to_gallery(self.__sliders)

    def __release_gallery(self):
        """
        Releases (del) the gallerynpy gallery if it is necessary.
        :return:
        """
        if gallerynpy.properties.keep_loaded:
            return
        del self.__gallery
        self.__gallery_released = True

    @property
    def start(self):
        """
        Gets the starting index of the current page on the current slide.
        """
        return self.__start

    @property
    def end(self):
        """
        Gets the end index of the current page on the current slide.
        """
        return self.__end

    @property
    def thumbnail_size(self) -> gallerynpy.Size:
        """
        Gets the thumbnail size of the items.
        """
        return self.__thumbnail_size

    @property
    def columns(self):
        """
        Gets the maximum number of columns on each page of each slide.
        """
        return self.__cols

    @property
    def rows(self):
        """
        Gets the maximum number of rows on each page of each slide.
        """
        return self.__rows

    @property
    def max_per_page(self):
        """
        Gets the maximum number of items on each page of each slide.
        """
        return self.rows * self.columns

    @property
    def idle_res(self):
        """
        Gets the scaled idle resource of the gallerynpy gallery.
        """
        return self.scale_res(gallerynpy.properties.idle)

    @property
    def play_idle_res(self):
        """
        Gets the scaled play_idle resource of the gallerynpy gallery.
        """
        return self.scale_res(gallerynpy.properties.play_idle)

    @property
    def play_hover_res(self):
        """
        Gets the scaled play_hover resource of the gallerynpy gallery.
        """
        return self.scale_res(gallerynpy.properties.play_hover)

    @property
    def current_slides(self):
        """
        Gets all the names of the current slider items.
        """
        return self.__current_slider.slides

    @property
    def current_slide_name(self):
        """
        Gets the name of the currently selected slide.
        """
        return self.__current_name

    @property
    def tooltip(self):
        """
        Gets the current tooltip.
        """
        return self.__tooltip

    def __change_page(self, page: int):
        """
        Change the current page to the given one.
        :param page: The new page number.
        """
        self.__page = int(page)

    def change_distribution(self, columns: int = None, rows: int = None):
        """
        Changes the distribution on each page of each slide.
        :param columns: The number of columns in the page.
        :param rows: The number of rows in the page.
        """
        if columns is None:
            columns = self.columns
        if rows is None:
            rows = self.rows

        if rows == self.rows and columns == self.columns:
            return

        def get_max(value: int):
            return 4 if value < 0 else value

        columns = get_max(int(columns))
        rows = get_max(int(rows))

        if rows == self.rows and columns == self.columns:
            return

        self.__rows = rows
        self.__cols = columns

        properties = gallerynpy.properties
        target = max(columns, rows)
        spacing = gallerynpy.properties.item_xspacing * (target - 1)
        actual_width = config.screen_width - properties.navigation_xsize - properties.navigation_spacing - spacing
        width = actual_width / target

        new_size = gallerynpy.Size(width, width / gallerynpy.screen_size.aspect_ratio)
        if self.thumbnail_size is None:
            self.__thumbnail_size = new_size
        else:
            self.thumbnail_size.set(new_size)
        self.__gallery.locked_button = self.scale_res(properties.locked)

    def scale_res(self, resource: gallerynpy.resources.Resource):
        """
        Scales the given resource according to the current thumbnail size.
        :param resource: The resource to scale
        """
        if not gallerynpy.resources.is_resource(resource):
            resource = gallerynpy.resources.Resource(resource, gallerynpy.properties.force_loader)
        return resource.scale_to(self.thumbnail_size)

    def change_transition(self, transition):
        """
        Changes the current transition of the gallerynpy gallery.
        :param transition: The new transition.
        """
        self.__gallery.transition = transition

    def put_item(self, item: gallerynpy.Item, where: str, for_animation_slide: bool = False):
        """
        Puts the given item into the gallerynpy gallery.
        :param item: The item to put
        :param where: The name of the slide to put the item into
        :param for_animation_slide: If true and the slide with the given name has not yet been created,
            the slide is marked as one for animations.
        :raises ValueError: If the where param is empty or None.
        :raises TypeError: If the given item is not valid.
        """
        if where is None or not where:
            raise ValueError("Cannot put an item in a slide without a valid name")
        elif not gallerynpy.is_item(item):
            raise TypeError("The given item not is a gallerynpy.Item: {}".format(item))

        where = str(where)
        slide = self.__sliders[where]
        if slide is None:
            slide = gallerynpy.Slide(where, is_for_animations=for_animation_slide)
            self.__sliders.put(slide)

        slide.put(item)

    def create_item(self, resource, thumbnail=None, song: str = None, condition: str = None,
                    tooltip: str = None):
        """
        Creates an item with the given params.
        :param resource: The item resource
        :param thumbnail: The item custom thumbnail resource.
        :param song: A valid filepath for an audio that renpy can load.
        :param condition: The condition to unlock the item.
        :param tooltip: The tooltip text to display when the item is hovered.
        :return: The created item.

        :raises ValueError: If the given resource is None.
        """
        if resource is None:
            raise ValueError("Cannot create a item from none resource")

        item = gallerynpy.Item(
            name="gallerynpy-" + str(self.__item_id),
            resource=resource,
            size=self.thumbnail_size,
            song=song,
            condition=condition,
            tooltip=tooltip
        )
        item.thumbnail.set_custom(thumbnail)
        self.__item_id += 1
        return item

    def create_slider(self, name: str):
        """
        Create a slider with the given name and the base slider as its parent
        :param name: The slider name
        :return: The created slider
        """
        return self.__sliders.create_slider(name)

    def create_slide(self, name: str, for_animation=False):
        """
        Create a slide with the given name and the base slider as its parent.
        :param name: The slide name
        :param for_animation: Sets true if the slide will be marked as one for animations
        :return: The created slide
        """
        return self.__sliders.create_slide(name, for_animation)

    def put_slide_like(self, slide: gallerynpy.Slide | gallerynpy.Slider):
        """
        Adds the given slide or slider to the base slider and all its items to the gallerynpy gallery.
        :param slide: The slide or slider to add
        """
        self.__sliders.put(slide)

    def check_puts(self):
        """
        Adds all items in the base slider to the gallery if `gallerynpy.properties.load_in_put` is true.
        """
        if gallerynpy.properties.load_in_put:
            self.__slide_like_to_gallery(self.__sliders)

    def change_slide(self, name: str):
        """
        Changes the current slide or slider to one with the given name (key).
        :param name: The name of the slide, or slide, to change.
        """
        name = str(gallerynpy.or_default(name, ""))
        if name and name in self.current_slides:
            if self.__change_current_slider(name, self.__current_slider):
                self.to_first_slide(gallerynpy.properties.sort_slides)
            else:
                self.__current_name = name
            self.__page = 0

    def is_current_slide(self, name: str):
        """
        Checks if the given name is equal to the currently selected slide name.
        :param name: The name of the slide, or slide, to check.
        :return: True if the name is equal to the currently selected, False otherwise.
        """
        return self.current_slide_name == str(gallerynpy.or_default(name, ""))

    def is_current_for_animations(self):
        """
        Checks if the current slide is one for animations
        :return: True if the current slide is one for animations, False otherwise
        """
        slide: gallerynpy.Slide | None = self.__current_slider[self.__current_name]
        return gallerynpy.is_slide(slide) and slide.is_for_animations

    def make_item_button(self, item: gallerynpy.Item):
        """
        Creates a button to display the given item.
        :param item: The item to create its button.
        :return: The created button. If the item is not valid, a button with none action will be returned.
        """
        button = Button(action=None)
        if not gallerynpy.is_item(item) or item.resource.is_none_type:
            return button

        if not gallerynpy.properties.load_in_put:
            if not gallerynpy.properties.keep_loaded or item.name not in self.__gallery.buttons.keys():
                self.__add_to_gallery(item)

        hover_border = None
        if item.resource.is_image_type or item.resource.is_displayable_type:
            idle_border = self.idle_res
        else:
            idle_border = self.play_idle_res
            hover_border = self.play_hover_res

        button = self.__gallery.make_button(
            item.name, item.thumbnail.create(),
            idle_border=idle_border,
            hover_border=hover_border,
            xalign=0.5, yalign=0.5,
            hovered=Function(self.__change_tooltip, item.tooltip),
            unhovered=Function(self.__change_tooltip, "")
        )

        if not item.meets_condition:
            button.action = NullAction()
        elif item.resource.is_video_type:
            button.action = Call("gallerynpy_cinema", movie=item.resource.resource, song=item.song)
        else:
            if item.song and gallerynpy.is_loadable(item.song):
                button.action = [Play("music", item.song), button.action, Stop("music")]

        return button

    def make_current_button_at(self, index: int):
        """
        Creates a button to display the item at the given index of the current slide.
        :param index: The index of the item in the current slide
        :return: The created button. If the index is not valid, a button with none action will be returned.
        """
        item = self.current_item_at(index)
        if item is None or item.resource.is_none_type:
            return Button(action=None)
        return self.make_item_button(item)

    def to_first_slide(self, sort: bool = False):
        """
        Changes the selected slide name to the name of the first valid slide in the current slider.
        :param sort: If true, sorts slide names before the change.
        """
        names = self.current_slides
        if names:
            if sort:
                names.sort()

            for name in names:
                slide: gallerynpy.Slide | None = self.__current_slider[name]
                if gallerynpy.is_slide(slide) and not (gallerynpy.properties.with_speed and slide.is_for_animations):
                    self.change_slide(name)
                    return
            self.__current_name = ""

    def item_at(self, where: str, index: int) -> gallerynpy.Item | None:
        """
        Gets the item at the given index on the slide with the given name
        :param where: The slide name in the current slider
        :param index: The index where is the item.
        :return: The item at the given index. If the index is out of range or the object
            with the `where` name in the current slider not is a slide, return None
        """
        slide = self.__current_slider[where]
        if not gallerynpy.is_slide(slide):
            return None
        return slide[index]

    def current_item_at(self, index: int):
        """
        Gets the item at the given index on the current slide name.
        :param index: The index where is the item.
        :return: The item at the given index. If the index is out of range, return None.
        """
        return self.item_at(self.__current_name, index)

    def slide_size(self, name: str):
        """
        Gets the size of the slide or slider with the given name.
        :param name: The slide name in the current slider
        :return: The size of the slide. If the name is not valid or not exists a slide or slider
            with the given name, return 0
        """
        if not name:
            return 0
        slide_like = self.__current_slider[str(name)]
        return len(slide_like) if slide_like else 0

    def current_slide_size(self):
        """
        Gets the size of the current slide name
        :return: The size of the slide
        """
        return self.slide_size(self.__current_name)

    def previous_page(self):
        """
        Gets the action to switch to the previous page on the current slide.
        :return: The action to change the page, or None if the current page number is the first
        """
        if self.__page > 0:
            return Function(self.__change_page, self.__page - 1)
        return None

    def next_page(self):
        """
        Gets the action to switch to the next page on the current slide.
        :return: The action to change the page, or None if the current page number is the last.
        """
        current = self.current_slide_size()
        if (self.__page + 1) * self.max_per_page < current:
            return Function(self.__change_page, self.__page + 1)
        return None

    @property
    def page_items(self):
        """
        Gets all buttons for the current page items on the current slide.
        """
        buttons = tuple(self.make_current_button_at(index) for index in range(self.start, self.end + 1))
        remains = tuple(Null() for _ in range(self.end - self.start + 1, self.max_per_page))

        return buttons + remains

    def back(self, from_animation_options=False):
        """
        Gets the action to return to the menu since gallerynpy was called or to navigate between sliders.
        :param from_animation_options: If true, and the current slide is for animations, it means that
            it must return to the first valid slide of the current slider
        :return: The action to return or navigate.
        """
        if not from_animation_options and self.__current_slider != self.__sliders:
            return Function(self.__change_to_parent)

        to_first = Function(self.to_first_slide, gallerynpy.properties.sort_slides)
        if from_animation_options and self.is_current_for_animations:
            return to_first

        return [Function(self.__release_gallery), to_first, Return(), Function(gallerynpy.db.save)]

    def update(self):
        """
        Updates the current start and end index of the current page on the current slide.
        """
        self.__init_gallery()
        self.__start = self.__page * self.max_per_page
        self.__end = min(self.start + self.max_per_page - 1, self.current_slide_size() - 1)


handler: Handler | None = None
"""
The only instance for the Handler class. A reassignment is not recommended.
"""

custom_names = {}
"""
The dic with the custom names for the slides or sliders. A reassignment or a direct set is not recommended.
"""
