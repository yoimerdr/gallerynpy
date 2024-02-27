from .ui import *
from .persistent import *
from .renpy import *


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
    def __init__(self, callable, *args, **kargs):
        pass


class Call:
    def __init__(self, label, *args, **kargs):
        pass


class Play:
    def __init__(self, canal, resource):
        pass


class Stop:
    def __init__(self, canal):
        pass


class Null:
    pass


class NullAction:
    pass


class Return:
    pass


class Gallery:
    def image(self, displayable, *args, **kargs):
        pass

    def condition(self, condition, *args, **kargs):
        pass

    def button(self, name, *args, **kargs):
        pass

    def make_button(self, name, disp, *args, **kargs) -> Button:
        pass


dissolve = None
