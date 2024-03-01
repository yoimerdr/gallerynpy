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


import typing
import gallerynpy

"""renpy
init -3 python in gallerynpy:
# docstring:1
The gallerynpy stored module.
from store import gallerynpy
"""


def is_slide(obj):
    """
    Checks if the object is a `Slide`

    :param obj: The object to check
    :return: True if the object is an `Slide`, False otherwise
    """
    return isinstance(obj, Slide)


def is_slider(obj):
    """
    Checks if the object is a `Slider`
    :param obj: The object to check
    :return: True if the object is an `Slider`, False otherwise
    """
    return isinstance(obj, Slider)


class SlideLike(object):
    """
    The base class for the slides and sliders.
    """

    def __init__(self, name: str, parent: "Slider"):
        """
        :param name: The name (identifier) of the `SlideLike`
        :param parent: The `Slider` parent of the `SlideLike`
        """
        self._name = str(name)
        self._parent = None
        self.parent = parent
        self._size = 0
        self._items = None

    @property
    def size(self) -> int:
        """
        Gets the current size.
        """
        return self._size

    @property
    def name(self) -> str:
        """
        Gets the current name.
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """
        Sets the name (str value).
        :param name: The new name.
        """
        self._name = str(gallerynpy.or_default(name, ""))

    @property
    def parent(self) -> "Slider":
        """
        Gets the current parent `Slider`.
        """
        return self._parent

    @parent.setter
    def parent(self, parent: "Slider"):
        """
        Sets the parent `Slider`. Only if is a `Slider` instance or is None.
        :param parent: The new parent.
        """
        if parent is None:
            self._parent = None
        elif is_slider(parent):
            self._parent = parent

    def clone(self, name: str = None, include_parent: bool = False) -> "SlideLike":
        raise NotImplementedError("Must be implemented in child")

    def put(self, item) -> bool:
        raise NotImplementedError("Must be implemented in child")

    def get(self, identifier) -> typing.Any | None:
        raise NotImplementedError("Must be implemented in child")

    def __len__(self):
        return self.size

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<SlideLike '{}' with {} items>".format(self.name, self.size)

    def __hash__(self):
        return hash(self.name)

    def __contains__(self, item):
        if self._items and item:
            return item in self._items
        return False

    def __iter__(self):
        if self._items:
            return iter(self._items)

        return iter([])

    def __getitem__(self, identifier) -> typing.Any | None:
        return self.get(identifier)


class Slider(SlideLike):
    """
    A slider to contain `Slide`s or other `Slider`s
    """

    def __init__(self, name: str, parent: "Slider" = None):
        """
        :param name: The name of the slider.
        :param parent: The `Slider` parent of this one.
        """
        super(Slider, self).__init__(name, parent)
        self._items = {}

    @property
    def slides(self) -> list[str]:
        """
        Gets all the names of the slider items.
        """
        return list(self._items.keys())

    def clone(self, name: str = None, include_parent: bool = False) -> "Slider":
        """
        Clone the slider and every slide or slider it has.
        :param name: The new name of the slider. By default, is the own.
        :param include_parent: If True, sets the parent `Slider` as the parent of the cloned slide.
        :return: The cloned slider.
        """

        name = name if name else self.name
        slider = Slider(name, parent=self.parent if include_parent else None)

        for item in map(lambda key: self.get(key).clone(), self.slides):
            item.parent = slider
            slider._items[item.name] = item

        return slider

    def _put(self, item: SlideLike):
        if item.name not in self.slides:
            self._items[item.name] = item
            self._size += 1
            return True
        return False

    def put(self, item: SlideLike):
        """
        Adds the `Slide` or `Slider` to this one.

        The name of the given item must be unique in this slider.
        :param item: The item to be added.
        :return: True if the item was added, False otherwise
        """
        if (is_slide(item) or is_slider(item)) and self._put(item):
            item.parent = self
            return True
        return False

    def get(self, identifier: str) -> SlideLike | None:
        """
        Gets the `Slide` or `Slider` with the given identifier.
        :param identifier: The item name
        :return: The item with the given name, or None if it is not present.
        """
        if identifier is None:
            return None

        identifier = str(identifier)
        if identifier in self.slides:
            return self._items[identifier]
        return None

    def create_slide(self, name: str, is_for_animations: bool = False) -> "Slide":
        """
        Creates a new `Slide` with this slider as parent.
        :param name: The slide name
        :param is_for_animations: Sets True if the slide will be marked as one for animations.
        :return: The created slide
        """
        slide = Slide(name=name, parent=self, is_for_animations=is_for_animations)
        self._put(slide)
        return slide

    def create_slider(self, name: str) -> "Slider":
        """
        Creates a new slide with this slider as parent.
        :param name: The slider name.
        :return: The created slider
        """
        slider = Slider(name=name, parent=self)
        self._put(slider)
        return slider

    def __getitem__(self, identifier: str) -> SlideLike | None:
        return super(Slider, self).__getitem__(identifier)

    def __contains__(self, item):
        if not item:
            return False
        return item in self.slides

    def __iter__(self):
        if self._items:
            return iter(self._items.items())
        return iter([])

    def __repr__(self):
        return "<Slider '{}' with {} items>".format(self.name, self.size)


class Slide(SlideLike):
    """
    A slide to contain the `Item`s
    """

    def __init__(self, name: str, parent: Slider = None, is_for_animations: bool = False):
        """
        :param name: The name of the slide.
        :param parent: The `Slider` parent of this one.
        :param is_for_animations: Sets True if the slide will be marked as one for animations.
            If it is marked for animations, only items of that type (`or maybe not`) will be accepted.
        """
        super(Slide, self).__init__(name, parent)
        self.__is_anim_slide = is_for_animations
        self._items = []

    @property
    def is_for_animations(self) -> bool:
        """
        Gets whether the slide is marked as one for animations.
        """
        return self.__is_anim_slide

    def clone(self, name: str = None, include_parent: bool = False) -> "Slide":
        """
        Clones the slide.
        :param name: The new name of the slide. By default, is the own.
        :param include_parent: If True, sets the parent slide as the parent of the cloned slide.
        :return: The cloned slide.
        """
        name = name if name else self.name
        slide = Slide(name, self.parent if include_parent else None, self.is_for_animations)
        [slide.put(item) for item in self]
        return slide

    def put(self, item: gallerynpy.Item):
        """
        Adds a valid `Item` to the slide.
        :param item: The item to be added.
        :return: True if the item was added, False otherwise.
        """
        if gallerynpy.is_item(item):
            self._items.append(item)
            self._size += 1
            return True
        return False

    def get(self, identifier: int) -> gallerynpy.Item | None:
        """
        Gets the `Item` with the given identifier.
        :param identifier: The item index
        :return: The item in the given index, or None if invalid.
        """
        if identifier is None:
            return None

        identifier = int(identifier)
        if 0 <= identifier < self.size:
            return self._items[identifier]
        return None

    def __getitem__(self, identifier: int) -> gallerynpy.Item | None:
        return super(Slide, self).__getitem__(identifier)

    def __repr__(self):
        return "<Slide '{}' with {} items>".format(self.name, self.size)
