# Gallerynpy logic
init python:
    import os

    # for try fix image size
    persistent.gallerynpy_rescale_image = False
    persistent.gallerynpy_rescale_screen = False

    # for animation speed
    persistent.gallerynpy_animation_speed = 1
    persistent.gallerynpy_spedded = True


    class GallerynpySize:
        def __init__(self, width, height):
            self.width = width
            self.height = height


    class GallerynpyExtensions:
        video_extensions = ('.webm', '.avi', '.mp4', '.wav', '.mkv', '.ogv')
        image_extensions = ('.png', '.jpg', '.web', '.jpeg', '.webp')


    class GallerynpyTypes:
        image = 'img'
        video = 'vdo'
        animation = 'anim'


    def is_image_path(path):
        try:
            head, tail = os.path.splitext(path)
            return tail in GallerynpyExtensions.image_extensions if tail else False
        except ValueError:
            return False


    def renpy_path(path):
        return path.replace('\\', '/')


    class GallerynpyProperties:
        def __init__(self):
            self.not_found_thumbnail = "images/gallerynpy/not_found.png"
            self.play_hover_overlay = "images/gallerynpy/play_hover_overlay.png"
            self.play_idle_overlay = "images/gallerynpy/play_idle_overlay.png"
            self.idle_overlay = "images/gallerynpy/idle_overlay.png"
            self.locked = "images/gallerynpy/locked.png"
            self.background_overlay = "images/gallerynpy/background_overlay.png"
            self.video_thumbnails_extension = ['_thumbnail.' + item for item in ['jpg', 'png']]
            self.thumbnail_folder = 'images/gallerynpy/thumbnails'
            self.common_pages = ['videos', 'animations', 'images']
            self.version = '1.0.1'
            self.font_size = 15
            self.font = "fonts/gallerynpy/JetBrainsMono-Bold.ttf"
            self.color = "#fff"
            self.hover_color = "#99ccff"
            self.selected_color = "#99ccff"
            self.insensitive_color = "#ffffff99"
            self.navigation_xpos = 45
            self.spacing = 5
            self.default_slide = 'images'
            self.pages_spacing = 0
            self.pages_ysize = 120
            self.adjustment = ui.adjustment()
            self.animation_slide = 'animations'
            self.show_pages_bar = False
            self.pages_bar_style = 'vscrollbar'


    gallerynpy_properties = GallerynpyProperties()


    class GalleryItem:
        def __init__(self, name, path, thumbnail_size, song=None, unlocked_condition=None):
            """
            constructor for a GalleryItem.
            Args:
                name: name of the item.
                path: image name or filepath to the image or video, if is an atl object, will be the name.
                thumbnail_size: GallerynpySize object to scale thumbnails.
                song: optional argument, it will be the path to the song that will be played when the item is displayed.
            """
            self.name = name
            self.path = path
            self.thumbnail = None
            self.type = None
            self.extension = os.path.splitext(path)[1]
            self.thumbnail_size = thumbnail_size
            self.song = song

            if self.extension in GallerynpyExtensions.image_extensions:
                self.type = GallerynpyTypes.image
                self.path = self.rescale_image()
            elif self.extension in GallerynpyExtensions.video_extensions:
                self.type = GallerynpyTypes.video

            self.thumbnail = self.create_thumbnail()

        def rescale_image(self):
            """
            If item type is GallerynpyTypes.image, rescale the image to screen size.
            If persistent.gallerynpy_rescale_image is True, it will rescale to a correct image ratio according to the screen size and image size.
            """
            if self.path is None:
                raise ValueError('the path cannot be None')
            if not self.type == GallerynpyTypes.image:
                raise ValueError('the type must be GallerynpyTypes.image')

            image = im.Image(self.path) if isinstance(self.path, str) else self.path
            if persistent.gallerynpy_rescale_image:
                width, height = image.load().get_size()
                ratio = width / height
                try:
                    if width == config.screen_width and height == config.screen_height:
                        return image
                    elif ratio == 16/9:
                        return im.Scale(image, config.screen_width, config.screen_height)
                    elif ratio > 16/9:
                        return im.Scale(image, config.screen_width, int(config.screen_width / ratio))
                    else:
                        return im.Scale(image, int(config.screen_height * ratio), config.screen_height)
                except:
                    pass
            return im.Scale(image, config.screen_width, config.screen_height)

        def create_thumbnail(self):
            """
            Creates a thumbnail if item type is GallerynpyTypes.video or GallerynpyTypes.image
            """
            if self.type:
                if self.type == GallerynpyTypes.video:
                    for extension in gallerynpy_properties.video_thumbnails_extension:
                        thumbnail_path = renpy_path(os.path.join(gallerynpy_properties.thumbnail_folder, self.path.replace(self.extension, extension)))
                        if renpy.loadable(thumbnail_path):
                            return self.scale(thumbnail_path)
                    return self.not_found()
                elif self.type == GallerynpyTypes.image:
                    return self.scale(self.path)

            return None

        def not_found(self):
            """
            Return a not found thumbnail rescaled to thumbnail_size
            """
            return self.scale(gallerynpy_properties.not_found_thumbnail)

        def scale(self, path):
            """
            Return a im.Scale object rescaled to thumbnail_size
            """
            return im.Scale(path, self.thumbnail_size.width, self.thumbnail_size.height)

        def create_animation_thumbnail(self, thumbnail_path):
            """
            Return a thumbnail for an animation.
            Args:
                thumbnail_path: The path for the animation thumbnail. Can be a filepath or a image name.
            """
            try:
                return self.scale(renpy.get_registered_image(thumbnail_path))
            except:
                if is_image_path(thumbnail_path):
                    return self.scale(thumbnail_path)

            return self.not_found()


    class Gallerynpy:
        def __init__(self, columns=3, rows=3, item_width=400, min_screen=1280, min_item_width=270):
            """
            constructor for Gallerynpy
            Args:
                columns: The number of columns in a slide.
                rows: The number of rows in a slide.
                item_width: thumbnail width for each GallerynpyItem.
                min_screen: The min config screen size to set item_width to min_item_width and columns and rows to 3
                min_item_width: The min thumbnail size if confing.screen_width is lower than min_screen
            """
            # navigation configuration
            self.start = 0
            self.end = 0
            self.columns = columns
            self.rows = rows

            # thumbnail size configuration
            width = item_width  # default width value
            ratio = 0.5625

            if config.screen_width <= min_screen:
                self.columns = 3 if self.columns > 3 else self.columns
                self.rows = 3 if self.rows > 3 else self.rows
                width = min_item_width

            self.scaling = config.screen_width / float(min_screen)
            self.navigation_width = int(290 * self.scaling)
            self.page = 0

            self.thumbnail_size = GallerynpySize(width, int(width * 0.5625))  # change the 0.5625 according a image scale
            self.max_in_page = self.columns * self.rows  # number of items in one page

            # Gallery
            self.gallery = Gallery()
            self.gallery.transition = dissolve
            self.gallery.locked_button = self.scale(gallerynpy_properties.locked)      
            self.video_idle_overlay = self.scale(gallerynpy_properties.play_idle_overlay)
            self.video_hover_overlay = self.scale(gallerynpy_properties.play_hover_overlay)  

            self.items = {}
            self.current_page = gallerynpy_properties.default_slide
            self.index = 0

        def __put_item(self, item, where):
            if where not in self.items.keys():
                self.items[where] = []

            self.items[where].append(item)
            self.index += 1
        
        def __create_item(self, filename, song=None):
            return GalleryItem(
                'gallerynpy-' + str(self.index),
                filename, self.thumbnail_size, song
            )

        def __add_to_gallery(self, item, condition=None):
            self.gallery.button(item.name)
            self.gallery.image(item.path)
            if condition and isinstance(condition, str):
                self.gallery.condition(condition)

        def __get_item(self, ndex):
            if index > len(self.items[self.current_page]):
                return None
            return self.items[where][index]

        def __add_music(self, button, song):
            button.action = [Play("music", song), button.action]
            return button

        def __make_playable_button(self, item):
            return self.gallery.make_button(
                item.name, item.thumbnail,
                idle_border=self.video_idle_overlay, 
                hover_border=self.video_hover_overlay, 
                fit_first=True, xalign=0.5, yalign=0.5
            )

        def __none_button(self):
            return Button(action=None)

        def change_locked(self, image):
            """
            Changes the thumbnail for locked item
            Args:
                image: Can be the filepath to image file, the name of the image declaration or a Image object
            """
            self.gallery.locked_button = self.scale(image)

        def change_transition(self, transition):
            """
            Change the transition for show item (image and animation)
            Args:
                transition: A valid renpy transition object
            """
            self.gallery.transitions = transition

        def scale(self, path):
            """
            Return a Scale object, rescaled to thumbnail size
            Args:
                path: Can be the filepath to image file, the name of the image declaration or a Image object
            """
            return im.Scale(path, self.thumbnail_size.width, self.thumbnail_size.height)

        def put_image(self, image, where, song=None, condition=None):
            """
            Put a image to gallery
            Args:
                image: Can be the filepath to image file or the name of the image declaration.
                where: The slide where the image will be put.
                song: The filepath to the song that will be played when image is showed, default is None.
                condition: The condition for unlock image, default is unlocked.
            """
            item = self.__create_item(image, song)
            if item.type is None:
                image = renpy.get_registered_image(image)
                if image:
                    item.type = GallerynpyTypes.image
                    item.path = image
                    item.path = item.rescale_image()
                    item.thumbnail = item.create_thumbnail()

            if item.type == GallerynpyTypes.image:
                self.__put_item(item, where)
                self.__add_to_gallery(item, condition)
        
        def put_video(self, filename, where, song=None, condition=None):
            """
            Put a video to gallery
            Args:
                filename: Must be the filepath to video file.
                where: The slide where the item video be put.
                song: The filepath to the song that will be played when video is played, default is None.
                condition: The condition for unlock image, default is unlocked.
            """
            item = self.__create_item(filename, song)
            if item.type == GallerynpyTypes.video:
                self.__put_item(item, where)
                self.__add_to_gallery(item, condition)

        def put_animation(self, atl_object, thumbnail_name, where=gallerynpy_properties.animation_slide, song=None, condition=None):
            """
            Put an animation to gallery
            Args:
                atl_object: Must be the name's atl animation block.
                where: The slide where the animation will be put, default is animations.
                thumbnail_name: Can be the filepath to image file or the name of the image declaration to set as thumbnail.
                song: The filepath to the song that will be played when video is played, default is None.
                condition: The condition for unlock image, default is unlocked.
            """
            if not isinstance(atl_object, str) or not isinstance(thumbnail_name, str):
                return
            item = self.__create_item(atl_object, song)
            item.thumbnail = item.create_animation_thumbnail(thumbnail_name)
            item.type = GallerynpyTypes.animation
            self.__put_item(item, where)
            self.__add_to_gallery(item, condition)

        def update(self, to_start=False):
            """
            Caltulates the page in current slide
            Args:
                to_start: If True, back to the zero page in current slide.
            """
            if to_start:
                self.page = 0
            self.start = self.page * self.max_in_page
            self.end = min(self.start + self.max_in_page - 1, len(self.items[self.current_page]) - 1)
        
        def make_animation_button(self, item):
            """
            Returns the button for show the animation item.
            Args:
                item: The GallerynpyItem
            """
            if item and item.type == GallerynpyTypes.animation:
                button = self.__make_playable_button(item)
                return self.__add_music(button, item.song) if item.song else button
            
            return self.__none_button()

        def make_video_button(self, item):
            """
            Returns the button for show the video item.
            Args:
                item: The GallerynpyItem
            """
            if item and item.type == GallerynpyTypes.video:
                button = self.__make_playable_button(item)
                if button.action is not None:
                    button.action = Call("gallerynpy_cinema", movie=item.path)
                return self.__add_music(button, item.song) if item.song else button
            return self.__none_button()

        def make_image_button(self, item):
            """
            Returns the button for show the image item.
            Args:
                item: The GallerynpyItem
            """
            if item and item.type == GallerynpyTypes.image:
                button = self.gallery.make_button(
                    item.name, item.thumbnail,
                    idle_border=gallerynpy_properties.idle_overlay, 
                    xalign=0.5, yalign=0.5
                )

                return self.__add_music(button, item.song) if item.song else button
            return self.__none_button()


    gallerynpy = Gallerynpy()
    config.log = 'logger.txt'

