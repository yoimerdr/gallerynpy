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
init -5 python in gallerynpy.actions:
# docstring:1
The gallerynpy.actions stored module.
from store import gallerynpy
"""
from store import Action, renpy


class UpdateUI(Action):
    """
    A renpy action. Update the ui restarting the current interaction using `renpy.restart_interaction()`
    """
    def __init__(self):
        super(UpdateUI, self).__init__()

    def _update(self):
        renpy.restart_interaction()

    def __call__(self, *args, **kwargs):
        self._update()


class ChangeAnimationSpeed(UpdateUI):
    """
    A gallerynpy action. Change the current value of the animation speed.

    Only works for animations that use `gallerynpy.animation_speed()`.
    """
    def __init__(self, current):
        super(ChangeAnimationSpeed, self).__init__()
        self._current = int(current)

    def __call__(self, *args, **kwargs):
        gallerynpy.properties.animation_speed = self._current
        self._update()

    def get_selected(self):
        return self._current == gallerynpy.properties.animation_speed


class IncreaseAnimationSpeed(ChangeAnimationSpeed):
    """
    A gallerynpy action. Increase the current value of the animation speed by +1.

    Only works for animations that use `gallerynpy.animation_speed()`.
    """
    def __init__(self, max=4):
        """
        :param max: The max value for animation speed.
        """
        value = gallerynpy.properties.animation_speed + 1
        if value > max:
            value = max
        self._max = max
        super(IncreaseAnimationSpeed, self).__init__(value)

    def get_sensitive(self):
        return self._current < self._max

    def get_selected(self):
        return False


class DecreaseAnimationSpeed(ChangeAnimationSpeed):
    """
    A gallerynpy action. Decrease the current value of the animation speed by -1.

    Only works for animations that use `gallerynpy.animation_speed()`.
    """
    def __init__(self, min=1):
        value = gallerynpy.properties.animation_speed - 1
        if value < min:
            value = min

        self._min = min
        super(DecreaseAnimationSpeed, self).__init__(value)

    def get_sensitive(self):
        return self._current > self._min

    def get_selected(self):
        return False
