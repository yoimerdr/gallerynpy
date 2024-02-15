from utils_ren import Singleton, join_path, file, split_folders, make_dir

__all__ = (
    "Size",
    "is_size",
    "SizesDb",
    "db",
    "_screen_size"
)

"""renpy
init -2 python in gallerynpy:
"""
from store import config

try:
    import json as json_module
except ImportError:
    json_module = None
    pass


def is_size(obj):
    return isinstance(obj, Size)


class Size:
    def __init__(self, width: int, height: int):
        self.__width = 0
        self.__height = 0

        self.width = width
        self.height = height

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width: int):
        width = int(width)
        if width < 0:
            raise ValueError('A dimension cannot be negative')
        self.__width = width

    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def height(self, height: int):
        height = int(height)
        if height < 0:
            raise ValueError('A dimension cannot be negative')
        self.__height = height

    def set(self, size: "Size"):
        if not is_size(size):
            raise ValueError("Invalid size to set")
        self.width = size.width
        self.height = size.height

    @staticmethod
    def from_size(size: "Size") -> "Size":
        if not is_size(size):
            raise ValueError('The size must be an instance of Size')
        return Size(size.width, size.height)

    @property
    def aspect_ratio(self):
        if self.height == 0:
            return 0
        return float(self.width) / self.height

    def __eq__(self, other):
        if not is_size(other):
            return False
        return self.width == other.width and self.height == other.height

    def __repr__(self):
        return "<Size: " + str(self.width) + "x" + str(self.height) + ">"


class SizesDb(Singleton):
    NAMED = "SizesDbNamed"

    def __init__(self, basename: str, folder: str):
        self.__folder = str(folder)
        self.__basename = str(basename)
        self.__source = join_path(self.__folder, self.__basename)
        self.__sizes = {}
        self.__save = False
        try:
            with file(self.__source, from_game=True) as fs:
                self.__sizes = json_module.load(fs)
        except:
            pass

    def __get_size(self, path: str) -> Size | None:
        target = self.__sizes
        folders, name = split_folders(path)

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
        if named:
            folder = SizesDb.NAMED
        if folder:
            path = join_path(folder, path)

        return self.__get_size(path)

    def put_size(self, path: str, size: Size, named: bool = False, folder: str = None):
        if not is_size(size):
            return

        if named:
            folder = SizesDb.NAMED

        if folder:
            path = join_path(folder, path)

        folders, name = split_folders(path)
        target = self.__sizes
        for folder in folders:
            if folder and folder not in target.keys():
                target[folder] = {}
            target = target[folder]

        self.__save = name not in target.keys() if not self.__save else self.__save
        target[name] = [size.width, size.height]

    def contains(self, path: str) -> bool:
        return self.get_size(path) is not None

    def save(self):
        if self.__save:
            try:
                make_dir(self.__folder, from_game=True)
                with file(self.__source, mode="w", encoding="utf-8", from_game=True) as fs:
                    json_module.dump(self.__sizes, fs)
                self.__save = False
            except:
                pass

    def __contains__(self, item):
        item = str(item)
        if "." not in item:
            item = join_path(SizesDb.NAMED, item)
        return self.contains(item)

    def __str__(self):
        return str(self.__sizes)


db = SizesDb("images.json", join_path("gallerynpy", "db"))
_screen_size = Size(config.screen_width, config.screen_height)
