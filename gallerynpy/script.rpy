label gallerynpy_cinema(movie=None, song=None):
    if song:
        $ renpy.music_start(song)

    if not movie is None:
        $ renpy.movie_cutscene(movie, loops=-1, stop_music=song is None)

    if song:
        $ renpy.music_stop()

    call screen gallerynpy
    return
