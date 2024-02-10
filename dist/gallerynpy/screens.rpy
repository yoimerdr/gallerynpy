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
    add gallerynpy.properties.menu_bg.composite_to(gallerynpy.screen_size())
    add "gallerynpy_bg_overlay"
    add gallerynpy.properties.menu.composite_to(gallerynpy.screen_size())
    text _("Gallerynpy v[gallerynpy.properties.version]"):
        style "gallerynpy_version"
    hbox:
        spacing gallerynpy.properties.frame_content_spacing
        if gallerynpy.properties.frame_position == 'r':
            use gallerynpy_content
            use gallerynpy_sliders
        else:
            use gallerynpy_sliders
            use gallerynpy_content
            
    use gallerynpy_tooltip(gallerynpy.tooltip()) 


screen gallerynpy_content():
    $ columns, rows = gallerynpy.distribution()
    grid columns rows:
        yfill True
        xfill gallerynpy.properties.frame_position != 'r'
        if gallerynpy.properties.frame_position == 'r':
            xspacing gallerynpy.properties.item_xspacing

        for btn in gallerynpy.page_buttons():
            add btn
        

screen gallerynpy_pages():
    side "c " + gallerynpy.properties.pages_bar_position + " b":
        spacing gallerynpy.properties.pages_spacing
        viewport id "gallerynpy_pages":
            ysize gallerynpy.properties.pages_ysize
            mousewheel True
            draggable True

            if gallerynpy.properties.show_pages_bar:
                yadjustment gallerynpy.properties.adjustment

            has vbox
            for slide in gallerynpy.content_slides():
                $ item = gallerynpy.name_for(slide)
                textbutton _("[item!t]"):
                    selected gallerynpy.is_current(slide)
                    action gallerynpy.change_slide_to(slide)
                    

        
        if gallerynpy.properties.show_pages_bar:
            vbar:
                value YScrollValue("gallerynpy_pages")
                style "gallerynpy_vscrollbar"
        else:
            null

        vbox:
            null height 35
            use gallerynpy_options

screen gallerynpy_sliders():
    frame:
        style "gallerynpy_frame"
        has vbox
        style_prefix "gallerynpy"
        xpos gallerynpy.properties.frame_xpos
        spacing gallerynpy.properties.spacing
        if gallerynpy.properties.with_speed and gallerynpy.is_for_animations():
            use gallerynpy_anim_speeds
            use gallerynpy_options(True)
        else:
            use gallerynpy_pages 
         


screen gallerynpy_options(from_animation_options=False):
    textbutton _("Previous"):
        action gallerynpy.previous_page()
    textbutton _("Next"):
        action gallerynpy.next_page()
    textbutton _("Return"):
        action gallerynpy.back(from_animation_options)


screen gallerynpy_anim_speeds():
    vbox:
        text "Velocity:"
        hbox:
            textbutton "x1" action SetVariable("gallerynpy.properties.animation_speed", 1)
            textbutton "x2" action SetVariable("gallerynpy.properties.animation_speed", 2)
            textbutton "x3" action SetVariable("gallerynpy.properties.animation_speed", 3)
            textbutton "x4" action SetVariable("gallerynpy.properties.animation_speed", 4)