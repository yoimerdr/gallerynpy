screen gallerynpy_tooltip(tooltip):
    if tooltip:
        frame:
            style_prefix "gallerynpy_tooltip"
            style "gallerynpy_tooltip"
            background None
            text "[tooltip!t]":
                xalign 0.5

screen gallerynpy_rescaling():
    frame:
        style 'gallerynpy_rescale_frame'
        hbox:
            style_prefix "gallerynpy"
            style "gallerynpy_rescaling"
            text "Rescale:":
                color gallerynpy_properties.color
            spacing 10
            textbutton _("Yes"):
                action [SetVariable("persistent.gallerynpy_rescale_image", True), Call("gallerynpy_rescale")]
                tooltip "The mod will try to rescale the images to a correct aspect ratio"

            textbutton _("No"):
                action [SetVariable("persistent.gallerynpy_rescale_image", False), Call("gallerynpy_rescale", True)]
                tooltip "The mod will not try to rescale the images to a correct aspect ratio"
    use gallerynpy_tooltip(GetTooltip())


screen gallerynpy_rescale_screen():
    vbox:
        style_prefix "gallerynpy"
        style "gallerynpy"
        text "This option may affect the performance of the game at startup, since at startup" xalign 0.5
        text "the mod will try to rescale ALL IMAGES to a proper ratio and this can be slow." xalign 0.5
        text "For this option to do its job, you have to exit the game and re-enter." xalign 0.5
        text "Accept this option at your own risk." xalign 0.5
        text "This screen will not appear again either.\n" xalign 0.5

        hbox:
            style_prefix "gallerynpy"
            style "gallerynpy"
            textbutton _("Accept"):
                align(0.4,0.54)
                action [SetVariable("persistent.gallerynpy_rescale_screen", True), Call('gallerynpy_rescale')]
            textbutton _("Cancel"):
                align(0.6,0.54)
                action [Call("gallerynpy_rescale", True)]

screen gallerynpy():
    tag menu
    $ gallerynpy.update()
    ## Layout
    style_prefix "game_menu"
    add gallerynpy_properties.menu_bg
    add "gallerynpy_bg_overlay"
    add gallerynpy_properties.menu
    text _("Gallerynpy v[gallerynpy_properties.version]"):
        style "gallerynpy_version"
    hbox:
        spacing gallerynpy_properties.frame_content_spacing
        if gallerynpy_properties.frame_position == 'r':
            use gallerynpy_content
            use gallerynpy_sliders
        else:
            use gallerynpy_sliders
            use gallerynpy_content

    use gallerynpy_rescaling


screen gallerynpy_content():
    grid gallerynpy.columns() gallerynpy.rows():
        yfill True
        xfill gallerynpy_properties.frame_position != 'r'
        if gallerynpy_properties.frame_position == 'r':
            xspacing gallerynpy_properties.item_xspacing
        for index in range(gallerynpy.start(), gallerynpy.end() + 1):
            $ item = gallerynpy.make_current_button_at(index)
            if item:
                add item
            else:
                null
        for index in range(gallerynpy.end() - gallerynpy.start() + 1, gallerynpy.max_items()):
            null

screen gallerynpy_pages():
    side "c " + gallerynpy_properties.pages_bar_position + " b":
        spacing gallerynpy_properties.pages_spacing
        viewport:
            ysize gallerynpy_properties.pages_ysize
            mousewheel True
            draggable True

            if gallerynpy_properties.show_pages_bar:
                yadjustment gallerynpy_properties.adjustment

            has vbox
            for name in gallerynpy.slides(gallerynpy_properties.sort_slides):
                if gallerynpy.slide_size(name) > 0:
                    $ item = gallerynpy_names[name] if name in gallerynpy_names.keys() else name.capitalize()
                    textbutton _("[item!t]"):
                        selected gallerynpy.is_current_slide(name)
                        action [Function(gallerynpy.update, True), Function(gallerynpy.change_slide, name)]


        if gallerynpy_properties.show_pages_bar:
            bar:
                adjustment gallerynpy_properties.adjustment
                style "vscrollbar"
        else:
            null

        vbox:
            null height 35
            use gallerynpy_options(gallerynpy.return_action())

screen gallerynpy_sliders():
    frame:
        style "gallerynpy_frame"
        has vbox
        style_prefix "gallerynpy"
        xpos gallerynpy_properties.frame_xpos
        spacing gallerynpy_properties.spacing
        if persistent.gallerynpy_spedded and gallerynpy.is_current_animation_slide():
            use gallerynpy_anim_speeds
            use gallerynpy_options(gallerynpy.return_action(True))
        else:
            use gallerynpy_pages 
            


screen gallerynpy_options(return_action=Return()):
    textbutton _("Previous"):
        if gallerynpy.page() > 0:
            action Function(gallerynpy.change_page, gallerynpy.page() - 1)
    textbutton _("Next"):
        if (gallerynpy.page() + 1) * gallerynpy.max_items() < gallerynpy.current_slide_size():
            action Function(gallerynpy.change_page, gallerynpy.page() + 1)
    
    textbutton _("Return"):
        action return_action


screen gallerynpy_anim_speeds():
    vbox:
        text "Velocity:"
        hbox:
            textbutton "x1" action SetVariable("persistent.gallerynpy_animation_speed", 1)
            textbutton "x2" action SetVariable("persistent.gallerynpy_animation_speed", 2)
            textbutton "x3" action SetVariable("persistent.gallerynpy_animation_speed", 3)
            textbutton "x4" action SetVariable("persistent.gallerynpy_animation_speed", 4)