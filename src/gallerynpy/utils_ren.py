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
    "or_default",
    "_RENPY_SEPARATOR"
)


"""renpy
init -4 python in gallerynpy:
"""

import os
import re
import errno
from store import renpy

_RENPY_SEPARATOR = "/"


class Singleton(object):
    """
    A class to simulate a `singleton`.

    Each class that inherits from this one will only have a single instance.
    """
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls)
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


def or_default(obj, default=None):
    """
    Checks if `obj` is not None and returns it.
    :param obj: The object to check
    :param default: Default value to return.
    :return: `obj` if it is not None, otherwise `default`
    """
    return default if obj is None else obj


def gamepath():
    """
    Gets the absolute path to the game `game` folder.
    """
    return join_path(renpy.config.basedir, "game")


def join_path(first: str, *args: str, **kwargs):
    """
    Joins the given paths.
    :param first: The initial path
    :param args: The other paths to joint with.
    :param kwargs: Only the variable keyword `from_renpy` will be taken.
    If it is `True`, the system path separator is replaced by the one used by renpy
    :return: The joined path.
    """
    joined = os.path.join(first, *args)
    for_renpy = kwargs.get("for_renpy", False)
    if for_renpy:
        return joined.replace(os.sep, _RENPY_SEPARATOR)
    return joined


def file(path: str, mode: str = "r", encoding: str = "utf-8", from_game: bool = False):
    """
    Open a file with the given mode.
    :param path: The path to the file.
    :param mode: The mode to open the file.
    :param encoding: The encoding of the file.
    :param from_game: If `True`, the `path` will be joined to the absolute path of `gamepath`.
    :return: The opened file.
    """
    path = str(path)
    if from_game:
        path = join_path(gamepath(), path)

    return open(path, mode, encoding=encoding)


def get_registered(name: str):
    """
    Gets the registered image (simple or animation like) in the game.

    See also `renpy.get_registered_image` in the documentation of renpy
    :param name: The name given to the image in the statement.
    :return: The registered image if exists, else `None`
    """
    if name is None:
        raise ValueError("Cannot get the registered image of None")
    name = str(name)
    return renpy.get_registered_image(name)


def make_dir(path: str, from_game: bool = False):
    """
    Create a leaf directory and all intermediate ones.

    See also `os.makedirs`
    :param path: The path to create.
    :param from_game: If `True`, the `path` will be joined to the absolute path of `gamepath`.
    """
    path = str(path)
    if from_game:
        path = join_path(gamepath(), path)

    try:
        return os.makedirs(path, exist_ok=True)
    except TypeError:
        pass
    try:
        return os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        if os.path.isfile(path):
            raise


def split_folders(path: str):
    """
    Splits the given path into their folders.

    :param path: The path to split.
    :return: A tuple containing a list of the split path, and the last folder name.
    """
    path = normalize_path(str(path))
    folder, last = os.path.split(path)
    return folder.split(os.sep), last


def file_extension(path: str):
    """
    Gets the file extension of the given path.

    See also `os.path.splitext`
    :param path: The file path
    :return: The file extension of the path.
    """
    if not path:
        raise ValueError('Path cannot be empty')
    path = str(path)
    _, extension = os.path.splitext(path)
    return extension


def normalize_path(path: str, for_renpy: bool = False):
    """
    Normalizes the given path.

    See also `os.path.normpath`
    :param path: The path to normalize
    :param for_renpy: If `True`, the system path separator is replaced by the one used by renpy
    :return: The normalized path.
    """
    if path is None:
        return ""
    path = os.path.normpath(str(path))
    if for_renpy:
        return path.replace(os.sep, _RENPY_SEPARATOR)
    return path


def images_path(first: str, *args, **kwargs):
    """
    Join the given paths to the `gallerynpy` or game `images` folder.
    :param first: The first path to append
    :param args: The other paths to append with.
    :param kwargs: Only the variable keyword `from_renpy` will be taken.
    If `True`, the paths will be appended to the `images` folder of the game,
    otherwise to the gallerynpy images folder.
    :return: The joined path.
    """
    from_renpy = kwargs.get("from_renpy", False)
    if from_renpy:
        return join_path("images", first, *args, for_renpy=True)

    return join_path("gallerynpy", "images", first, *args, for_renpy=True)


def is_loadable(path: str, extensions: tuple | list[str] | None = None):
    """
    Checks if the given path is loadable.

    See also `renpy.loadable`
    :param path: The path to the file.
    :param extensions: Extensions with which the path should end.
    :return: True if the path is loadable and ends with extensions (if present), False otherwise
    """
    if not path:
        return False

    path = str(path)
    if extensions and not path.endswith(extensions):
        return False

    return renpy.loadable(path)


def is_image(obj):
    """
    Checks if the given object is an image.

    Any instance of `renpy.display.im.Image` (or simply `im.Image` or `Image`)
    or inheriting from it is considered an image.
    :param obj: The object to check.
    :return: True if the object is an image, False otherwise.
    """
    return isinstance(obj, renpy.display.im.Image)


def is_animation(obj):
    """
    Checks if the given object is an animation.

    Any instance of `renpy.display.transform.ATLTransform`
    or inheriting from it is considered an animation.
    :param obj: The object to check.
    :return: True if the object is an animation, False otherwise
    """
    return isinstance(obj, renpy.display.transform.ATLTransform)


def is_hex_color(color: str):
    """
    Checks if the given color is a hexadecimal.
    :param color: The string to check
    :return: True if the string matches the hexadecimal color format, False otherwise
    """
    return re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}(?:[0-9a-fA-F]{2})?$', color) is not None


def normalize_color(hex_color: str) -> str:
    """
    Normalizes the given hexadecimal color.

    Normalization refers to completing the channels so that they can have
    the 6 or 8 values of a normal hexadecimal color.
    :param hex_color: The color to normalize.
    :return: The normalized color.
    """
    if hex_color is None:
        raise ValueError('The hexadecimal color cannot be None')

    hex_color = str(hex_color)
    color = hex_color if hex_color[0] == "#" else "#" + hex_color
    size = len(color)
    if size == 5 or size == 8:
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

    out = "#" + red + green + blue
    if alpha:
        out += alpha
    return out.upper()
