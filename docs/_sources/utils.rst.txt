Utils
=====

Utils Functions
---------------

.. multi-directive::
    :source: gallerynpy
    :directive: autorenstoredfunc
    :items: or_default, gamepath, join_path, file, get_registered, make_dir, split_folders, file_extension, normalize_path,
            images_path, is_loadable, is_image, is_animation, is_hex_color, normalize_color, width_ratio, is_size, is_item,
            is_slide, is_slider

Util Classes
------------

.. autorenstoredcls:: gallerynpy.Singleton

Utils Variables
---------------

.. py:attribute:: gallerynpy.screen_size
    :type: ~gallerynpy.Size

    The size of the configured game screen. A reassignment is not recommended.

.. py:attribute:: gallerynpy.custom_names
    :type: dict

    The dic with the custom names for the slides or sliders. A reassignment or a direct set is not recommended.

.. py:attribute:: gallerynpy.RENPY_SEP
    :type: str

    The sep character that renpy use as path separator