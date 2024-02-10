image gallerynpy_bg_overlay:
    gallerynpy.properties.background.composite_to(gallerynpy.screen_size())
    zoom gallerynpy.scaling()


style gallerynpy:
    xalign 0.5
    yalign 0.46

style gallerynpy_xcenter:
    xalign 0.5

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
    xalign 1.0
    yalign 1.0
    ypadding 18
    xpadding 10

style gallerynpy_version is gallerynpy_tooltip
style gallerynpy_version:
    ypadding 2
    xpadding 2
    size 12

style gallerynpy_tooltip_text is gallerynpy_text

style gallerynpy_tooltip_text:
    outlines [(1, "#000000", 0, 0)]

style gallerynpy_rescaling:
    yalign 0.0
    xpos gallerynpy.properties.navigation_xpos

style gallerynpy_frame:
    yalign gallerynpy.properties.frame_yalign
    xsize gallerynpy.properties.frame_xsize
    background gallerynpy.properties.frame_color

style gallerynpy_rescale_frame is gallerynpy_frame

style gallerynpy_rescale_frame:
    yalign 0.0

style gallerynpy_vscrollbar is vscrollbar

style gallerynpy_vscrollbar:
    xsize gallerynpy.properties.pages_bar_xsize
    xpos -gallerynpy.properties.pages_bar_xpos