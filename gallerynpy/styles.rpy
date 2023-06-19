image gallerynpy_bg_overlay:
    gallerynpy_properties.background_overlay
    zoom gallerynpy.scaling


style gallerynpy:
    xalign 0.5
    yalign 0.46

style gallerynpy_xcenter:
    xalign 0.5

style gallerynpy_button_text:
    size gallerynpy_properties.font_size
    font gallerynpy_properties.font
    color gallerynpy_properties.color

style gallerynpy_text is gallerynpy_button_text

style gallerynpy_button_text:
    hover_color gallerynpy_properties.hover_color
    selected_color gallerynpy_properties.selected_color
    insensitive_color gallerynpy_properties.insensitive_color

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
    xpos gallerynpy_properties.navigation_xpos

style gallerynpy_frame:
    yalign 0.992
    xsize 420
    background "#0005"