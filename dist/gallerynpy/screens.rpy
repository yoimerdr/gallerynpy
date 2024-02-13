screen gallerynpy():
    tag menu
    $ gallerynpy.update()
    style_prefix "game_menu"
    add gallerynpy.properties.menu_bg.composite_to(gallerynpy.screen_size())
    add gallerynpy.properties.menu.composite_to(gallerynpy.screen_size())
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
    $ columns, rows = gallerynpy.distribution()
    grid columns rows:
        style "gallerynpy_items"
        xspacing gallerynpy.properties.item_xspacing
        for btn in gallerynpy.page_buttons():
            add btn

screen gallerynpy_slides_options(show_bar=True):
    # gallerynpy.properties.slides_bar_position
    side "c " + gallerynpy.properties.navigation_slides_bar_position:
        # gallerynpy.properties.slides_spacing
        viewport id "gallerynpy_slides_options":
            style "gallerynpy_slides"
            mousewheel True
            draggable True

            if show_bar:
                yadjustment gallerynpy.properties.navigation_slides_adjustment

            has vbox
            for slide in gallerynpy.content_slides():
                $ item = gallerynpy.name_for(slide)
                textbutton _("[item!t]"):
                    selected gallerynpy.is_current(slide)
                    action gallerynpy.change_slide_to(slide)

        if show_bar:
            vbar:
                value YScrollValue("gallerynpy_slides_options")
                style "gallerynpy_vscrollbar"
        else:
            null


screen gallerynpy_animations_options():
    vbox:
        text "Velocity:"
        hbox:
            textbutton "x1" action SetVariable("gallerynpy.properties.animation_speed", 1)
            textbutton "x2" action SetVariable("gallerynpy.properties.animation_speed", 2)
            textbutton "x3" action SetVariable("gallerynpy.properties.animation_speed", 3)
            textbutton "x4" action SetVariable("gallerynpy.properties.animation_speed", 4)

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
                xalign 0.0
            background None
            text "[tooltip!t]":
                xalign 0.5