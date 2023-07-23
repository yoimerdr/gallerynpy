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

    def is_string(obj):
        return isinstance(obj, str)

    class GallerynpyProperties:
        def __init__(self):
            self.not_found_thumbnail = gallerynpy_images_path("not_found.png")
            self.play_hover_overlay = gallerynpy_images_path("play_hover_overlay.png")
            self.play_idle_overlay = gallerynpy_images_path("play_idle_overlay.png")
            self.idle_overlay = gallerynpy_images_path("idle_overlay.png")
            self.locked = gallerynpy_images_path("locked.png")
            self.background_overlay = im.Scale(gallerynpy_images_path("background_overlay.png"), config.screen_width, config.screen_height)
            self.video_thumbnails_extension = ('_thumbnail.' + item for item in ['jpg', 'png'])
            self.thumbnail_folder = gallerynpy_images_path('thumbnails')
            self.common_pages = ['videos', 'animations', 'images']
            self.version = '1.4.2'
            self.default_slide = 'images'

            ## The properties below may change
            self.font_size = 15
            self.font = gallerynpy_fonts_path("JetBrainsMono-Bold.ttf")  # can be change for a valid font path
            self.color = "#fff"
            self.hover_color = "#99ccff"
            self.selected_color = "#99ccff"
            self.insensitive_color = "#ffffff99"
            self.frame_color = "#0005"
            self.navigation_xpos = 45
            self.spacing = 5
            self.pages_spacing = 0
            self.pages_ysize = 120
            self.adjustment = ui.adjustment()
            self.animation_slide = 'animations'
            self.show_pages_bar = False
            self.pages_bar_style = 'vscrollbar'
            self.menu_bg = Solid("#ffffff00")
            self.menu = Solid("#ffffff00")


    gallerynpy_properties = GallerynpyProperties()


    class GallerynpyItem:
        def __init__(self, name, path, thumbnail_size, song=None, unlocked_condition=None):
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
            self.thumbnail = None
            self.type = None
            self.extension = os.path.splitext(path)[1]
            self.thumbnail_size = thumbnail_size
            self.song = song
            self.condition = unlocked_condition

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

            image = im.Image(self.path) if is_string(self.path) else self.path
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


    def is_gallerynpy_slider(obj):
        return isinstance(obj, GallerynpySlider)

    def is_gallerynpy_slide(obj):
        return isinstance(obj, GallerynpySlide)

    def is_gallerynpy_item(obj):
        return isinstance(obj, GallerynpyItem)


    class GallerynpyBaseSlide:
        def __init__(self, name, father=None):
            self._name = str(name)
            self._father_slider = father
            self._size = 0
            self._items = None

        def size(self):
            """
            Returns the current size
            """
            return self._size

        def name(self):
            """
            Returns the current name
            """
            return str(self._name)

        def father(self):
            """
            Returns the current father
            """
            return self._father_slider

        def clone(self, name=None, include_father=False,):
            raise NotImplementedError

        def change_father(self, father):
            """
            Changes the father slider
            If father is not valid, doesn't changes.
            """
            if is_gallerynpy_slider(father):
                self._father_slider = father

        def __len__(self):
            return self.size()

        def __str__(self):
            return self.name()

        def __repr__(self):
            return self.name().__repr__()

        def __hash__(self):
            return self.name().__hash__()

        def __iter__(self):
            if self._items:
                return self._items.__iter__()


    class GallerynpySlide(GallerynpyBaseSlide):
        def __init__(self, name, father=None):
            super().__init__(name, father)
            self._items = []

        def put(self, item):
            """
            Puts the GallerynpyItem object to the slide.
            If item is not valid, it is not putted
            Args:
                item: The GallerynpyItem
            """
            if is_gallerynpy_item(item):
                self._items.append(item)
                self._size += 1

        def get(self, index):
            """
            Returns the GallerynpyItem object in the index.
            If index is not valid, returns None
            Args:
                index: The item index
            """
            if 0 <= index < self.size():
                return self._items[index]
            return None

        def clone(self, name=None, include_father=False,):
            """
            Creates a new GallerynpySlide object with all the current values of this slide and returns it.
            Args:
                name: A new name for the new slide, default is the current slider name
                include_father: If is True, sets the current slider father as father of the new GallerynpySlide
            """
            name = name if name else self._name
            slide = GallerynpySlide(str(name), self._father_slider if include_father else None)
            [slide.put(item) for item in self]
            return slide


    class GallerynpySlider(GallerynpyBaseSlide):
        def __init__(self, name, father=None):
            super().__init__(name, father)
            self._items = {}

        def put(self, slide):
            """
            Puts the GallerynpySlider or GallerynpySlide object with the slide name as the key.
            The name of the slide must be unique in this slider.
            If slide is not valid, it is not puted
            Args:
                slide: The GallerynpySlider  or GallerynpySlide object
            """
            if is_gallerynpy_slide(slide) or is_gallerynpy_slider(slide):
                if slide.name() not in self.slides():
                    self._items[str(slide)] = slide
                    self._size += 1

        def get(self, key):
            """
            Returns the GallerynpySlider or GallerynpySlide object associated with key.
            If key is not valid, returns None
            Args:
                key: The name of the slide or slider
            """
            if key in self.slides():
                return self._items[key]
            return None

        def create_slide(self, name):
            """
            Creates a GallerynpySlide object with the specified name and the current slider as its father
            Args:
                name: A string variable
            """
            return GallerynpySlide(name, self)

        def create_slider(self, name):
            """
            Creates a GallerynpySlider object with the specified name and the current slider as its father
            Args:
                name: A string variable
            """
            return GallerynpySlider(name, self)

        def clone(self, name=None, include_father=True,):
            """
            Creates a new GallerynpySlider object with all the current values of this slider and returns it.
            Args:
                name: A new name for the new slider, default is the current slider name
                include_father: If is True, sets the current slider as father of the new GallerynpySlider
            """
            name = name if name else self._name
            slider = GallerynpySlider(name, self if include_father else None)
            for name in self.slides():
                slide = self.get(name).clone()
                slide.change_father(slider)
                slider.put(slide)

            return slider

        def slides(self):
            """
            Returns all slide names.
            """
            return self._items.keys()

        def __getitem__(self, key):
            return self.get(key)




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
            self.__start = 0
            self.__end = 0
            self.__columns = columns
            self.__rows = rows
            self.__item_width = item_width
            self.__item_min_width = min_item_width
            self.__min_screen = min_screen

            if config.screen_width <= self.__min_screen:
                self.__columns = 3 if self.__columns > 3 else self.__columns
                self.__rows = 3 if self.__rows > 3 else self.__rows
                self.__item_width = self.__item_min_width

            self.__scaling = config.screen_width / float(self.__min_screen)
            self.__navigation_width = int(290 * self.__scaling)
            if config.screen_width <= self.__min_screen:
                self.__navigation_width = int(240 * self.__scaling)
            self.__page = 0

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
            self.__current_page = gallerynpy_properties.default_slide
            self.__index = 0

        def __init_distribution(self):
            self.__item_width = 400 - 40 * (self.columns() - 3)
            if config.screen_width <= self.__min_screen:
                self.__columns = 3 if self.__columns > 3 else self.__columns
                self.__rows = 3 if self.__rows > 3 else self.__rows
                self.__item_width = self.__item_min_width

            self.__thumbnail_size = GallerynpySize(self.__item_width, int(self.__item_width * 0.5625))  # change the 0.5625 according a image scale
            self.__max_in_page = self.__columns * self.__rows

        def __put_item(self, item, where):
            where = str(where)
            self.__sliders.put(GallerynpySlide(where))
            self.__sliders[where].put(item)

        def __create_item(self, filename, song=None):
            item = GallerynpyItem('gallerynpy-' + str(self.__index), filename, self.__thumbnail_size, song)
            self.__index += 1
            return item

        def __add_to_gallery(self, item, condition=None):
            self.__gallery.button(item.name)
            self.__gallery.image(item.path)
            if condition and is_string(condition):
                self.__gallery.condition(condition)

        def __add_music(self, button, song):
            button.action = [Play("music", song), button.action, Stop("music")]
            return button

        def __make_playable_button(self, item):
            return self.__gallery.make_button(
                item.name, item.thumbnail,
                idle_border=self.__video_idle_overlay,
                hover_border=self.__video_hover_overlay,
                fit_first=True, xalign=0.5, yalign=0.5
            )

        def __change_current_slide(self, name, sliders):
            slider = sliders.get(name)
            if is_gallerynpy_slider(slider):
                self.__current_slider = slider

        def __none_button(self):
            return Button(action=None)

        def __put_slide(self, slide):
            for item in slide:
                self.__add_to_gallery(item, item.condition)

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

        def __change_to_father(self):
            self.__current_slider = self.__current_slider.father()
            if self.__current_slider is None:
                self.__current_slider = self.__sliders

        def create_image(self, image, song=None, condition=None):
            """
            Returns an image GallerynpyItem.
            Args:
                image: Can be the filepath to image file or the name of the image declaration.
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

            return item

        def create_video(self, filename, thumbnail=None, song=None, condition=None):
            """
            Returns an video GallerynpyItem.
            Args:
                filename: Must be the filepath to video file.
                thumbnail: The image name or image path for put as video thumbnail.
                song: The filepath to the song that will be played when video is played, default is None.
                condition: The condition for unlock image, default is unlocked.
            """
            item = self.__create_item(filename, song)
            if item.type == GallerynpyTypes.video:
                if thumbnail is not None and is_string(thumbnail):
                    item.thumbnail = item.create_animation_thumbnail(thumbnail)
            return item

        def create_animation(self, atl_object, thumbnail_name, song=None, condition=None):
            """
            Returns an animation GallerynpyItem.
            If atl_object or thumbnail_name are not valid, None is returned.
            Args:
                atl_object: Must be the name's atl animation block.
                thumbnail_name: Can be the filepath to image file or the name of the image declaration to set as thumbnail.
                song: The filepath to the song that will be played when video is played, default is None.
                condition: The condition for unlock image, default is unlocked.
            """
            if not is_string(atl_object) or not is_string(thumbnail_name):
                return None
            item = self.__create_item(atl_object, song)
            item.thumbnail = item.create_animation_thumbnail(thumbnail_name)
            item.type = GallerynpyTypes.animation
            return item

        def create_slide(self, name):
            """
            Creates a GallerynpySlide object with the specified name and the base slider as its father
            Args:
                name: A string variable
            """
            return self.__sliders.create_slide(name)

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
                    button.action = Call("gallerynpy_cinema", movie=item.path)
                return self.__add_music(button, item.song) if item.song else button
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
            idle = gallerynpy_properties.idle_overlay
            border = self.scale(idle) if is_string(idle) and idle.endswith(GallerynpyExtensions.image_extensions) else idle
            if item and item.type == GallerynpyTypes.image:
                button = self.__gallery.make_button(
                    item.name, item.thumbnail,
                    idle_border=border,
                    xalign=0.5, yalign=0.5
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
                return None

            if item.type == GallerynpyTypes.image:
                return self.make_image_button(item)
            elif item.type == GallerynpyTypes.animation:
                return self.make_animation_button(item)
            elif item.type == GallerynpyTypes.video:
                return self.make_video_button(item)

            return None

        def change_distribution(self, rows=None, columns=None):
            """
            Changes the distribution of the elements on the gallerynpy screen.
            Must be called before put or create methods.
            Args:
                rows: a valid rows number
                columns: a valid columns number
            """
            if rows is not None and rows > 0:
                self.__rows = rows

            if columns is not None and columns > 0:
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

        def put_image(self, image, where, song=None, condition=None):
            """
            Puts a image to gallery on the base slider and on the the where slide
            Args:
                image: Can be the filepath to image file or the name of the image declaration.
                where: The slide where the image will be put.
                song: The filepath to the song that will be played when image is showed, default is None.
                condition: The condition for unlock image, default is unlocked.
            """
            item = self.create_image(image, song, condition)
            if item.type == GallerynpyTypes.image:
                self.__put_item(item, where)
                self.__add_to_gallery(item, condition)

        def put_video(self, filename, where, thumbnail=None, song=None, condition=None):
            """
            Puts a video to gallery on the base slider and on the the where slide
            Args:
                filename: Must be the filepath to video file.
                where: The slide where the item video will be put.
                thumbnail: The image name or image path for put as video thumbnail.
                song: The filepath to the song that will be played when video is played, default is None.
                condition: The condition for unlock image, default is unlocked.
            """
            item = self.create_video(filename, thumbnail, song, condition)
            if item.type == GallerynpyTypes.video:
                self.__put_item(item, where)
                self.__add_to_gallery(item, condition)

        def put_animation(self, atl_object, thumbnail_name, where=gallerynpy_properties.animation_slide, song=None, condition=None):
            """
            Puts an animation to gallery on the base slider and on the where slide
            Args:
                atl_object: Must be the name's atl animation block.
                where: The slide where the animation will be put, default is animations.
                thumbnail_name: Can be the filepath to image file or the name of the image declaration to set as thumbnail.
                song: The filepath to the song that will be played when video is played, default is None.
                condition: The condition for unlock image, default is unlocked.
            """
            item = self.create_animation(atl_object, thumbnail_name, song, condition)
            if item is not None:
                self.__put_item(item, where)
                self.__add_to_gallery(item, condition)

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

        def is_current_animation_slide(self):
            """
            Returns True if current slide name is equal to gallerynpy_properties.animation_slide
            """
            return self.__current_page.lower() == gallerynpy_properties.animation_slide.lower()

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

        def slides(self):
            """
            Returns the current all slide names
            """
            return self.__current_slider.slides()

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

        def is_current_slide(self, slide):
            """
            Returns if the current slide is equals to slide.
            Args:
                slide: the slide value
            """
            return self.current_slide() == slide

        def return_action(self):
            """
            Returns the action for the back button on the current slider
            """
            if self.__current_slider != self.__sliders:
                return [Function(self.update, True), Function(self.__change_to_father)]

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

        def change_slide(self, slide):
            """
            Changes the current slide.
            If slide isn't insde the current slides, doesnt change.
            Args:
                slide: the new current slide name
            """
            if slide in self.slides():
                self.__change_current_slide(slide, self.__current_slider)
                self.__current_page = slide


    gallerynpy = Gallerynpy()
    config.log = 'gallerynpy.txt'

init 999 python:
    gallerynpy_names = {}
    for name in gallerynpy.slides():
        gallerynpy_names[name] = name.capitalize()