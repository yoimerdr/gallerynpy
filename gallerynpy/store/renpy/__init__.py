from .config import *
from .display import *


def loadable(path):
    return True


def get_registered_image(name):
    return Image(name)