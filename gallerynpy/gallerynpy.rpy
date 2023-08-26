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
    

    class GallerynpyProperties:
        def __init__(self):
            self.not_found_thumbnail = gallerynpy_images_path("not_found.png")
            self.play_hover_overlay = gallerynpy_images_path("play_hover_overlay.png")
            self.play_idle_overlay = gallerynpy_images_path("play_idle_overlay.png")
            self.idle_overlay = gallerynpy_images_path("idle_overlay.png")
            self.locked = gallerynpy_images_path("locked.png")
            self.background_overlay = im.Scale(gallerynpy_images_path("background_overlay.png"), config.screen_width, config.screen_height)
            self.video_thumbnails_extension = tuple('_thumbnail.' + item for item in ['jpg', 'png'])
            self.common_pages = ['videos', 'animations', 'images']
            self.version = '1.6'
            self.default_slide = 'images'

            ## The properties below may change
            self.thumbnail_folder = images_path(renpy_join("gallerynpy", "thumbnails"))
            self.font_size = 20
            self.font = gallerynpy_fonts_path("JetBrainsMono-Bold.ttf")  # can be change for a valid font path
            self.color = "#fff"
            self.hover_color = "#99ccff"
            self.selected_color = "#99ccff"
            self.insensitive_color = "#ffffff99"

            # frame options properties
            self.frame_color = "#0005"
            self.frame_yalign = 0.992
            self.frame_xsize = 420
            self.frame_position = 'l'
            self.frame_xpos = 45
            self.frame_content_spacing = 10

            # item properties
            self.item_xspacing = 10

            self.spacing = 5
            self.navigation_xpos = 45

            self.pages_spacing = 0
            self.pages_ysize = 120
            self.adjustment = ui.adjustment()
            self.animation_slide = 'animations'
            self.show_pages_bar = False

            self.pages_bar_position = 'r'
            self.pages_bar_style = 'vscrollbar'  # No longer used
            self.pages_bar_xsize = 20
            if config.screen_width <= 1280:
                self.pages_bar_xsize = 15
            self.pages_bar_xpos = self.pages_bar_xsize * 2
            

            if config.screen_width <= 1280:
                self.pages_bar_xpos += 10
            
            self.menu_bg = Solid("#ffffff00")
            self.menu = Solid("#ffffff00")
            self.sort_slides = False
            self.rescale_images = True

        def __validate_image_overlay(self):
            if is_string(self.idle_overlay):
                if not is_image_loadable(self.idle_overlay):
                    image = renpy.get_registered_image(self.idle_overlay)
                    self.idle_overlay = image if is_image(image) else gallerynpy_images_path("idle_overlay.png")
                self.idle_overlay = gallerynpy.scale(self.idle_overlay)

        def validate(self,):
            if self.pages_bar_position not in ('l', 'r'):
                self.pages_bar_position = 'r'
            if self.frame_position not in ('l', 'r'):
                self.frame_position = 'l'
            if self.frame_yalign < 0 or self.frame_yalign > 1:
                self.frame_yalign = 0.992

            self.__validate_image_overlay()
            
 
    gallerynpy_properties = GallerynpyProperties()


    class GallerynpyItem:
        def __init__(self, name, path, thumbnail_size, song=None, unlocked_condition=None, tooltip=None):
            """
            constructor for a GallerynpyItem.
            Args:
                name: name of the item.
                path: image name or filepath to the image or video, if is an atl object, will be the name.
                thumbnail_size: GallerynpySize object to scale thumbnails.
                song: optional argument, it will be the path to the song that will be played when the item is displayed.
            """
            self.name = name
            self.path = path
            self.image = None
            self.thumbnail = None
            self.type = None
            self.extension = os.path.splitext(path)[1]
            self.thumbnail_size = thumbnail_size
            self.song = song
            self.condition = unlocked_condition
            self.image_size = None
            self.custom_thumbnail = None
            self.__named_image = None
            self.tooltip = ""
            if tooltip is not None:
                self.tooltip = str(tooltip)

            if self.extension in GallerynpyExtensions.image_extensions:
                self.image_size = gallerynpy_db.imagesize(path)
                self.__init_image()
            elif self.extension in GallerynpyExtensions.video_extensions:
                if not is_video_loadable(self.path):
                    raise FileNotFoundError("Cannot find file '" + self.path + "'")
                self.type = GallerynpyTypes.video
            else:
                image = renpy.get_registered_image(self.path)
                if image:
                    if is_image(image):
                        self.image_size = gallerynpy_db.named_imagesize(self.path)
                        self.__named_image = image
                        self.__init_image()
                    elif is_animation(image):
                        self.type = GallerynpyTypes.animation
                        self.image = image
                else:
                    raise NameError("No image block or animation with name '" + self.path + "' found.\nIf exists, make the put in a init 999 python block")
            self.thumbnail = self.create_thumbnail()

        def __init_image(self):
            self.type = GallerynpyTypes.image
            self.image = self.rescale_image()

        def __validate_size(self, image):
            if self.image_size is None or not is_gallerynpy_size(self.image_size):
                width, height = image.load().get_size()
                self.image_size = GallerynpySize(width, height)
                if self.__named_image:
                    gallerynpy_db.put_named_imagesize(self.path, self.image_size)
                else:
                    gallerynpy_db.put_imagesize(self.path, self.image_size)

        def __ratio_size(self, size, ratio=None):
            if is_gallerynpy_size(size):
                if ratio is None:
                    ratio = self.image_size.width / self.image_size.height
                if self.image_size == size or ratio == 16/9:
                    return size
                elif ratio > 16/9:
                    return GallerynpySize(size.width, size.width / ratio)
                return GallerynpySize(size.height * ratio, size.height)
            return size

        def __ratio_scale(self, image, screen_size, ratio=None):
            if all(is_gallerynpy_size(item) for item in [self.image_size, screen_size]):
                size = self.__ratio_size(screen_size, ratio)
                return im.Scale(image, size.width, size.height)

            return im.Scale(image, screen_size.width, screen_size.height)
        
        def __image_thumbnail(self):
            if gallerynpy_properties.rescale_images:
                return self.__ratio_scale(self.__named_image if self.__named_image else self.path, self.thumbnail_size)
            return self.scale(self.__named_image if self.__named_image else self.path)

        def __custom_thumbnail_size(self, path):
            size = None
            if self.type == GallerynpyTypes.image:
                return size
            if is_image_loadable(path):
                size = gallerynpy_db.imagesize(path)
            elif not '.' in path:
                size = gallerynpy_db.named_imagesize(path)
            return size
        
        def rescale_image(self):
            """
            If item type is GallerynpyTypes.image, rescale the image to screen size.
            If gallerynpy_properties.rescale_images is True, it will rescale to a correct image ratio according to the screen size and image size.
            """
            if self.path is None:
                raise ValueError('The path cannot be None')
            if not self.type == GallerynpyTypes.image:
                raise ValueError('The type must be GallerynpyTypes.image')
            image = gallerynpy_properties.not_found_thumbnail
            if self.extension in GallerynpyExtensions.image_extensions:
                if not is_image_loadable(self.path):
                    raise FileNotFoundError("Cannot find file " + self.path)
                image = Image(self.path)
            elif self.__named_image:
                image = self.__named_image
            if gallerynpy_properties.rescale_images:
                self.__validate_size(image)
                ratio = self.image_size.width / self.image_size.height
                try:
                    return self.__ratio_scale(image, GallerynpySize(config.screen_width, config.screen_height), ratio)
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
                        thumbnail_path = renpy_path(join_paths(gallerynpy_properties.thumbnail_folder, self.path.replace(self.extension, extension)))
                        if is_image_loadable(thumbnail_path):
                            return self.scale(thumbnail_path)
                elif self.type == GallerynpyTypes.image:
                    return self.__croped_thumbnail()
                elif self.type == GallerynpyTypes.animation and self.custom_thumbnail:
                    return self.scale(self.custom_thumbnail)

            return self.not_found()

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

        def change_size(self, size):
            """
            Change the current size and rescale the thumbnail and image
            """
            if is_gallerynpy_size(size) and size != self.thumbnail_size:
                self.thumbnail_size = size
                if self.type == GallerynpyTypes.image:
                    self.image = self.rescale_image()
                self.thumbnail = self.create_thumbnail()

        def set_custom_thumbnail(self, thumbnail):
            """
            Change the thumbnail image
            """
            if is_string(thumbnail):
                if is_image_loadable(thumbnail):
                    self.image_size = self.__custom_thumbnail_size(thumbnail)
                    self.thumbnail = self.__croped_thumbnail(self.__ratio_scale(thumbnail, self.thumbnail_size))
                    self.image_size = None
                    self.custom_thumbnail = thumbnail
                    return
                image = renpy.get_registered_image(thumbnail)
                if image and is_image(image):
                    self.custom_thumbnail = image
                    self.image_size = self.__custom_thumbnail_size(thumbnail)
                    self.thumbnail = self.__croped_thumbnail(self.__ratio_scale(image, self.thumbnail_size))
                    self.image_size = None
                    return
            self.custom_thumbnail = None
            # self.thumbnail = self.not_found()

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
        
        def __croped_thumbnail(self, thumbnail=None):
            self.thumbnail = self.__image_thumbnail()
            if thumbnail is not None:
                self.thumbnail = thumbnail
            x = 0
            if gallerynpy_properties.rescale_images and is_gallerynpy_size(self.image_size):
                size = self.__ratio_size(self.thumbnail_size)
                x = int((self.thumbnail_size.width / 2 - size.width / 2))
                
            return Composite((self.thumbnail_size.width, self.thumbnail_size.height), (x, 0), self.thumbnail)

    class Gallerynpy:
        def __init__(self, columns=5, rows=5, item_width=None, min_screen=1280):
            """
            constructor for Gallerynpy
            Args:
                columns: The number of columns in a slide.
                rows: The number of rows in a slide.
                item_width: thumbnail width for each GallerynpyItem. No longer used.
                min_screen: The min config screen size
            """
            # navigation configuration
            self.__start = 0
            self.__end = 0
            self.__columns = columns
            self.__rows = rows
            self.__min_screen = min_screen
            self.__scaling = config.screen_width / float(self.__min_screen)

            self.__navigation_width = int(290 * self.__scaling)
            if config.screen_width <= self.__min_screen:
                self.__navigation_width = int(260 * self.__scaling)

            gallerynpy_properties.frame_xsize = self.nav_width()
            self.__item_width = self._item_width()

            self.__page = 0

            self.__tooltip = ""

            if config.screen_width <= self.__min_screen:
                self.__columns = 4 if self.__columns > 4 else self.__columns
                self.__rows = 4 if self.__rows > 4 else self.__rows
                self.__item_width = self._item_width()

            self.__thumbnail_size = GallerynpySize(self.__item_width, int(self.__item_width * 0.5625))  # change the 0.5625 according a image scale
            self.__max_in_page = self.__columns * self.__rows  # number of items in one page

            # Gallery
            self.__gallery = Gallery()
            self.__gallery.transition = dissolve
            self.__gallery.locked_button = self.scale(gallerynpy_properties.locked)
            self.__video_idle_overlay = self.scale(gallerynpy_properties.play_idle_overlay)
            self.__video_hover_overlay = self.scale(gallerynpy_properties.play_hover_overlay)

            self.__sliders = GallerynpySlider("base")
            self.__current_slider =  self.__sliders
            self.__current_page = ""
            self.__index = 0

        def _item_width(self,):
            spacing_size = gallerynpy_properties.item_xspacing * (self.columns() - 1)
            screen = config.screen_width - gallerynpy_properties.frame_xsize - gallerynpy_properties.frame_content_spacing

            return (screen - spacing_size) / self.columns()

        def __init_distribution(self):
            self.__item_width = self._item_width()
            self.__thumbnail_size = GallerynpySize(int(self.__item_width), int(self.__item_width * 0.5625))  # change the 0.5625 according a image scale
            self.__max_in_page = self.__columns * self.__rows
            self.__gallery.locked_button = self.scale(gallerynpy_properties.locked)
            self.__video_idle_overlay = self.scale(gallerynpy_properties.play_idle_overlay)
            self.__video_hover_overlay = self.scale(gallerynpy_properties.play_hover_overlay)

        def __put_item(self, item, where, is_animation_slide=False):
            where = str(where)
            self.__sliders.put(GallerynpySlide(where, is_animation_slide=is_animation_slide))
            self.__sliders[where].put(item)

        def __create_item(self, filename, song=None, condition=None, tooltip=None):
            item = GallerynpyItem('gallerynpy-' + str(self.__index), filename, self.__thumbnail_size, song, condition, tooltip)
            self.__index += 1
            return item

        def __add_to_gallery(self, item):
            self.__gallery.button(item.name)
            if item.type == GallerynpyTypes.video:
                self.__gallery.image(item.path)
            else:
                self.__gallery.image(item.image)
            if item.condition and is_string(item.condition):
                self.__gallery.condition(item.condition)

        def __add_music(self, button, song, is_movie=False):
            if not is_movie:
                song = str(song)
                if renpy.loadable(song):
                    button.action = [Play("music", song), button.action, Stop("music")]
            return button

        def __make_playable_button(self, item):
            return self.__gallery.make_button(
                item.name, item.thumbnail,
                idle_border=self.__video_idle_overlay,
                hover_border=self.__video_hover_overlay,
                fit_first=True, xalign=0.5, yalign=0.5,
                hovered=Function(self.__change_tooltip, item.tooltip),
                unhovered=Function(self.__change_tooltip, "")
            )

        def __change_current_slide(self, name, sliders):
            slider = sliders.get(name)
            if is_gallerynpy_slider(slider):
                self.__current_slider = slider
                return True
            return False

        def __none_button(self):
            return Button(action=None)

        def __put_slide(self, slide):
            for item in slide:
                self.__add_to_gallery(item)

        def __put_slider(self, slider):
            if is_gallerynpy_slider(slider):
                for name in slider:
                    slide = slider.get(name)
                    if is_gallerynpy_slider(slide):
                        self.__put_slider(slide)
                    elif is_gallerynpy_slide(slide):
                        self.__put_slide(slide)
            elif is_gallerynpy_slide(slider):
                self.__put_slide(slider)

        def __empty_slide(self):
            self.__current_page = ""

        def __change_to_father(self):
            self.__current_slider = self.__current_slider.father()
            if self.__current_slider is None:
                self.__current_slider = self.__sliders
            self.to_first_slide(gallerynpy_properties.sort_slides)

        def __slide(self, where):
            if where not in self.slides():
                return None
            return self.__current_slider[where]

        def __current_slide(self):
            return self.__slide(self.__current_page)

        def __create_playable_item(self, path, thumbnail=None, song=None, condition=None, tooltip=None):
            if not is_string(path):
                return None
            item = self.__create_item(path, song, condition, tooltip)
            item.set_custom_thumbnail(thumbnail)
            return item

        def __change_tooltip(self, text):
            self.__tooltip = str(text)

        def create_image(self, image, song=None, condition=None, tooltip=None):
            """
            Returns an image GallerynpyItem.
            Args:
                image: Can be the filepath to image file or the name of the image declaration.
                song: The filepath to the song that will be played when image is showed, default is None.
                condition: The condition for unlock image, default is unlocked.
            """
            return self.__create_item(image, song, condition, tooltip)

        def create_video(self, filename, thumbnail=None, song=None, condition=None, tooltip=None):
            """
            Returns an video GallerynpyItem.
            Args:
                filename: Must be the filepath to video file.
                thumbnail: The image name or image path for put as video thumbnail.
                song: The filepath to the song that will be played when video is played, default is None.
                condition: The condition for unlock image, default is unlocked.
            """
            return self.__create_playable_item(filename, thumbnail, song, condition, tooltip)

        def create_animation(self, atl_object, thumbnail_name, song=None, condition=None, tooltip=None):
            """
            Returns an animation GallerynpyItem.
            If atl_object or thumbnail_name are not valid, None is returned.
            Args:
                atl_object: Must be the name's atl animation block.
                thumbnail_name: Can be the filepath to image file or the name of the image declaration to set as thumbnail.
                song: The filepath to the song that will be played when video is played, default is None.
                condition: The condition for unlock image, default is unlocked.
            """
            return self.__create_playable_item(atl_object, thumbnail_name, song, condition, tooltip)

        def create_slide(self, name, is_animation_slide=False):
            """
            Creates a GallerynpySlide object with the specified name and the base slider as its father
            Args:
                name: A string variable
                is_animation_slide: If is True, the slide is marked as an animation slide
            """
            return self.__sliders.create_slide(name, is_animation_slide)

        def create_slider(self, name):
            """
            Creates a GallerynpySlider object with the specified name  and the base slider as its father
            Args:
                name: A string variable
            """
            return self.__sliders.create_slider(name)

        def put_slider(self, slider):
            """
            Puts the valid slider in the gallery.
            Args:
                slider: A GallerynpySlider or GallerynpySlide object
            """
            if not is_gallerynpy_slider(slider) and not is_gallerynpy_slide(slider):
                return
            self.__put_slider(slider)
            self.__sliders.put(slider)

        def make_animation_button(self, item):
            """
            Returns the button to display the animation type item.
            If it is not or item is not an GallerynpyItem, a button with no action will be returned.
            Args:
                item: The GallerynpyItem
            """
            if not is_gallerynpy_item(item):
                return self.__none_button()
            if item and item.type == GallerynpyTypes.animation:
                button = self.__make_playable_button(item)
                return self.__add_music(button, item.song) if item.song else button

            return self.__none_button()

        def make_video_button(self, item):
            """
            Returns the button to display the video type item.
            If it is not or item is not an GallerynpyItem, a button with no action will be returned.
            Args:
                item: The GallerynpyItem
            """
            if not is_gallerynpy_item(item):
                return self.__none_button()
            if item and item.type == GallerynpyTypes.video:
                button = self.__make_playable_button(item)
                if button.action is not None:
                    button.action = Call("gallerynpy_cinema", movie=item.path, song=item.song)
                return self.__add_music(button, item.song, True) if item.song else button
            return self.__none_button()

        def make_image_button(self, item):
            """
            Returns the button to display the image type item.
            If it is not or item is not an GallerynpyItem, a button with no action will be returned.
            Args:
                item: The GallerynpyItem
            """
            if not is_gallerynpy_item(item):
                return self.__none_button()

            if item and item.type == GallerynpyTypes.image:
                button = self.__gallery.make_button(
                    item.name, item.thumbnail,
                    idle_border=gallerynpy_properties.idle_overlay,
                    xalign=0.5, yalign=0.5,
                    hovered=Function(self.__change_tooltip, item.tooltip),
                    unhovered=Function(self.__change_tooltip, "")
                )

                return self.__add_music(button, item.song) if item.song else button
            return self.__none_button()

        def make_current_button_at(self, index):
            """
            Returns the button for the element in the index of the current slide.
            If the index is invalid, returns None.
            Args:
                index: The index of the item
            """
            item = self.current_item_at(index)
            if item is None:
                return Null()
            item.change_size(self.__thumbnail_size)
            if item.type == GallerynpyTypes.image:
                return self.make_image_button(item)
            elif item.type == GallerynpyTypes.animation:
                return self.make_animation_button(item)
            elif item.type == GallerynpyTypes.video:
                return self.make_video_button(item)

            return Null()

        def change_distribution(self, rows=None, columns=None):
            """
            Changes the distribution of the elements on the gallerynpy screen.
            Must be called before put or create methods.
            Args:
                rows: a valid rows number
                columns: a valid columns number
            """
            if rows is not None and rows > 0 and rows != self.__rows:
                self.__rows = rows

            if columns is not None and columns > 0 and columns != self.__columns:
                self.__columns = columns

            self.__init_distribution()

        def change_locked(self, image):
            """
            Changes the thumbnail for locked item
            Args:
                image: Can be the filepath to image file, the name of the image declaration or a Image object
            """
            self.__gallery.locked_button = self.scale(image)

        def change_transition(self, transition):
            """
            Change the transition for show item (image and animation)
            Args:
                transition: A valid renpy transition object
            """
            self.__gallery.transitions = transition

        def scale(self, path):
            """
            Return a Scale object, rescaled to thumbnail size
            Args:
                path: Can be the filepath to image file, the name of the image declaration or a Image object
            """
            return im.Scale(path, self.__thumbnail_size.width, self.__thumbnail_size.height)

        def put_image(self, image, where, song=None, condition=None, tooltip=None):
            """
            Puts a image to gallery on the base slider and on the the where slide
            Args:
                image: Can be the filepath to image file or the name of the image declaration.
                where: The slide where the image will be put.
                song: The filepath to the song that will be played when image is showed, default is None.
                condition: The condition for unlock image, default is unlocked.
            """
            item = self.create_image(image, song, condition, tooltip)
            if item.type == GallerynpyTypes.image:
                self.__put_item(item, where)
                self.__add_to_gallery(item)

        def put_video(self, filename, where, thumbnail=None, song=None, condition=None, tooltip=None):
            """
            Puts a video to gallery on the base slider and on the the where slide
            Args:
                filename: Must be the filepath to video file.
                where: The slide where the item video will be put.
                thumbnail: The image name or image path for put as video thumbnail.
                song: The filepath to the song that will be played when video is played, default is None.
                condition: The condition for unlock image, default is unlocked.
            """
            item = self.create_video(filename, thumbnail, song, condition, tooltip)
            if item.type == GallerynpyTypes.video:
                self.__put_item(item, where)
                self.__add_to_gallery(item)

        def put_animation(self, atl_object, thumbnail_name, where=gallerynpy_properties.animation_slide, song=None, condition=None, is_animation_slide=True, tooltip=None):
            """
            Puts an animation to gallery on the base slider and on the where slide
            Args:
                atl_object: Must be the name's atl animation block.
                where: The slide where the animation will be put, default is animations.
                thumbnail_name: Can be the filepath to image file or the name of the image declaration to set as thumbnail.
                song: The filepath to the song that will be played when video is played, default is None.
                condition: The condition for unlock image, default is unlocked.
                is_animation_slide: If is True, mark the where slide as animation slide
            """
            item = self.create_animation(atl_object, thumbnail_name, song, condition, tooltip)
            if item is not None:
                self.__put_item(item, where, is_animation_slide)
                self.__add_to_gallery(item)

        def update(self, to_start=False):
            """
            Caltulates the page in current slide
            Args:
                to_start: If True, back to the zero page in current slide.
            """
            if to_start:
                self.__page = 0
            self.__start = self.__page * self.__max_in_page
            self.__end = min(self.__start + self.__max_in_page - 1, self.current_slide_size() - 1)

        def slide_size(self, where):
            """
            Returns the size of the slide.
            If where is not a valid slide, returns 0
            Args:
                where: The slide where items where pushed
            """
            return len(self.__current_slider[where]) if where in self.__current_slider.slides() else 0

        def current_slide_size(self):
            """
            Returns the size of the current slide.
            If current slide is not a valid slide, returns 0
            """
            return self.slide_size(self.__current_page)

        def item_at(self, where, index):
            """
            Returns the GallerynpyItem at the index of the where slide.
            If where slide is not a valid slide or the index is not a valid index, returns None.
            Args:
                where: The slide where items were pushed
                index: The index of the item
            """

            if where not in self.slides() or index < 0 or index > self.slide_size(where):
                return None
            slide = self.__current_slider[where]
            if not is_gallerynpy_slide(slide):
                return None
            return slide.get(index)

        def current_item_at(self, index):
            """
            Returns the GallerynpyItem at the index of the current slide.
            If the current slide is not a valid slide or the index is not a valid index, returns None.
            Args:
                index: The index of the item
            """
            return self.item_at(self.__current_page, index)

        def is_current_animation_slide(self,):
            """
            Returns True if current slide name is marked as animation slide
            """
            slide = self.__current_slide()
            if not is_gallerynpy_slide(slide):
                return False
            return slide.is_animation_slide()

        def columns(self):
            """
            Returns the current columns number
            """
            return self.__columns

        def rows(self):
            """
            Returns the current rows number
            """
            return self.__rows

        def current_slide(self):
            """
            Returns the current slide name
            """
            return self.__current_page

        def start(self):
            """
            Returns the current start slide number
            """
            return self.__start

        def end(self):
            """
            Returns the current end slide number
            """
            return self.__end

        def max_items(self):
            """
            Returns the current max items in the slide
            """
            return self.__max_in_page

        def slides(self, sort=False):
            """
            Returns the current all slide names
            Args:
                sort: If is True, sort the list before return it.
            """
            return self.__current_slider.slides(sort)

        def nav_width(self):
            """
            Returns the navigation width
            """
            return self.__navigation_width

        def page(self):
            """
            Returns the current page number
            """
            return self.__page

        def scaling(self):
            """
            Returns the current scaling rate
            """
            return self.__scaling

        def tooltip(self):
            return self.__tooltip

        def is_current_slide(self, slide):
            """
            Returns if the current slide is equals to slide.
            Args:
                slide: the slide value
            """
            return self.current_slide() == slide

        def return_action(self, from_animation_options=False):
            """
            Returns the action for the back button on the current slider
            """
            if not from_animation_options and self.__current_slider != self.__sliders:
                return [Function(self.update, True), Function(self.__change_to_father)]

            if from_animation_options and self.is_current_animation_slide():
                return [Function(self.update, True), Function(self.to_first_slide, gallerynpy_properties.sort_slides)]

            return Return()

        def change_page(self, number):
            """
            Changes the current page number.
            If number is not valid, doesnt change.
            Args:
                number: the new page number
            """
            if number >= 0 and number * self.max_items() < self.current_slide_size():
                self.__page = number

        def to_first_slide(self, sort=False):
            """
            Changes the current slide to the first slide in the current slider.
            If current slider size is 0 or unique slide is is_current_animation_slide, change to a empty slide.
            Args:
                sort: If is True, sort the names list before select the first slide name
            """
            names = self.slides()
            if names:
                size = len(names)
                if sort:
                    names.sort()

                for name in names:
                    slide = self.__slide(name)
                    if is_gallerynpy_slide(slide) and not (persistent.gallerynpy_spedded and slide.is_animation_slide()):
                        self.change_slide(name)
                        return

                self.__empty_slide()

        def change_slide(self, slide):
            """
            Changes the current slide.
            If slide isn't insde the current slides, doesnt change.
            Args:
                slide: the new current slide name
            """
            if slide in self.slides():
                if self.__change_current_slide(slide, self.__current_slider):
                    self.to_first_slide(gallerynpy_properties.sort_slides)
                else:
                    self.__current_page = slide


    gallerynpy = Gallerynpy()
    gallerynpy_names = {}
    config.log = 'gallerynpy.txt'

init 9999 python:
    gallerynpy_db.save()
    gallerynpy_properties.validate()
    gallerynpy.to_first_slide(gallerynpy_properties.sort_slides)
       