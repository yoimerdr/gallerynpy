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
init -4 python in gallerynpy:
# docstring:1
The gallerynpy stored module.
from store import gallerynpy
"""

import json


def is_size(obj):
    """
    Checks if the given object is instance of `Size`

    :param obj: The object to check.
    """
    return isinstance(obj, Size)


class Size:
    """
    Represents the dimensions (integers) of an image.
    """

    def __init__(self, width: int, height: int):
        """
        :param width: The width dimension.
        :param height: The height dimension.
        """
        self.__width = 0
        self.__height = 0

        self.width = width
        self.height = height

    @property
    def width(self):
        """
        Gets the width of the size.
        """
        return self.__width

    @width.setter
    def width(self, width: int):
        """
        Sets the width of the size.
        This value must be a positive integer.
        """
        width = int(width)
        if width < 0:
            raise ValueError('A dimension cannot be negative')
        self.__width = width

    @property
    def height(self) -> int:
        """
        Gets the height of the size.
        """
        return self.__height

    @height.setter
    def height(self, height: int):
        """
        Sets the height of the size.
        This value must be a positive integer.
        """
        height = int(height)
        if height < 0:
            raise ValueError('A dimension cannot be negative')
        self.__height = height

    def set(self, size: "Size"):
        """
        Sets the actual dimensions to those of the given size.
        :raises TypeError: If the given size not is an instance of Size.
        :param size: The size object with the new dimensions.
        """
        if not is_size(size):
            raise TypeError("Invalid size to set")
        self.width = size.width
        self.height = size.height

    @staticmethod
    def from_size(size: "Size") -> "Size":
        """
        Creates a new size object from the given size.
        :param size: The size object
        :raises TypeError: If the given size not is an instance of Size.
        :return: The new size object.
        """
        if not is_size(size):
            raise TypeError('The size must be an instance of Size')
        return Size(size.width, size.height)

    @property
    def aspect_ratio(self):
        """
        Gets the aspect ratio of the current dimensions.

        Calculated as `width / height`.

        :return: The calculated aspect ratio.
        """
        if self.height == 0:
            return 0.0
        return float(self.width) / self.height

    def __eq__(self, other):
        if not is_size(other):
            return False
        return self.width == other.width and self.height == other.height

    def __repr__(self):
        return "<Size of {}x{}>".format(self.width, self.height)


class SizesDb(gallerynpy.Singleton):
    """
    A dumb json db for save the image dimensions.
    It inherits from Singleton, so there will be only one instance of it.
    """
    NAMED = "SizesDbNamed"

    def __init__(self, basename: str, folder: str):
        """
        :param basename: The base name of the json file. e.g. `images.json`
        :param folder: The folder path where the json file is. Must be relative to the game folder of the game.
        """
        self.__folder = str(folder)
        self.__basename = str(basename)
        self.__source = gallerynpy.join_path(self.__folder, self.__basename)
        self.__sizes = {}
        self.__save = False
        try:
            with gallerynpy.file(self.__source, from_game=True) as fs:
                self.__sizes = json.load(fs)
        except:
            pass

    def __get_size(self, path: str) -> Size | None:
        target = self.__sizes
        folders, name = gallerynpy.split_folders(path)

        for folder in folders:
            if folder not in target.keys():
                return None
            target = target[folder]

        if name in target.keys():
            if len(target[name]) != 2:
                return None

            return Size(target[name][0], target[name][1])

        return None

    def get_size(self, path: str, named: bool = False, folder: str = None) -> Size | None:
        """
        Gets from the json object the size for the given path.
        :param path: The image filepath or image name.
        :param named: If true, the path is considered as an image name.
        :param folder: The base folder of the path. If given, will be joined with the `path` param.
        :return: The size for the `path` or None if it doesn't present.
        """
        if named:
            folder = SizesDb.NAMED
        if folder:
            path = gallerynpy.join_path(folder, path)

        return self.__get_size(path)

    def put_size(self, path: str, size: Size, named: bool = False, folder: str = None):
        """
        Puts from the json object the size for the given path.
        :param path: The image filepath or image name.
        :param size: The image size to put.
        :param named: If true, the path is considered as an image name.
        :param folder: The base folder of the path. If given, will be joined with the `path` param.
        """
        if not is_size(size):
            return

        if named:
            folder = SizesDb.NAMED

        if folder:
            path = gallerynpy.join_path(folder, path)

        folders, name = gallerynpy.split_folders(path)
        target = self.__sizes
        for folder in folders:
            if folder and folder not in target.keys():
                target[folder] = {}
            target = target[folder]

        self.__save = name not in target.keys() if not self.__save else self.__save
        target[name] = [size.width, size.height]

    def contains(self, path: str, named: bool = False, folder: str = None) -> bool:
        """
        Checks if there is a size for the given path.
        :param path: The image filepath or image name.
        :param named: If true, the path is considered as an image name.
        :param folder: The base folder of the path. If given, will be joined with the `path` param.
        """
        return self.get_size(path, named, folder) is not None

    def save(self):
        """
        Saves the current json object as a json file.
        """
        if self.__save:
            try:
                gallerynpy.make_dir(self.__folder, from_game=True)
                with gallerynpy.file(self.__source, mode="w", encoding="utf-8", from_game=True) as fs:
                    json.dump(self.__sizes, fs)
                self.__save = False
            except:
                pass

    def __contains__(self, item):
        item = str(item)
        if "." not in item:
            item = gallerynpy.join_path(SizesDb.NAMED, item)
        return self.contains(item)

    def __str__(self):
        return str(self.__sizes)


db: SizesDb | None = None
"""
The only instance for the SizesDb class. A reassignment is not recommended.
"""

screen_size: Size | None = None
"""
The size of the configured game screen. A reassignment is not recommended.
"""
