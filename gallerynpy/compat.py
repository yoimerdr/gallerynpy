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

from store import Function


def load_named_resources():
    """
    Load all resource putted in the named_resources_loader.
    """
    gallerynpy.resources.named_resources_loader.load()
    gallerynpy.handler.check_puts()


def to_first_slide(sort: bool = False):
    """
    Changes the selected slide name to the name of the first valid slide in the current slider.
    :param sort: If true, sorts slide names before the change.
    """
    gallerynpy.handler.to_first_slide(sort)


def change_distribution(rows: int = None, columns: int = None):
    """
    Changes the distribution on each page of each slide.
    :param columns: The number of columns in the page.
    :param rows: The number of rows in the page.
    """
    gallerynpy.handler.change_distribution(rows=rows, columns=columns)


def tooltip():
    """
    Gets the current tooltip.
    """
    return gallerynpy.handler.tooltip


def distribution():
    """
    Gets the current distribution on each page.
    :return: A tuple containing the (cols, rows) values
    """
    return gallerynpy.handler.columns, gallerynpy.handler.rows


def rows():
    """
    Gets the maximum number of rows on each page of each slide.
    """
    return gallerynpy.handler.rows


def cols():
    """
    Gets the maximum number of columns on each page of each slide.
    """
    return gallerynpy.handler.columns


def next_page():
    """
    Gets the action to switch to the next page on the current slide.
    :return: The action to change the page, or None if the current page number is the last.
    """
    return gallerynpy.handler.next_page()


def previous_page():
    """
    Gets the action to switch to the previous page on the current slide.
    The action to change the page, or None if the current page number is the first
    """
    return gallerynpy.handler.previous_page()


def page_buttons():
    """
    Gets all buttons for the current page items on the current slide.
    """
    return gallerynpy.handler.page_items


def content_slides():
    """
    Gets the name of all slides that have at least one item into.
    """
    return [name for name in gallerynpy.handler.current_slides if gallerynpy.handler.slide_size(name) > 0]


def custom_name_for(slide_name: str, new_name: str):
    """
    Sets a custom name for the slides or sliders with the given name.
    :param slide_name: The name of the slides or sliders
    :param new_name: The custom name
    """
    slide_name = str(gallerynpy.or_default(slide_name, ""))
    new_name = str(gallerynpy.or_default(new_name, ""))
    if slide_name and new_name:
        gallerynpy.custom_names[slide_name] = new_name


def name_for(name: str):
    """
    Gets the name for the sliders or slides with the given name.
    :param name: The name of the slides or sliders
    :return: The custom name if it exists, otherwise the capitalized name.
    """
    name = str(gallerynpy.or_default(name, ""))
    return gallerynpy.custom_names[name] if name in gallerynpy.custom_names.keys() else name.capitalize()


def is_current(name: str):
    """
    Checks if the given name is equal to the currently selected name.
    :param name: The name of the slide, or slide, to check.
    :return: True if the name is equal to the currently selected, False otherwise.
    """
    return gallerynpy.handler.is_current_slide(name)


def change_slide_to(slide_name: str):
    """
    Gets the action to change the current selected slide.
    :param slide_name: The name of the new selected slide.
    """
    return Function(gallerynpy.handler.change_slide, slide_name)


def back(from_animation_options=False):
    """
    Gets the action to return to the menu since gallerynpy was called or to navigate between sliders.
    :param from_animation_options: If true, and the current slide is for animations, it means that it must return to
        the first valid slide of the current slider
    :return: The action to return or navigate.
    """
    return gallerynpy.handler.back(from_animation_options)


def is_for_animations():
    """
    Checks if the current slide is one for animations
    :return: True if the current slide is one for animations, False otherwise
    """
    return gallerynpy.handler.is_current_for_animations()


def update(start: bool = False):
    """
    Updates the current start and end index of the current page on the current slide.
    :param start: Parameter not used, it is present for compatibility
    """
    return gallerynpy.handler.update()


