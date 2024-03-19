# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os
import datetime

sys.path.append(os.path.abspath(''))

project = 'gallerynpy'
copyright = '2023-{}, Yoimer Davila'.format(datetime.date.today().year)
author = 'Yoimer Davila'
release = '2.0'
version = release + " Documentation"

html_title = project.capitalize() + " Documentation"

extensions = [
    'sphinx.ext.todo',
    'renpydoc',
    'sphinx.ext.autodoc',
    'sphinx_rtd_theme',
    "title_as_you_type",
    "extensions.multi_directive",
    "extensions.py_autodoc",
    "extensions.renpy_autodoc",
]

rst_prolog = """
.. |br| raw:: html

   <br />
"""

# html_file_suffix = ''

lunrsearch_highlight = True

highlight_language = "renpy"

pygments_style = 'default'

html_css_files = [
    'css/custom.css',
    "css/font-jb-sans.css"
]
html_js_files = [
    "js/custom.js"
]

templates_path = [
    '_templates'
]

locale_dirs = ["locale/"]

exclude_patterns = []

source_suffix = '.rst'

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']

html_theme_options = {
    'sticky_navigation': False
}

master_doc = 'index'

html_show_sourcelink = False

html_permalinks = True

autoclass_content = 'both'

html_favicon = "img/favicon.ico"
html_logo = "img/navbar-logo.png"


def generic_reference(name, targets, source=None, same_source=False):
    def check_target(item):
        if isinstance(item, str):
            if source:
                return name, item, source
            return name, item
        elif isinstance(item, (tuple, list)):
            if len(item) == 2:
                if source and same_source:
                    src = "{}.{}".format(source, item[1])
                    return name, item[0], src, True
                return name, item[0], item[1], True
        raise TypeError("Invalid parameter value: {}".format(item))

    return tuple(map(check_target, targets))


def class_reference(targets, source=None, same_source=False):
    return generic_reference("class", targets, source, same_source)


def met_reference(targets, source=None, same_source=False):
    return generic_reference("met", targets, source, same_source)


def attr_reference(targets, source=None, same_source=False):
    return generic_reference("attr", targets, source, same_source)


def func_reference(targets, source=None, same_source=False):
    return generic_reference("func", targets, source, same_source)


def exc_reference(targets, source=None, same_source=False):
    return generic_reference("exc", targets, source, same_source)


renpy_stored_config = {
    "module": "gallerynpy",
    "class_module": (
        ("Properties",),
        ("Handler",),
        ("SizesDb", "db")
    ),
    "references": [
        *class_reference(("Resource",), "resources"),
        *exc_reference((
            "ResourceNameNotFoundError",
            "ResourceForbiddenOperationError",
            "UnsupportedResourceTypeError",
            "ResourceNoLoadableError",
        ), "resources"),
        *class_reference(("Slide", "Slider", "Item", "Size")),
        *attr_reference(("VIDEO", "IMAGE", "DISPLAYABLE", "NONE", "ANIMATION"), "resources.ResourceTypes"),
        *func_reference(("put_item", "create_item", "put_slide_like",)),
        *attr_reference(("db",)),
        *attr_reference((
            ("gallerynpy.properties.load_in_put", "load_in_put"),
            ("gallerynpy.properties.not_found", "not_found"),
            ("gallerynpy.properties.animation_speed", "animation_speed"),
        ), source="gallerynpy.properties", same_source=True),
        *func_reference((
            ("Resource.composite_to", "composite_to"),
        ), "gallerynpy.resources.Resource", same_source=True),
        *attr_reference((
            ("Item.meets_condition", "meets_condition"),

        ), "gallerynpy.Item", same_source=True),
        *func_reference((
            ("gallerynpy.animation_speed()", "animation_speed"),
            ("gamepath", "gamepath")
        ), "gallerynpy", same_source=True)
    ],
    "enum_classes": [
        "resources.ResourceTypes",
    ]
}

autodoc_member_order = "groupwise"
