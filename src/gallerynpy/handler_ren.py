from db_ren import Size, _screen_size, db
from items_ren import Item, is_item
from properties_ren import Properties
from resources_ren import ResourceTypes, Resource
from slides_ren import Slider, Slide, is_slider, is_slide
from utils_ren import Singleton, is_loadable, or_default

"""renpy
init python in gallerynpy:
"""
from store import Button, Function, Gallery, dissolve, Call, Play, Stop, Null, config, Return, NullAction

properties = Properties()


class Handler(Singleton):
    def __init__(self):
        self.__start = 0
        self.__end = 0
        self.__rows = 0
        self.__cols = 0
        self.__max_per_page = 0

        self.__thumbnail_size = None
        self.__gallery = Gallery()
        self.__gallery.transition = dissolve

        self.change_distribution(4, 4)
        self.__page = 0
        self.__tooltip = ""

        self.__sliders = Slider("base")
        self.__current_slider = self.__sliders
        self.__current_slide = ""
        self.__item_id = 0

        self.__for_put = []

    def __change_tooltip(self, tooltip: str):
        self.__tooltip = str(tooltip)

    def __add_to_gallery(self, item: Item):
        if not is_item(item):
            return

        self.__gallery.button(item.name)
        if item.resource.type == ResourceTypes.IMAGE:
            image = item.resource.resource
            if properties.rescale_images:
                image = item.resource.composite_to(_screen_size)
            self.__gallery.image(image)
        else:
            self.__gallery.image(item.resource.resource)
        if item.condition:
            self.__gallery.condition(item.condition)

    def __change_current_slide(self, name: str, slider: Slider):
        slider = slider[name]
        if is_slider(slider):
            self.__current_slider = slider
            return True
        return False

    def __add_slide_to_gallery(self, slide: Slide):
        if not is_slide(slide):
            return
        self.__for_put.extend(slide)

    def __slide_like_to_gallery(self, slider: Slider | Slide):
        if is_slider(slider):
            for item in slider:
                key, slide = item
                if is_slider(slide):
                    self.__slide_like_to_gallery(slide)
                elif is_slide(slide):
                    self.__add_slide_to_gallery(slide)

        elif is_slide(slider):
            self.__add_slide_to_gallery(slider)

    def __empty_slide(self):
        self.__current_slide = ""

    def __change_to_parent(self):
        self.__current_slider = self.__current_slider.parent
        if self.__current_slider is None:
            self.__current_slider = self.__sliders

        self.to_first_slide(properties.sort_slides)

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @property
    def thumbnail_size(self) -> Size:
        return self.__thumbnail_size

    @property
    def columns(self):
        return self.__cols

    @property
    def rows(self):
        return self.__rows

    def change_distribution(self, columns: int = None, rows: int = None):
        if columns is None:
            columns = self.columns
        if rows is None:
            rows = self.rows

        def get_max(value: int):
            return 4 if value < 0 else value

        columns = get_max(int(columns))
        rows = get_max(int(rows))

        if rows == self.rows and columns == self.columns:
            return

        self.__rows = rows
        self.__cols = columns
        self.__max_per_page = self.rows * self.columns

        target = max(columns, rows)
        spacing = properties.item_xspacing * (target - 1)
        actual_width = config.screen_width - properties.navigation_xsize - properties.navigation_spacing - spacing
        width = actual_width / target

        new_size = Size(width, int(width * _screen_size.aspect_ratio))
        if self.thumbnail_size is None:
            self.__thumbnail_size = new_size
        else:
            self.thumbnail_size.set(new_size)
        self.__gallery.locked_button = self.scale(properties.locked)

    @property
    def max_per_page(self):
        return self.__max_per_page

    def scale(self, resource: Resource):
        if not isinstance(resource, Resource):
            resource = Resource(resource, properties.force_loader)
        return resource.scale_to(self.thumbnail_size)

    @property
    def idle(self):
        return self.scale(properties.idle)

    @property
    def video_idle(self):
        return self.scale(properties.play_idle)

    @property
    def video_hover(self):
        return self.scale(properties.play_hover)

    @property
    def current_slides(self):
        return self.__current_slider.slides

    @property
    def current_slide(self):
        return self.__current_slide

    @property
    def tooltip(self):
        return self.__tooltip

    def __change_page(self, page: int):
        self.__page = int(page)

    def put_item(self, item: Item, where: str, for_animation_slide: bool = False):
        if where is None or not where:
            raise ValueError("Cannot put an item in a slide without a valid name")

        where = str(where)
        slide = self.__sliders[where]
        if slide is None:
            slide = Slide(where, is_for_animations=for_animation_slide)
            self.__sliders.put(slide)

        slide.put(item)
        self.__for_put.append(item)

    def create_item(self, resource, thumbnail_resource=None, song: str = None, condition: str = None,
                    tooltip: str = None):
        if resource is None:
            raise ValueError("Cannot create a item from none resource")

        item = Item(
            name="gallerynpy-" + str(self.__item_id),
            resource=resource,
            size=self.thumbnail_size,
            song=song,
            condition=condition,
            tooltip=tooltip
        )
        item.thumbnail.set_custom(thumbnail_resource)
        self.__item_id += 1
        return item

    def create_slider(self, name: str):
        return self.__sliders.create_slider(name)

    def put_slide_like(self, slide: Slide | Slider):
        if not is_slide(slide) and not is_slider(slide):
            return
        self.__slide_like_to_gallery(slide)
        self.__sliders.put(slide)

    def change_slide(self, name: str):
        name = str(or_default(name, ""))
        if name in self.current_slides:
            if self.__change_current_slide(name, self.__current_slider):
                self.to_first_slide(properties.sort_slides)
            else:
                self.__current_slide = name

    def is_current_slide(self, name: str):
        return self.current_slide == str(or_default(name, ""))

    def is_current_for_animations(self):
        slide: Slide | None = self.__current_slider[self.__current_slide]
        return is_slide(slide) and slide.is_for_animations

    def make_item_button(self, item: Item):
        button = Button(action=None)
        if not is_item(item) or item.resource.type == ResourceTypes.NONE:
            return button

        self.__add_to_gallery(item)

        if item.resource.type in (ResourceTypes.IMAGE, ResourceTypes.DISPLAYABLE):
            idle_border = self.idle
            hover_border = None
        else:
            idle_border = self.video_idle
            hover_border = self.video_hover

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
        elif item.resource.type == ResourceTypes.VIDEO:
            button.action = Call("gallerynpy_cinema", movie=item.resource.resource, song=item.song)
        else:
            if item.song and is_loadable(item.song):
                button.action = [Play("music", item.song), button.action, Stop("music")]

        return button

    def make_current_button_at(self, index: int):
        item = self.current_item_at(index)
        if item is None or item.resource.type == ResourceTypes.NONE:
            return Null()
        return self.make_item_button(item)

    def to_first_slide(self, sort: bool = False):
        names = self.current_slides
        if names:
            if sort:
                names.sort()

            for name in names:
                slide: Slide | None = self.__current_slider[name]
                if is_slide(slide) and not (properties.with_speed and slide.is_for_animations):
                    self.change_slide(name)
                    return
            self.__empty_slide()

    def item_at(self, where: str, index: int) -> Item | None:
        slide = self.__current_slider[where]
        if not is_slide(slide):
            return None
        return slide[index]

    def current_item_at(self, index: int):
        return self.item_at(self.__current_slide, index)

    def slide_size(self, name: str):
        name = str(name)
        return len(self.__current_slider[name]) if name in self.__current_slider.slides else 0

    def current_slide_size(self):
        return self.slide_size(self.__current_slide)

    def previous_page(self):
        if self.__page > 0:
            return Function(self.__change_page, self.__page - 1)
        return None

    def next_page(self):
        current = self.current_slide_size()
        if (self.__page + 1) * self.max_per_page < current:
            return Function(self.__change_page, self.__page + 1)
        return None

    @property
    def page_items(self):
        buttons = [self.make_current_button_at(index) for index in range(self.start, self.end + 1)]
        remains = [Null() for _ in range(self.end - self.start + 1, self.max_per_page)]

        return buttons + remains

    def back(self, from_animation_options=False):
        if not from_animation_options and self.__current_slider != self.__sliders:
            return [Function(self.update, True), Function(self.__change_to_parent)]

        if from_animation_options and self.is_current_for_animations:
            return [Function(self.update, True), Function(self.to_first_slide, properties.sort_slides)]

        return [Return(), Function(db.save)]

    def update(self, start: bool = False):
        if start:
            self.__page = 0

        self.__start = self.__page * self.max_per_page
        self.__end = min(self.start + self.max_per_page - 1, self.current_slide_size() - 1)


_handler: Handler = Handler()
_custom_names = {}