init 999 python:
    gallerynpy_names = {}
    for name in gallerynpy.items.keys():
        gallerynpy_names[name] = name.capitalize()


### Styling

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


### Necesary labels for gallerynpy works

label gallerynpy_cinema(movie=None):
    if not movie is None:
        $ renpy.movie_cutscene(movie, loops=-1)
    
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


### Screens

screen gallerynpy_tooltip(tooltip):
    if tooltip:
        frame:
            style_prefix "gallerynpy_tooltip"
            style "gallerynpy_tooltip"
            background None
            text "[tooltip!t]":
                xalign 0.5

screen gallerynpy_rescaling():
    hbox:
        style_prefix "gallerynpy"
        style "gallerynpy_rescaling"
        text "Rescale:"
        spacing 10
        textbutton _("Yes"):
            action [SetVariable("persistent.gallerynpy_rescale_image", True), Call("gallerynpy_rescale")]
            tooltip "The mod will try to rescale the images to a correct aspect ratio"

        textbutton _("No"):
            action [SetVariable("persistent.gallerynpy_rescale_image", False), Call("gallerynpy_rescale", True)]
            tooltip "The mod will not try to rescale the images to a correct aspect ratio"
    use gallerynpy_tooltip(GetTooltip())


screen gallerynpy_rescale_screen():
    vbox:
        style_prefix "gallerynpy"
        style "gallerynpy"
        text "This option may affect the performance of the game at startup, since at startup" xalign 0.5
        text "the mod will try to rescale ALL IMAGES to a proper ratio and this can be slow." xalign 0.5
        text "For this option to do its job, you have to exit the game and re-enter." xalign 0.5
        text "Accept this option at your own risk." xalign 0.5
        text "This screen will not appear again either.\n" xalign 0.5

        hbox:
            style_prefix "gallerynpy"
            style "gallerynpy"
            textbutton _("Accept"):
                align(0.4,0.54)
                action [SetVariable("persistent.gallerynpy_rescale_screen", True), Call('gallerynpy_rescale')]
            textbutton _("Cancel"):
                align(0.6,0.54)
                action [Call("gallerynpy_rescale", True)]

