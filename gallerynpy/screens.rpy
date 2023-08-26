screen gallerynpy_tooltip(tooltip):
    if tooltip:
        frame:
            style_prefix "gallerynpy_tooltip"
            style "gallerynpy_tooltip"
            background None
            text "[tooltip!t]":
                xalign 0.5


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
            
    use gallerynpy_tooltip(gallerynpy.tooltip()) 


screen gallerynpy_content():
    grid gallerynpy.columns() gallerynpy.rows():
        yfill True
        xfill gallerynpy_properties.frame_position != 'r'
        if gallerynpy_properties.frame_position == 'r':
            xspacing gallerynpy_properties.item_xspacing
        for index in range(gallerynpy.start(), gallerynpy.end() + 1):
            add gallerynpy.make_current_button_at(index)
            
        for index in range(gallerynpy.end() - gallerynpy.start() + 1, gallerynpy.max_items()):
            null

screen gallerynpy_pages():
    side "c " + gallerynpy_properties.pages_bar_position + " b":
        spacing gallerynpy_properties.pages_spacing
        viewport id "gallerynpy_pages":
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
            vbar:
                value YScrollValue("gallerynpy_pages")
                style "gallerynpy_vscrollbar"
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