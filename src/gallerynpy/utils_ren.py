__all__ = (
    "Singleton",
    "gamepath",
    "join_path",
    "file",
    "file_extension",
    "is_loadable",
    "is_image",
    "is_animation",
    "is_hex_color",
    "get_registered",
    "split_folders",
    "normalize_path",
    "images_path",
    "make_dir",
    "normalize_color",
    "or_default"
)

"""renpy
init -4 python in gallerynpy:
"""

import os
import re
from store import renpy

RENPY_SEPARATOR = "/"


class Singleton(object):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls)
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


def or_default(obj, default=None):
    return default if obj is None else obj


def gamepath():
    return join_path(renpy.config.basedir, "game")


def join_path(first: str, second: str, *args: str, for_renpy: bool = False):
    joined = os.path.join(first, second, *args)
    if for_renpy:
        return joined.replace(os.sep, RENPY_SEPARATOR)
    return joined


def file(path: str, mode: str = "r", encoding: str = "utf-8", from_game: bool = False):
    path = str(path)
    if from_game:
        path = join_path(gamepath(), path)

    return open(path, mode, encoding=encoding)


def get_registered(name: str):
    name = str(name)
    return renpy.get_registered_image(name)


def make_dir(path: str, from_game: bool = False):
    path = str(path)
    if from_game:
        path = join_path(gamepath(), path)
    os.makedirs(path, exist_ok=True)


def split_folders(path: str):
    path = normalize_path(str(path))
    folder, last = os.path.split(path)
    return folder.split(os.sep), last


def file_extension(path: str):
    path = str(path)
    _, extension = os.path.splitext(path)
    return extension


def normalize_path(path: str, for_renpy: bool = False):
    if path is None:
        return ""
    path = os.path.normpath(str(path))
    if for_renpy:
        return path.replace(os.sep, RENPY_SEPARATOR)
    return path


def images_path(first: str, *args, from_renpy: bool = False):
    if from_renpy:
        return join_path("images", first, *args, for_renpy=True)

    return join_path("gallerynpy", "images", first, *args, for_renpy=True)


def is_loadable(path: str, extensions: tuple | list[str] | None = None):
    if not path:
        return False

    path = str(path)
    if extensions:
        if not path.endswith(extensions):
            return False

    return renpy.loadable(path)


def is_image(obj):
    return isinstance(obj, renpy.display.im.Image)


def is_animation(obj):
    return isinstance(obj, renpy.display.transform.ATLTransform)


def is_hex_color(color: str):
    """
    Checks if the given color is a hexadecimal.
    :param color: The string to check
    :return: True if the string matches the hexadecimal color format, False otherwise
    """
    return re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}(?:[0-9a-fA-F]{2})?$', color) is not None


def normalize_color(hex_color: str) -> str:
    color = hex_color if hex_color[0] == "#" else "#" + hex_color
    size = len(color)
    if size == 5:
        color += color[-1]
        size += 1
    if not is_hex_color(color):
        raise ValueError("The color must be hexadecimal.")

    if size == 7 or size == 9:
        return color

    red, green, blue, alpha = ("", "", "", None)

    def __get_simple_rgb() -> tuple[str, str, str]:
        return color[1] * 2, color[2] * 2, color[3] * 2

    if size == 4:
        red, green, blue = __get_simple_rgb()
    elif size == 6:
        alpha = color[-2:]
        red, green, blue = __get_simple_rgb()

    out = f"#{red}{green}{blue}"
    if alpha:
        out += alpha
    return out.upper()