def put_item(where: str, resource, thumbnail=None, song: str = None,
             condition: str = None, tooltip: str = None, for_animation_slide: bool = False):
    """
    Creates a new item and put it into the gallerynpy gallery.
    :param where: The name of the slide to put the item into
    :param resource: The item resource
    :param thumbnail: The item custom thumbnail resource.
    :param song: A valid filepath for an audio that renpy can load.
    :param condition: The condition to unlock the item.
    :param tooltip: The tooltip text to display when the item is hovered.
    :param for_animation_slide: If true and the slide with the given name has not yet been created, the slide is marked
        as one for animations.
    """
    item = create_item(resource, thumbnail, song, condition, tooltip)
    gallerynpy.handler.put_item(item, where, for_animation_slide)


def put_image(image, where: str = None, song: str = None, condition: str = None, tooltip: str = None,
              thumbnail_resource=None, ):
    """
    Deprecated. Use `put_item` instead.
    """
    put_item(gallerynpy.or_default(where, "images"), image, thumbnail_resource, song, condition, tooltip, False)


def put_video(filename: str | gallerynpy.resources.Resource, where: str = None, thumbnail=None,
              song=None, condition=None, tooltip=None):
    """
    Deprecated. Use `put_item` instead.
    """
    put_item(gallerynpy.or_default(where, "videos"), filename, thumbnail, song, condition, tooltip, False)


def put_animation(animation_name: str | gallerynpy.resources.Resource, thumbnail_name=None, where=None, song=None,
                  condition=None, is_animation_slide=True, tooltip=None):
    """
    Deprecated. Use `put_item` instead.
    """
    put_item(gallerynpy.or_default(where, "animations"), animation_name, thumbnail_name,
             song, condition, tooltip, is_animation_slide)


def create_item(resource, thumbnail=None, song: str = None, condition: str = None,
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
    return gallerynpy.handler.create_item(resource, thumbnail, song, condition, tooltip)


def create_image(image, song: str = None, condition: str = None, tooltip: str = None, thumbnail_resource=None, ):
    """
    Deprecated. Use `create_item` instead.
    """
    return create_item(image, thumbnail_resource, song, condition, tooltip)


def create_video(filename, thumbnail=None, song=None, condition=None, tooltip=None):
    """
    Deprecated. Use `create_item` instead.
    """
    return create_item(filename, thumbnail, song, condition, tooltip)


def create_animation(atl_object, thumbnail_name, song=None, condition=None, tooltip=None):
    """
    Deprecated. Use `create_item` instead.
    """
    return create_item(atl_object, thumbnail_name, song, condition, tooltip)


def create_slider(name: str):
    """
    Create a slider with the given name and the base slider as its parent
    :param name: The slider name
    :return: The created slider
    """
    return gallerynpy.handler.create_slider(name)


def create_slide(name, is_animation_slide=False):
    """
    Create a slide with the given name and the base slider as its parent.
    :param name: The slide name
    :param is_animation_slide: Sets true if the slide will be marked as one for animations
    :return: The created slide.
    """
    return gallerynpy.handler.create_slide(name, is_animation_slide)


def put_slide_like(slide: gallerynpy.Slide | gallerynpy.Slider, *args: gallerynpy.Slide | gallerynpy.Slider):
    """
    Adds the given slide or slider to the base slider and all its items to the gallerynpy gallery.
    :param slide: The slide or slider to add
    :param args: Other slides or sliders to add
    """
    gallerynpy.handler.put_slide_like(slide)
    for slide in args:
        gallerynpy.handler.put_slide_like(slide)


def put_slider(slider: gallerynpy.Slide | gallerynpy.Slider):
    """
    Deprecated. Use `put_slide_like` instead.
    """
    put_slide_like(slider)


def change_locked(displayable):
    """
    Sets the resource `locked`.
    :param displayable: The new resource for locked
    """
    gallerynpy.properties.locked = displayable


def scale(resource):
    """
    Scales the given resource according to the current thumbnail size.
    :param resource: The resource to scale
    :return:
    """
    return gallerynpy.handler.scale_res(resource)


def change_transition(transition):
    """
    Changes the current transition of the gallerynpy gallery.
    :param transition: Changes the current transition of the gallerynpy gallery.
    """
    gallerynpy.handler.change_transition(transition)


def animation_speed():
    """
    Gets the current animation speed.

    A shortcut to `gallerynpy.properties.animation_speed`.
    """
    return gallerynpy.properties.animation_speed
