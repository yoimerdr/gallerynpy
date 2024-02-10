from db_ren import Size, is_size
from utils_ren import (is_loadable, normalize_path, join_path, or_default)
from resources_ren import Resource, ResourceTypes
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
    def __init__(self, item: Resource, size: Size):
        if not isinstance(item, Resource):
            item = Resource(item)
        self.__resource = item
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
        elif resource.type != ResourceTypes.IMAGE:
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

    def __init_image(self):
        self.__type = ResourceTypes.IMAGE

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
        self.__song = normalize_path(song, for_renpy=True)

    @property
    def condition(self) -> str:
        return self.__condition

    @condition.setter
    def condition(self, condition: str):
        if condition is None:
            self.__condition = None
        else:
            self.__condition = str(condition)

    @property
    def thumbnail(self) -> Thumbnail:
        return self.__thumbnail
