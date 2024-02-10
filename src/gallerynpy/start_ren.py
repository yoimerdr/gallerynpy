import compat_ren as gallerynpy

"""renpy
init 9999 python:
"""
gallerynpy.load_named_resources()
gallerynpy.db.save()
gallerynpy.to_first_slide(gallerynpy.properties.sort_slides)
