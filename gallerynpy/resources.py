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
init -4 python in gallerynpy.resources:
# docstring:1
The gallerynpy.resources stored module.
from store import gallerynpy
"""

from store import Image, renpy, Composite, im

try:
    displayable = renpy.display.displayable
except AttributeError:
    displayable = renpy.display.core
except ImportError:
    displayable = renpy.display.core


class ResourceForbiddenOperationError(Exception):
    """
    Raised when a resource does not have the required type for the operation.
    """

    def __init__(self, rtype):
        message = "Type of resource not allowed to perform this operation: {}".format(rtype)
        super(ResourceForbiddenOperationError, self).__init__(message)


class UnsupportedResourceTypeError(Exception):
    """
    Raised when the object of the resource is not supported.
    """

    def __init__(self, obj):
        message = "The object type for the resource is not valid.: " + str(type(obj))
        super(UnsupportedResourceTypeError, self).__init__(message)


class ResourceNameNotFoundError(Exception):
    """
    Raised when the resource name is not found in the renpy declared images.
    """

    def __init__(self, name: str, message: str = None):
        if message is None:
            message = "No image or animation block with name: '" + name + "'."
        super(ResourceNameNotFoundError, self).__init__(str(message))


class ResourceNoLoadableError(Exception):
    """
    Raised when the rosource filepath is not loadable by renpy.
    """

    def __init__(self, resource):
        message = "The resource '{}' cannot be loaded.".format(resource)
        super(ResourceNoLoadableError, self).__init__(message)


def is_displayable(obj):
    """
    Checks if the object is `renpy displayable`.

    :param obj: The object to check.
    :return: True if the object is a displayable, False otherwise
    """
    return isinstance(obj, displayable.Displayable)


def is_resource(obj):
    """
    Checks if the object is a `Resource`.
    :param obj: The object to check.
    :return: True if the object is a `Resource`, False otherwise
    """
    return isinstance(obj, Resource)


class Extensions:
    """
    Enum class for resource extensions that renpy can load.
    """
    IMAGES = ('.png', '.jpg', '.web', '.jpeg', '.webp')
    """
    List of image extensions that renpy can load.
    """

    VIDEOS = ('.webm', '.avi', '.mp4', '.wav', '.mkv', '.ogv')
    """
    List of video extensions that renpy can load.
    """

    AUDIO = ('.mp3', '.ogg', '.opus', ".mp2")
    """
    List of audio extensions that renpy can load.
    """


class ResourceTypes:
    """
    Enum class for the types of resources to be found.
    """

    ANIMATION = 'animation'
    """
    Represents that the resource is an animation, this means that the saved resource 
    is a str (name) of an atl block or the atl block itself (object).
    
    An atl block is the animation declaration.
    """

    VIDEO = 'video'
    """
    Represents that the resource is an video, this means that the saved resource is a filepath to the video.
    """

    IMAGE = 'image'
    """
    Represents that the resource is an image, this means that the saved resource 
    is a str (name) of an image or the image itself (object).
    """

    DISPLAYABLE = 'displayable'
    """
    Represents that the resource is an displayable, this means that the saved resource is instance of renpy displayable.
    """

    NONE = 'none'
    """
    Represents that the resource is not valid, and at any moment it will raise an error.
    """


class NamedResourcesLoader(gallerynpy.Singleton):
    """
    A dumpy loader class.

    This loader will load the resources that were not forced to load, or were put into it.

    It inherits from Singleton, so there will be only one instance of it.
    """

    def __init__(self):
        self.__resources: list[Resource] = []

    def push(self, resource: "Resource"):
        """
        Adds the resource to be loaded in the future.

        It only accepts resources of type `NONE` and with no extension.
        :param resource: The resource to be loaded
        """
        if not is_resource(resource):
            return
        if resource.is_none_type and resource.extension is None:
            self.__resources.append(resource)

    def load(self):
        """
        Load the resources by forcing them to load.

        If you don't call it before, it will be called in an `init 9999 python` block.
        """
        for resource in self.__resources:
            resource.load(True)
        self.__resources.clear()


named_resources_loader = NamedResourcesLoader()


class Resource:
    """
    A helper to trait with resources such as images, videos, animations or displayable.
    """

    def __init__(self, resource, force_check: bool = False):
        """
        :param resource: The resource
        :param force_check: If `true`, named resources such as images or animations will throw
            `ResourceNameNotFoundError` if they are not found, otherwise the `self resource`
            will be put in the resource loader.
        """

        self.__type = ResourceTypes.NONE
        self.__extension = None
        self.__force_check = gallerynpy.or_default(force_check, False)
        self.__size: gallerynpy.Size | None = None
        self.resource = resource

    def load(self, force_check: bool = False):
        """
        Try to load the resource.

        :param force_check: If `true`, named resources such as images or animations will force to load,
            otherwise the `self resource` will be put in the resource loader.

        :raise UnsupportedResourceTypeError: If the resource type is not valid.
        :raise ResourceNameNotFoundError: If the resource is force to load and don't exist the image or animation
            for the given resource name
        :raise ResourceNoLoadableError: If the resource filepath is not loadable.
        """
        self.__size = None
        self.__type = ResourceTypes.NONE
        self.__extension = None

        def image_like(displayable, nameable: bool = False):
            if displayable:
                if gallerynpy.is_animation(displayable):
                    self.__type = ResourceTypes.ANIMATION
                elif gallerynpy.is_image(displayable):
                    self.__size = gallerynpy.db.get_size(self.resource, named=True)
                    self.__type = ResourceTypes.IMAGE
                elif is_displayable(displayable):
                    self.__type = ResourceTypes.DISPLAYABLE
                else:
                    raise UnsupportedResourceTypeError(displayable)
            elif nameable:
                if force_check:
                    raise ResourceNameNotFoundError(self.resource)
                named_resources_loader.push(self)
            else:
                raise UnsupportedResourceTypeError(displayable)

        if isinstance(self.resource, str):
            def _is_loadable():
                # checks if the file is loadable
                if not gallerynpy.is_loadable(self.resource):
                    raise ResourceNoLoadableError(self.resource)

            self.__extension = gallerynpy.file_extension(self.resource)
            if self.__extension in Extensions.IMAGES:
                _is_loadable()
                self.__size = gallerynpy.db.get_size(self.resource)
                self.__type = ResourceTypes.IMAGE
            elif self.__extension in Extensions.VIDEOS:
                _is_loadable()
                self.__type = ResourceTypes.VIDEO
            else:
                self.__extension = None
                image_like(gallerynpy.get_registered(self.resource), True)
        else:
            image_like(self.resource)

    @property
    def resource(self):
        """
        Gets the resource.
        """
        return self.__resource

    @resource.setter
    def resource(self, resource):
        """
        Sets the resource.
        :param resource: The new resource.
        """
        if is_resource(resource):
            resource = resource.resource
        self.__resource = resource
        self.load(self.__force_check)

    @property
    def extension(self) -> str | None:
        """
        Gets the extension of the resource asset.
        :return: The extension if the loaded resource asset was a filepath, otherwise None
        """
        return self.__extension

    @property
    def type(self):
        """
        Gets the type of the resource.
        """
        return self.__type

    @property
    def size(self):
        """
        Gets the size of the resource.
        :return: Size object if the loaded resource was an image and its size was in `db`, otherwise None
        """
        if self.__size is None:
            return None
        return gallerynpy.Size.from_size(self.__size)

    @property
    def is_named(self):
        """
        Checks if the resource is named.

        That means, the resource type is `IMAGE` or `ANIMATION` and doesn't have extension.
        """
        return (self.is_image_type or self.is_animation_type) and self.extension is None

    @property
    def is_image_type(self):
        """
        Checks if the resource type is `IMAGE`
        """
        return self.type == ResourceTypes.IMAGE

    @property
    def is_video_type(self):
        """
        Checks if the resource type is `VIDEO`
        """
        return self.type == ResourceTypes.VIDEO

    @property
    def is_animation_type(self):
        """
        Checks if the resource type is `ANIMATION`
        """
        return self.type == ResourceTypes.ANIMATION

    @property
    def is_displayable_type(self):
        """
        Checks if the resource type is `DISPLAYABLE`
        """
        return self.type == ResourceTypes.DISPLAYABLE

    @property
    def is_none_type(self):
        """
        Checks if the resource type is `NONE`
        """
        return self.type == ResourceTypes.NONE

    def get_image(self):
        """
        Gets the image object of the resource.

        :raises ResourceForbiddenOperationError: if the resource type is not `IMAGE`.
        :raises ResourceNoLoadableError: If the resource filepath is not loadable.
        """
        if not self.is_image_type:
            raise ResourceForbiddenOperationError(self.type)

        if self.is_named:
            return gallerynpy.get_registered(self.resource)
        elif gallerynpy.is_image(self.resource):
            return self.resource
        elif gallerynpy.is_loadable(self.resource):
            return Image(self.resource)

        raise ResourceNoLoadableError(self.resource)

    def force_load_size(self):
        """
        Forces to load the image size of the resource.
        :raises ResourceForbiddenOperationError: if the resource type is not `IMAGE`.
        :raises ResourceNoLoadableError: If the resource filepath is not loadable.
        """
        if gallerynpy.is_size(self.__size):
            return

        image = self.get_image()
        width, height = image.load().get_size()
        self.__size = gallerynpy.Size(width, height)
        gallerynpy.db.put_size(self.resource, self.__size, named=self.is_named)

    def size_to(self, target: gallerynpy.Size):
        """
        Adjusts the current size to match the aspect ratio of the provided target size.
        :param target: The target size to match.
        :return: The adjusted size, or the target size if the resource doesn't have a `size`.
        :raises TypeError: If the target size is not a Size object.
        """
        if not gallerynpy.is_size(target):
            raise TypeError("The target size mut be a Size object")

        if self.__size is None:
            return target

        ratio = self.__size.aspect_ratio
        tratio = target.aspect_ratio
        if self.__size == target or ratio == tratio:
            return target
        elif ratio > tratio:
            return gallerynpy.Size(target.width, target.width / ratio)

        return gallerynpy.Size(target.height * ratio, target.height)

    def scale_to(self, target: gallerynpy.Size):
        """
        Creates an `im.Scale` object from the current resource according to the given size.
        :param target: The size to scale the resource.
        :return: The `im.Scale` object.
        :raises TypeError: If the target size is not a `Size` object.
        :raises ResourceForbiddenOperationError: if the resource type is not `IMAGE` or `DISPLAYABLE`.
        :raises ResourceNoLoadableError: If the resource filepath is not loadable.
        """
        if not gallerynpy.is_size(target):
            raise TypeError("The target size mut be a Size object")
        if self.is_displayable_type:
            image = self.resource
            size = target
        else:
            self.force_load_size()
            image = self.get_image()
            size = self.size_to(target)
        return im.Scale(image, size.width, size.height)

    def composite_to(self, target: gallerynpy.Size):
        """
        Creates a `Composite` object from the current resource,
        trying to center it according to the given size and the resource size.
        :param target: The size to composite the resource.
        :return: The `Composite` object.
        """
        if not gallerynpy.is_size(target):
            raise TypeError("The target size mut be a Size object")
        if self.is_displayable_type or self.is_animation_type:
            image = self.resource
            size = target
        else:
            self.force_load_size()
            size = self.size_to(target)
            image = self.scale_to(target)
        x = int(target.width / 2.0 - size.width / 2.0)
        return Composite((target.width, target.height), (x, 0), image)

    def __repr__(self):
        return "<Resource of '{}' is '{}'>".format(self.resource, self.type)


class Thumbnail:
    """
    Handles the creation of thumbnails for the different types of `Resource`.
    """

    def __init__(self, resource: Resource | str, size: gallerynpy.Size):
        """
        :param resource: The resource object, or an object for instance the resource.
        :param size: The size of the thumbnail dimensions.
        """
        if not isinstance(resource, Resource):
            resource = Resource(resource)
        self.__resource = resource
        self.__custom = None
        self.size = size

    @property
    def size(self) -> gallerynpy.Size:
        """
        Gets the size of the thumbnail.
        :return:
        """
        return self.__size

    @size.setter
    def size(self, size: gallerynpy.Size):
        """
        Sets the size of the thumbnail.

        It changes the self `size` reference to the new size object.
        :param size: The new size object to set.
        """
        if gallerynpy.is_size(size):
            self.__size = size

    @property
    def resource(self):
        """
        Gets the resource of the thumbnail.

        :return: The custom resource if was set, otherwise the initial resource.
        """
        return self.__resource if self.__custom is None else self.__custom

    def create(self):
        """
        Create a thumbnail `displayable` for the current thumbnail `resource`.

        See also `Resource.composite_to`

        If the `resource` is not valid, the `gallerynpy.properties.not_found` resource will be used.
        """
        resource = self.resource
        if resource.is_video_type and resource.extension:
            for ext in gallerynpy.properties.video_thumbnail_extensions:
                name = resource.resource.replace(resource.extension, ext)
                path = gallerynpy.join_path(gallerynpy.properties.thumbnails_folder, name, for_renpy=True)
                if gallerynpy.is_loadable(path):
                    return Resource(path).composite_to(self.size)
            resource = gallerynpy.properties.not_found
        elif not (resource.is_image_type or resource.is_displayable_type):
            resource = gallerynpy.properties.not_found

        return resource.composite_to(self.size)

    def set_custom(self, resource):
        """
        Set the given `resource` as custom.

        It will not change the initial resource.
        :param resource:
        :return:
        """
        if resource is None:
            self.__custom = None
        elif self.__custom is None:
            self.__custom = Resource(resource, gallerynpy.properties.force_loader)
        else:
            self.__custom.resource = resource

    def __repr__(self):
        return "<Thumbnail of {} with {}>".format(self.resource, self.size)
