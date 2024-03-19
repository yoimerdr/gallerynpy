Gallerynpy Properties
=====================

Gallerynpy uses multiple values accessible from **gallerynpy.properties** to configure and/or style the screens to be displayed.
The properties that can be accessed are shown below.

Style Properties
----------------

To customize the screen where the gallery is displayed, you can do it directly in the **screens.rpy** file by modifying
the code to your liking. But if you don't want to make big changes, and you only want to change some styles as
colours or background of the gallery, you can do this by changing the value of the following properties.

.. multi-directive::
    :directive: autorenstoredprop
    :source: gallerynpy.Properties
    :items: font, font_size, color, hover_color, selected_color, insensitive_color, navigation_background, menu_bg, menu,
        spacing, item_xspacing, navigation_position, navigation_yalign, navigation_xsize, navigation_slides_ysize,
        navigation_slides_bar_position, navigation_slides_bar_xpos, navigation_slides_bar_xsize

Item Properties
---------------

You can configure images (or viewables) for gallery item thumbnails such as **blocked** and **image not found**,
or special overlays such as **play icon** for videos or animations.

.. multi-directive::
    :directive: autorenstoredprop
    :source: gallerynpy.Properties
    :items: not_found, locked, idle, play_idle, play_hover, thumbnails_folder


Configuration Properties
------------------------

You can set some parameters to change the behavior of some functions in gallerynpy.

.. multi-directive::
    :directive: autorenstoredattr
    :source: gallerynpy.Properties
    :items: force_loader, sort_slides, keep_loaded, rescale_images, load_in_put, with_speed, animation_speed

Other Properties
----------------

There are also other properties which, although not editable, may be useful.

.. multi-directive::
    :directive: autorenstoredprop
    :source: gallerynpy.Properties
    :items: version, video_thumbnail_extensions

