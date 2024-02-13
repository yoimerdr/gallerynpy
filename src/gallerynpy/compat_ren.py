from handler_ren import *
from handler_ren import _handler, _custom_names, _screen_size
from resources_ren import load_named_resources

"""renpy
init python in gallerynpy:
"""


def to_first_slide(sort: bool = False):
    _handler.to_first_slide(sort)


def change_distribution(rows: int = None, columns: int = None):
    _handler.change_distribution(rows=rows, columns=columns)


def tooltip():
    return _handler.tooltip


def distribution():
    return _handler.columns, _handler.rows


def next_page():
    return _handler.next_page()


def previous_page():
    return _handler.previous_page()


def page_buttons():
    return _handler.page_items


def content_slides():
    return [name for name in _handler.current_slides if _handler.slide_size(name) > 0]


def custom_name_for(slide_name: str, new_name: str):
    slide_name = str(or_default(slide_name, ""))
    new_name = str(or_default(new_name, ""))
    if slide_name and new_name:
        _custom_names[slide_name] = new_name


def name_for(name: str):
    name = str(or_default(name, ""))
    return _custom_names[name] if name in _custom_names.keys() else name.capitalize()


def is_current(name: str):
    return _handler.is_current_slide(name)


def change_slide_to(slide_name: str):
    return [Function(_handler.update, True), Function(_handler.change_slide, slide_name)]


def back(from_animation_options=False):
    return _handler.back(from_animation_options)


def is_for_animations():
    return _handler.is_current_for_animations()


def update(start: bool = False):
    return _handler.update(start)


def put_item(where: str, resource, thumbnail_resource=None, song: str = None,
             condition: str = None, tooltip: str = None, for_animation_slide: bool = False):
    item = create_item(resource, thumbnail_resource, song, condition, tooltip)
    _handler.put_item(item, where, for_animation_slide)


def put_image(image, where: str = None, song: str = None, condition: str = None, tooltip: str = None,
              thumbnail_resource=None, ):
    put_item(image, or_default(where, "images"), thumbnail_resource, song, condition, tooltip, False)


def put_video(filename: str, where: str = None, thumbnail=None, song=None, condition=None, tooltip=None):
    if filename:
        filename = str(filename)
    put_item(or_default(where, "videos"), filename, thumbnail, song, condition, tooltip, False)


def put_animation(animation_name: str, thumbnail_name=None, where=None, song=None,
                  condition=None, is_animation_slide=True, tooltip=None):
    if animation_name:
        animation_name = str(animation_name)
    put_item(or_default(where, "animations"), animation_name, thumbnail_name,
             song, condition, tooltip, is_animation_slide)


def create_item(resource, thumbnail_resource=None, song: str = None, condition: str = None,
                tooltip: str = None):
    return _handler.create_item(resource, thumbnail_resource, song, condition, tooltip)


def create_image(image, song: str = None, condition: str = None, tooltip: str = None, thumbnail_resource=None, ):
    return create_item(image, thumbnail_resource, song, condition, tooltip)


def create_video(filename, thumbnail=None, song=None, condition=None, tooltip=None):
    filename = or_default(filename, "")
    return create_item(filename, thumbnail, song, condition, tooltip)


def create_animation(atl_object, thumbnail_name, song=None, condition=None, tooltip=None):
    return create_video(atl_object, thumbnail_name, song, condition, tooltip)


def put_slide_like(slide: Slide | Slider, *args: Slide | Slider):
    _handler.put_slide_like(slide)
    [_handler.put_slide_like(slide) for slide in args]


def put_slider(slider: Slider):
    put_slide_like(slider)


def screen_size():
    return Size.from_size(_screen_size)
