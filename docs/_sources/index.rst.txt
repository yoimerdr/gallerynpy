Welcome to gallerynpy's documentation!
======================================

Gallerynpy is a set of Ren'Py scripts that allows you to display a gallery screen in your visual novel.
The gallery screen displays all images, animations and videos that have been inserted through the methods provided by gallerynpy.

The gallerynpy 2.0 version adds new optimizations when adding items and loading them,
without forcing it at the start of the game and only creating the gallery items when they are needed,
so as not to take up too much memory space. Also, there is now compatibility between renpy versions using
python 3 (e.g. 8.x.x) and those using python 2.7 (e.g. 7.x.x),
so now gallerynpy can be used in most games without major problems.

This documentation is based on the features that gallerynpy has from version 2.0, if you are using an earlier version,
check the `readme of version 1.6 <https://github.com/yoimerdr/gallerynpy/tree/1.6.0>`_
which is the last one before the changes of 2.0.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   quickstart
   properties

.. toctree::
    :maxdepth: 1
    :caption: Gallerynpy Stored Resource

    gallerynpy
    sliders
    items
    handler
    db
    utils

.. toctree::
    :maxdepth: 1
    :caption: Resources Stored Module

    resources

.. toctree::
    :maxdepth: 1
    :caption: Actions Stored Module

    actions