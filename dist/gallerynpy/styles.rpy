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
    xsize gallerynpy.screen_size().width - gallerynpy.properties.navigation_xsize
