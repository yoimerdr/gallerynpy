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

screen gallerynpy():
    tag menu
    $ gallerynpy.update()
    style_prefix "game_menu"
    add gallerynpy.properties.menu_bg.composite_to(gallerynpy.screen_size)
    add gallerynpy.properties.menu.composite_to(gallerynpy.screen_size)
    text _("Gallerynpy v[gallerynpy.properties.version]"):
        style "gallerynpy_version"
        if gallerynpy.properties.navigation_position == "r":
            xalign 0.0

    hbox:
        xfill True
        spacing gallerynpy.properties.spacing
        if gallerynpy.properties.navigation_position == 'l':
            use gallerynpy_navigation
            use gallerynpy_items
        else:
            use gallerynpy_items
            use gallerynpy_navigation



    use gallerynpy_tooltip(gallerynpy.tooltip())


screen gallerynpy_navigation():
    frame:
        style "gallerynpy_navigation"
        has vbox
        style_prefix "gallerynpy"
        spacing gallerynpy.properties.spacing
        if gallerynpy.properties.with_speed and gallerynpy.is_for_animations():
            use gallerynpy_animations_options
            use gallerynpy_pages_options(True)
        else:
            use gallerynpy_slides_options
            use gallerynpy_pages_options

screen gallerynpy_items():
    grid gallerynpy.cols() gallerynpy.rows():
        style "gallerynpy_items"
        xspacing gallerynpy.properties.item_xspacing
        for btn in gallerynpy.page_buttons():
            add btn

screen gallerynpy_slides_options():
    side "c " + gallerynpy.properties.navigation_slides_bar_position:
        viewport id "gallerynpy_slides_options":
            style "gallerynpy_slides"
            mousewheel True
            draggable True

            if gallerynpy.properties.navigation_slides_show_bar:
                yadjustment gallerynpy.properties.navigation_slides_adjustment

            has vbox
            for slide in gallerynpy.content_slides():
                $ item = gallerynpy.name_for(slide)
                textbutton _("[item!t]"):
                    selected gallerynpy.is_current(slide)
                    action gallerynpy.change_slide_to(slide)

        if gallerynpy.properties.navigation_slides_show_bar:
            vbar:
                value YScrollValue("gallerynpy_slides_options")
                style "gallerynpy_vscrollbar"
        else:
            null


screen gallerynpy_animations_options():
    vbox:
        text "Velocity:"
        hbox:
            textbutton "x1" action gallerynpy.actions.ChangeAnimationSpeed(1)
            textbutton "x2" action gallerynpy.actions.ChangeAnimationSpeed(2)
            textbutton "x3" action gallerynpy.actions.ChangeAnimationSpeed(3)
            textbutton "x4" action gallerynpy.actions.ChangeAnimationSpeed(4)

screen gallerynpy_pages_options(from_animation_options=False):
    vbox:
        xfill True
        textbutton _("Previous"):
            action gallerynpy.previous_page()
        textbutton _("Next"):
            action gallerynpy.next_page()
        textbutton _("Return"):
            action gallerynpy.back(from_animation_options)

screen gallerynpy_tooltip(tooltip):
    if tooltip:
        frame:
            style_prefix "gallerynpy_tooltip"
            style "gallerynpy_tooltip"
            if gallerynpy.properties.navigation_position == "r":
                xalign 1.0
            background None
            text "[tooltip!t]":
                xalign 0.5