from . import ui
from . import persistent
from . import config
from . import renpy


from .renpy.display import *


class Action:
    def get_sensitive(self):
        return True

    def get_selected(self):
        return False

    def __call__(self, *args, **kwargs):
        pass


class Solid(Displayable):
    def __init__(self, color):
        pass


class Composite:
    def __init__(self, size, positions, displayable):
        pass


class Button:
    def __init__(self, action):
        pass


class Function:
    def __init__(self, callable, *args, **kwargs):
        pass


class Call:
    def __init__(self, label, *args, **kwargs):
        pass


class Play:
    def __init__(self, canal, resource):
        pass


class Stop:
    def __init__(self, canal):
        pass


class Null:
    pass


class NullAction(Action):
    pass


class Return:
    pass


class Gallery:
    def image(self, displayable, *args, **kwargs):
        pass

    def condition(self, condition, *args, **kwargs):
        pass

    def button(self, name, *args, **kwargs):
        pass

    def make_button(self, name, disp, *args, **kwargs) -> Button:
        pass

dissolve = None

