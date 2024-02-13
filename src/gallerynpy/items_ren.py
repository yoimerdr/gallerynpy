from db_ren import Size, is_size
from utils_ren import (is_loadable, normalize_path, join_path, or_default)
from resources_ren import Resource, ResourceTypes, Extensions
from definitions import properties

__all__ = (
    "Item",
    "Thumbnail",
    "is_item"
)

"""renpy
init -1 python in gallerynpy:
"""


def is_item(obj):
    return isinstance(obj, Item)


class Thumbnail:
    def __init__(self, resource: Resource, size: Size):
        if not isinstance(resource, Resource):
            resource = Resource(resource)
        self.__resource = resource
        self.__custom = None
        self.size = size

    @property
    def size(self) -> Size:
        return self.__size

    @size.setter
    def size(self, size: Size):
        if is_size(size):
            self.__size = size

    def __get_resource(self):
        return self.__resource if self.__custom is None else self.__custom

    def create(self):
        resource = self.__get_resource()
        if resource.type == ResourceTypes.VIDEO and resource.extension:
            for ext in properties.video_thumbnail_extensions:
                name = resource.resource.replace(resource.extension, ext)
                path = join_path(properties.thumbnails_folder, name, for_renpy=True)
                if is_loadable(path):
                    resource = Resource(path)
                    break
        elif resource.type not in (ResourceTypes.IMAGE, ResourceTypes.DISPLAYABLE):
            resource = properties.not_found

        return resource.composite_to(self.size)

    def set_custom(self, resource):
        if resource is None:
            self.__custom = None
        elif self.__custom is None:
            self.__custom = Resource(resource, properties.force_loader)
        else:
            self.__custom.resource = resource


class Item:
    def __init__(self, name: str, resource: str, size: Size, song: str = None, condition: str = None,
                 tooltip: str = None):
        self.name = name
        self.__resource = Resource(resource, properties.force_loader)
        self.__thumbnail = Thumbnail(self.__resource, size)
        self.song = song
        self.condition = condition
        self.tooltip = tooltip

    @property
    def resource(self):
        return self.__resource

    @resource.setter
    def resource(self, resource):
        self.__resource.resource = resource

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = str(name)

    @property
    def tooltip(self) -> str:
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, tooltip: str):
        self.__tooltip = str(or_default(tooltip, ""))

    @property
    def song(self) -> str:
        return self.__song

    @song.setter
    def song(self, song: str):
        song = normalize_path(song, for_renpy=True)
        if not is_loadable(song, Extensions.AUDIO):
            song = None
        self.__song = song

    @property
    def condition(self) -> str:
        return self.__condition

    @condition.setter
    def condition(self, condition: str):
        if condition is not None:
            condition = str(condition)
        self.__condition = condition

    @property
    def meets_condition(self):
        """
        Checks if this `Item` meets the condition it has.
        :return: True if it meets the condition `or does not have it`, False otherwise
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
    def thumbnail(self) -> Thumbnail:
        if self.meets_condition:
            return self.__thumbnail
        return Thumbnail(properties.locked, self.__thumbnail.size)
