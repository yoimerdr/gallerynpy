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


def is_item(obj):
    """
    Checks if the given object is instance of `Item`

    :param obj: The object to check.
    """
    return isinstance(obj, Item)


class Item:
    """
    Represents a single item in gallerynpy gallery.
    """

    def __init__(self, name: str, resource, size: gallerynpy.Size, song: str = None, condition: str = None,
                 tooltip: str = None):
        """
        :param name: The item name. Must be unique.
        :param resource: The resource of the item.
        :param size: The size of the item thumbnail.
        :param song: A valid filepath for an audio that renpy can load.
        :param condition: The condition to unlock the item.
        :param tooltip: The tooltip text to display when the item is hovered.
        """
        self.name = name
        self.__resource = gallerynpy.resources.Resource(resource, gallerynpy.properties.force_loader)
        self.__thumbnail = gallerynpy.resources.Thumbnail(self.__resource, size)
        self.song = song
        self.condition = condition
        self.tooltip = tooltip

    @property
    def resource(self):
        """
        Gets the item resource.
        """
        return self.__resource

    @resource.setter
    def resource(self, resource):
        """
        Changes the item resource
        :param resource: The new resource of the item.
        """
        self.__resource.resource = resource

    @property
    def name(self) -> str:
        """
        Gets the item name
        """
        return self.__name

    @name.setter
    def name(self, name: str):
        """
        Sets the item name
        :param name: The new item name. Must be unique.
        """
        if not name:
            raise ValueError("The given name is not valid for an item")

        self.__name = str(name)

    @property
    def tooltip(self) -> str:
        """
        Gets the item tooltip.
        """
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, tooltip: str):
        """
        Sets the item tooltip.
        :param tooltip: The new item tooltip
        """
        self.__tooltip = str(gallerynpy.or_default(tooltip, ""))

    @property
    def song(self) -> str:
        """
        Gets the item song.
        """
        return self.__song

    @song.setter
    def song(self, song: str):
        """
        Sets the item song.
        :param song: A valid filepath for an audio that renpy can load
        """
        song = gallerynpy.normalize_path(song, for_renpy=True)
        if not gallerynpy.is_loadable(song, gallerynpy.resources.Extensions.AUDIO):
            song = None
        self.__song = song

    @property
    def condition(self) -> str:
        """
        Gets the item condition.
        """
        return self.__condition

    @condition.setter
    def condition(self, condition: str):
        """
        Sets the item condition.
        :param condition: The new condition to unlock the item
        """
        if condition is not None:
            condition = str(condition)
        self.__condition = condition

    @property
    def meets_condition(self):
        """
        Checks if this `Item` meets the condition it has or does not have it.
        """
        return not self.condition or eval(self.condition)

    def if_condition(self, to_return):
        """
        Gets the given param if this `Item` meets the condition it has.

        See also `Item.meets_condition`
        :param to_return: The object to return
        :return: `to_return` if it meets the condition, None otherwise
        """
        return to_return if self.meets_condition else None

    @property
    def thumbnail(self) -> gallerynpy.resources.Thumbnail:
        """
        Gets the thumbnail object of the item. If not meets its condition, returns a thumbnail of the locked resource
        """
        if self.meets_condition:
            return self.__thumbnail
        return gallerynpy.resources.Thumbnail(gallerynpy.properties.locked, self.__thumbnail.size)
