# Gallerynpy logic
init -1 python:
    import os

    # for try fix image size
    if persistent.gallerynpy_rescale_image is None:
        persistent.gallerynpy_rescale_image = False
    if persistent.gallerynpy_rescale_screen is None:
        persistent.gallerynpy_rescale_screen = False

    # for animation speed
    persistent.gallerynpy_animation_speed = 1
    persistent.gallerynpy_spedded = False


    class GallerynpySize:
        def __init__(self, width, height):
            self.width = width
            self.height = height


    class GallerynpyExtensions:
        video_extensions = ('.webm', '.avi', '.mp4', '.wav', '.mkv', '.ogv')
        image_extensions = ('.png', '.jpg', '.web', '.jpeg', '.webp')


    class GallerynpyTypes:
        image = 'image'
        video = 'video'
        animation = 'animation'


    def is_image_path(path):
        try:
            head, tail = os.path.splitext(path)
            return tail in GallerynpyExtensions.image_extensions if tail else False
        except ValueError:
            return False


    def renpy_path(path):
        return path.replace('\\', '/')

    def gallerynpy_path(path):
        return "gallerynpy/" + path

    def gallerynpy_images_path(path):
        return gallerynpy_path("images/" + path)

    def gallerynpy_fonts_path(path):
        return gallerynpy_path("fonts/" + path)

    class GallerynpyProperties:
        def __init__(self):
            self.not_found_thumbnail = gallerynpy_images_path("not_found.png")
            self.play_hover_overlay = gallerynpy_images_path("play_hover_overlay.png")
            self.play_idle_overlay = gallerynpy_images_path("play_idle_overlay.png")
            self.idle_overlay = gallerynpy_images_path("idle_overlay.png")
            self.locked = gallerynpy_images_path("locked.png")
            self.background_overlay = gallerynpy_images_path("background_overlay.png")
            self.video_thumbnails_extension = ('_thumbnail.' + item for item in ['jpg', 'png'])
            self.thumbnail_folder = gallerynpy_images_path('thumbnails')
            self.common_pages = ['videos', 'animations', 'images']
            self.version = '1.0.1'
            self.font_size = 15
            self.font = gallerynpy_fonts_path("JetBrainsMono-Bold.ttf")
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
            where = str(where)
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

        def __get_item(self, index):
            if self.current_page not in self.items.keys() or index > len(self.items[self.current_page]):
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
        
        def put_video(self, filename, where, thumbnail=None, song=None, condition=None):
            """
            Put a video to gallery
            Args:
                filename: Must be the filepath to video file.
                where: The slide where the item video be put.
                thumbnail: The image name or image path for put as video thumbnail.
                song: The filepath to the song that will be played when video is played, default is None.
                condition: The condition for unlock image, default is unlocked.
            """
            item = self.__create_item(filename, song)
            if item.type == GallerynpyTypes.video:
                if thumbnail is not None and isinstance(thumbnail, str):
                    item.thumbnail = item.create_animation_thumbnail(thumbnail)
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

        def slide_size(self, where):
            """
            Returns the size of the slide. 
            If where is not a valid slide, returns 0
            Args:
                where: The slide where items where pushed
            """
            return len(self.items[where]) if where in self.items.keys() else 0

        def current_slide_size(self):
            """
            Returns the size of the current slide. 
            If current slide is not a valid slide, returns 0
            """
            return self.slide_size(self.current_page)
        
        def item_at(self, where, index):
            """
            Returns the GalleryItem in the index passed from the where slide. 
            If where slide is not a valid slide or index is a not valid index, returns None
            Args:
                where: The slide where items were pushed
                index: The index of the item
            """
            if where not in self.items.keys() or index < 0 or index > self.slide_size(where):
                return None
            return self.items[where][index]

        def current_item_at(self, index):
            """
            Returns the GalleryItem in the index passed from the where slide. 
            If current slide is not a valid slide or index is a not valid index, returns None
            Args:
                index: The index of the item
            """
            return self.item_at(self.current_page, index)

        def update(self, to_start=False):
            """
            Caltulates the page in current slide
            Args:
                to_start: If True, back to the zero page in current slide.
            """
            if to_start:
                self.page = 0
            self.start = self.page * self.max_in_page
            self.end = min(self.start + self.max_in_page - 1, self.current_slide_size() - 1)
        
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

        def make_current_button_at(self, index):
            """
            Returns the button for the item at the index in the current slide.
            If the index is not valid, returns None.
            Args:
                index: The index of the item
            """
            item = self.current_item_at(index)
            if item is None:
                return None

            if item.type == GallerynpyTypes.image:
                return self.make_image_button(item)
            elif item.type == GallerynpyTypes.animation:
                return self.make_animation_button(item)
            elif item.type == GallerynpyTypes.video:
                return self.make_video_button(item)

            return None

        def is_current_animation_slide(self):
            return self.current_page.lower() == gallerynpy_properties.animation_slide.lower()
        

    gallerynpy = Gallerynpy()
    config.log = 'logger.txt'

init 999 python:
    gallerynpy_names = {}
    for name in gallerynpy.items.keys():
        gallerynpy_names[name] = name.capitalize()