screen gallerynpy():
    tag menu
    $ gallerynpy.update()

    ## Layout
    style_prefix "game_menu"
    add "gallerynpy_bg_overlay"
    use gallerynpy_rescaling
    text _("Gallerynpy v[gallerynpy_properties.version]"):
        style "gallerynpy_version"
    hbox:
        use gallerynpy_sliders
        use gallerynpy_content


screen gallerynpy_content():
    grid gallerynpy.columns gallerynpy.rows:
        xfill True
        yfill True
        
        for index in range(gallerynpy.start, gallerynpy.end + 1):
            $ item = gallerynpy.items[gallerynpy.current_page][index]
            if item.type == GallerynpyTypes.image:
                add gallerynpy.make_image_button(item)
            elif item.type == GallerynpyTypes.animation:
                add gallerynpy.make_animation_button(item)
            elif item.type == GallerynpyTypes.video:
                add gallerynpy.make_video_button(item)
            else:
                null
        for index in range(gallerynpy.end - gallerynpy.start + 1, gallerynpy.max_in_page):
            null

screen gallerynpy_pages():
    side "c r b":
        spacing gallerynpy_properties.pages_spacing
        viewport:
            ysize gallerynpy_properties.pages_ysize
            mousewheel True
            draggable True

            if gallerynpy_properties.show_pages_bar:
                yadjustment gallerynpy_properties.adjustment

            has vbox
            for name in gallerynpy.items.keys():
                if len(gallerynpy.items[name]) > 0:
                    python:
                        try:
                            item = gallerynpy_names[name]
                        except:
                            item = name.capitalize()
                    textbutton _("[item!t]"):
                        action [Function(gallerynpy.update, True), SetVariable("gallerynpy.current_page", name)]
        
        if gallerynpy_properties.show_pages_bar:
            bar:
                adjustment gallerynpy_properties.adjustment
                style "vscrollbar"
        else:
            null

        vbox:
            null height 35
            use gallerynpy_options  

