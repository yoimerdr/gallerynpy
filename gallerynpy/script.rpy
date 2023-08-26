label gallerynpy_cinema(movie=None, song=None):
    if song:
        $ renpy.music_start(song)

    if not movie is None:
        $ renpy.movie_cutscene(movie, loops=-1, stop_music=song is None)

    if song:
        $ renpy.music_stop()

    call screen gallerynpy
    return

label gallerynpy_rescale(to_gallery=False):
    if not persistent.gallerynpy_rescale_screen and not to_gallery:
        call screen gallerynpy_rescale_screen
    else:
        if to_gallery:
            $ persistent.gallerynpy_rescale_image = False
        call screen gallerynpy
    return
