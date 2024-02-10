from typing import Any
from items_ren import Item, is_item

__all__ = (
    "Slider",
    "SlideLike",
    "Slide",
    "is_slider",
    "is_slide"
)

"""renpy
init -3 python in gallerynpy:
"""


def is_slide(obj):
    return isinstance(obj, Slide)


def is_slider(obj):
    return isinstance(obj, Slider)


class SlideLike:
    def __init__(self, name: str, parent: "Slider", is_for_animations: bool = False):
        self._name = str(name)
        self._parent = None
        self.parent = parent
        self._size = 0
        self._items = None
        self.__is_anim_slide = is_for_animations

    @property
    def size(self) -> int:
        """
        Gets the size of the slide.
        """
        return self._size

    @property
    def name(self) -> str:
        """
        Gets the name of the slide.
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """
        Sets the name (str value) of the slide.
        :param name: The new name.
        """
        self._name = str(name)

    @property
    def parent(self) -> "Slider":
        """
        Gets the parent of the slide.
        """
        return self._parent

    @parent.setter
    def parent(self, parent: "Slider"):
        """
        Sets the father of the slide. Only if is a GallerynpySlider instance or is None.
        :param parent: The new parent.
        """
        if parent is None:
            self._parent = None
        elif is_slider(parent):
            self._parent = parent

    @property
    def is_for_animations(self) -> bool:
        """
        Gets whether the slide is marked as one for animations.
        :return:
        """
        return self.__is_anim_slide

    def clone(self, name: str = None, include_parent: bool = False) -> "SlideLike":
        raise NotImplementedError("Must be implemented in child")

    def put(self, item):
        raise NotImplementedError("Must be implemented in child")

    def get(self, identifier) -> Any | None:
        raise NotImplementedError("Must be implemented in child")

    def __len__(self):
        return self.size

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name.__repr__()

    def __hash__(self):
        return hash(self.name)

    def __iter__(self):
        if self._items:
            return iter(self._items)

        return iter([])

    def __getitem__(self, identifier) -> Any | None:
        return self.get(identifier)


class Slider(SlideLike):
    def __init__(self, name: str, parent: "Slider" = None):
        super().__init__(name, parent)
        self._items = {}

    @property
    def slides(self) -> list[str]:
        """
        Gets all the names of the slider items.
        :return:
        """
        return list(self._items.keys())

    def clone(self, name: str = None, include_parent: bool = False) -> "Slider":
        """
        Clone the slider and every slide or slider it has.
        :param name: The new name of the slider. By default, is the own.
        :param include_parent: If True, sets the parent slider as the parent of the cloned slide.
        :return: The cloned slider.
        """

        name = name if name else self.name
        slider = Slider(name, parent=self.parent if include_parent else None)

        for item in map(lambda key: self.get(key).clone(), self.slides):
            item.parent = slider
            slider._items[item.name] = item

        return slider

    def put(self, item: SlideLike):
        """
        Adds the slide or slider item to the slider.

        The name of the given item must be unique in this slider.
        :param item: The item to be added.
        """
        if is_slide(item) or is_slider(item):
            if item.name not in self.slides:
                self._items[item.name] = item
                self._size += 1

    def get(self, identifier: str) -> SlideLike | None:
        """
        Gets the BaseGallerynpySlide with the given identifier.
        :param identifier: The item name
        :return: The item with the given name, or None if not present.
        """
        identifier = str(identifier)
        if identifier in self.slides:
            return self._items[identifier]
        return None

    def create_slide(self, name: str, is_for_animations: bool = False) -> "Slide":
        """
        Creates a new slide with this slider as parent.
        :param name: The slide name
        :param is_for_animations: Sets True if the slide will be marked as one for animations.
        :return: The created slide
        """
        return Slide(name=name, parent=self, is_for_animations=is_for_animations)

    def create_slider(self, name: str) -> "Slider":
        """
        Creates a new slide with this slider as parent.
        :param name: The slider name.
        :return: The created slider
        """
        return Slider(name=name, parent=self)

    def __getitem__(self, identifier: str) -> SlideLike | None:
        return super().__getitem__(identifier)


class Slide(SlideLike):
    def __init__(self, name: str, parent: Slider = None, is_for_animations: bool = False):
        super().__init__(name, parent, is_for_animations)
        self._items = []

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

    def put(self, item: Item):
        """
        Adds a valid Item to the slide.
        :param item: The item to be added.
        """
        if is_item(item):
            self._items.append(item)
            self._size += 1

    def get(self, identifier: int) -> Item | None:
        """
        Gets the Item with the given identifier.
        :param identifier: The item index
        :return: The item with the given index, or None if not valid.
        """
        identifier = int(identifier)
        if 0 <= identifier < self.size:
            return self._items[identifier]
        return None

    def __getitem__(self, identifier: int) -> Item | None:
        return super().__getitem__(identifier)
