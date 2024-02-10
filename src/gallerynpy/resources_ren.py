from db_ren import Size, is_size, db
from utils_ren import is_image, is_animation, file_extension, is_loadable, get_registered, Singleton, or_default

# All of the above will be ignored when converting to .rpy files.


"""renpy
init -3 python in gallerynpy:
"""
from store import Image, renpy, im, Composite


def is_displayable(obj):
    return isinstance(obj, renpy.display.displayable.Displayable)


def get_displayable_of(displayable_like, force_check=False):
    if is_displayable(displayable_like):
        return displayable_like
    resource = Resource(displayable_like, force_check=force_check)
    if resource.type != ResourceTypes.IMAGE:
        raise ValueError("Invalid asset type.")
    return resource.resource


class Extensions:
    IMAGES = ('.png', '.jpg', '.web', '.jpeg', '.webp')
    VIDEOS = ('.webm', '.avi', '.mp4', '.wav', '.mkv', '.ogv')


class ResourceTypes:
    ANIMATION = 'animation'
    VIDEO = 'video'
    IMAGE = 'image'
    DISPLAYABLE = 'displayable'
    NONE = 'none'


class NamedResourcesLoader(Singleton):
    def __init__(self):
        self.__resources = []

    def push(self, resource: "Resource"):
        if not isinstance(resource, Resource):
            return
        if not resource.is_named:
            raise ValueError("Illegal resource. An non named resource should already be validated.")
        self.__resources.append(resource)

    def load(self):
        [resource.load(True) for resource in self.__resources]
        self.__resources.clear()


_named_resources_loader = NamedResourcesLoader()


class Resource:
    def __init__(self, asset, force_check: bool = False):
        self.__type = ResourceTypes.NONE
        self.__extension = None
        self.__is_named = False
        self.__force_check = or_default(force_check, False)
        self.__size: Size | None = None
        self.resource = asset

    def load(self, force_check: bool = False):
        self.__size = None
        self.__type = ResourceTypes.NONE
        self.__extension = None
        self.__is_named = False

        def image_like(displayable, nameable: bool = False):
            if displayable:
                self.__is_named = True
                if is_image(displayable):
                    self.__size = db.get_size(self.resource, named=True)
                    self.__type = ResourceTypes.IMAGE
                elif is_animation(displayable):
                    self.__type = ResourceTypes.ANIMATION
                elif is_displayable(displayable):
                    self.__type = ResourceTypes.DISPLAYABLE
                    self.__is_named = False
                else:
                    raise ValueError(f"Unsupported resource type: {type(displayable)}")
            elif nameable:
                if force_check:
                    raise ValueError("No image or animation block with name: '" + self.resource + "'.")
                self.__is_named = True
                _named_resources_loader.push(self)
            else:
                raise ValueError("Invalid resource. It is not an Image object or inherits from it.")

        if isinstance(self.resource, str):
            def _is_loadable():
                # checks if the file is loadable
                if not is_loadable(self.resource):
                    raise FileNotFoundError("Cannot find the file: '" + self.resource + "'")

            self.__extension = file_extension(self.resource)
            if self.__extension in Extensions.IMAGES:
                _is_loadable()
                self.__size = db.get_size(self.resource)
                self.__type = ResourceTypes.IMAGE
            elif self.__extension in Extensions.VIDEOS:
                _is_loadable()
                self.__type = ResourceTypes.VIDEO
            else:
                image_like(get_registered(self.resource), True)
        else:
            image_like(self.resource)
            self.__is_named = False

    @property
    def resource(self):
        return self.__resource

    @resource.setter
    def resource(self, resource):
        self.__resource = resource
        self.load(self.__force_check)

    @property
    def extension(self) -> str | None:
        if self.is_named or self.type in (ResourceTypes.ANIMATION, ResourceTypes.NONE):
            return None

        return self.__extension

    @property
    def type(self) -> str:
        return self.__type

    @property
    def size(self) -> Size | None:
        if self.__size is None:
            return None
        return Size.from_size(self.__size)

    @property
    def is_named(self) -> bool:
        return self.__is_named

    def get_image(self):
        if self.type != ResourceTypes.IMAGE:
            raise ValueError("Cannot get an Image of an " + self.type + " resource type")

        if self.is_named:
            return get_registered(self.resource)
        elif is_image(self.resource):
            return self.resource
        elif is_loadable(self.resource, Extensions.IMAGES):
            return Image(self.resource)

        return None

    def force_load_size(self):
        if is_size(self.__size):
            return

        image = self.get_image()
        if image is None:
            raise ValueError("Cannot load size of none.")

        width, height = image.load().get_size()
        self.__size = Size(width, height)
        db.put_size(self.resource, self.__size, named=self.__is_named)

    def size_to(self, target: Size) -> Size:
        if not is_size(target):
            raise ValueError("The target size mut be a Size object")

        if self.__size is None:
            return target

        ratio = self.__size.width / self.__size.height

        if self.__size == target or ratio == 16 / 9:
            return target
        elif ratio > 16 / 9:
            return Size(target.width, int(target.width / ratio))

        return Size(int(target.height * ratio), target.height)

    def scale_to(self, target: Size):
        if not is_size(target):
            raise ValueError("The target size mut be a Size object")
        if self.type == ResourceTypes.DISPLAYABLE:
            image = self.resource
            size = target
        else:
            image = self.get_image()
            size = self.size_to(target)
        return im.Scale(image, size.width, size.height)

    def composite_to(self, target: Size):
        if self.type == ResourceTypes.DISPLAYABLE:
            image = self.resource
            size = target
        else:
            self.force_load_size()
            size = self.size_to(target)
            image = self.scale_to(target)
        x = int(target.width / 2 - size.width / 2)
        return Composite((target.width, target.height), (x, 0), image)


def load_named_resources():
    _named_resources_loader.load()