screen gallerynpy_sliders():
    frame:
        style "gallerynpy_frame"
        xsize gallerynpy.navigation_width
        has vbox
        yalign 0.9
        style_prefix "gallerynpy"
        xpos gallerynpy_properties.navigation_xpos
        spacing gallerynpy_properties.spacing
        if persistent.gallerynpy_spedded and gallerynpy.current_page.lower() == gallerynpy_properties.animation_slide:
            use gallerynpy_anim_speeds
            use gallerynpy_options([Function(gallerynpy.update, True), SetVariable("gallerynpy.current_page", gallerynpy_properties.default_slide)])
        else:
            use gallerynpy_pages 
            


screen gallerynpy_options(return_action=Return()):
    textbutton _("Previous"):
        if gallerynpy.page > 0:
            action SetVariable("gallerynpy.page", gallerynpy.page - 1)
    textbutton _("Next"):
        if (gallerynpy.page + 1) * gallerynpy.max_in_page < len(gallerynpy.items[gallerynpy.current_page]):
            action SetVariable("gallerynpy.page", gallerynpy.page + 1)
    
    textbutton _("Return"):
        action return_action


screen gallerynpy_anim_speeds():
    vbox:
        text "Velocity:"
        hbox:
            textbutton "x1" action SetVariable("persistent.gallerynpy_animation_speed", 1)
            textbutton "x2" action SetVariable("persistent.gallerynpy_animation_speed", 2)
            textbutton "x3" action SetVariable("persistent.gallerynpy_animation_speed", 3)
            textbutton "x4" action SetVariable("persistent.gallerynpy_animation_speed", 4)