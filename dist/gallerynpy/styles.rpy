# Copyright © 2023-2024, Yoimer Davila
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

style gallerynpy_button_text:
    size gallerynpy.properties.font_size
    font gallerynpy.properties.font
    color gallerynpy.properties.color

style gallerynpy_text is gallerynpy_button_text

style gallerynpy_button_text:
    hover_color gallerynpy.properties.hover_color
    selected_color gallerynpy.properties.selected_color
    insensitive_color gallerynpy.properties.insensitive_color

style gallerynpy_tooltip:
    xalign 0.0
    yalign 0.0
    ypadding 18
    xpadding 10
    xsize gallerynpy.properties.navigation_xsize

style gallerynpy_version:
    xalign 1.0
    yalign 1.0
    ypadding 2
    xpadding 2
    size 12

style gallerynpy_tooltip_text is gallerynpy_text

style gallerynpy_tooltip_text:
    outlines [(1, "#000000", 0, 0)]

style gallerynpy_vscrollbar is vscrollbar

style gallerynpy_vscrollbar:
    xsize gallerynpy.properties.navigation_slides_bar_xsize
    xpos gallerynpy.properties.navigation_slides_bar_xpos

style gallerynpy_navigation:
    yalign gallerynpy.properties.navigation_yalign
    xsize gallerynpy.properties.navigation_xsize
    background gallerynpy.properties.navigation_background.resource

style gallerynpy_slides:
    ysize gallerynpy.properties.navigation_slides_ysize
    xfill True

style gallerynpy_items:
    yfill True
    xfill True
    xsize gallerynpy.screen_size.width - gallerynpy.properties.navigation_xsize
