init -2 python:
    class GallerynpyBaseSlide:
        def __init__(self, name, father=None, is_animation_slide=False):
            self._name = str(name)
            self._father_slider = father
            self._size = 0
            self._items = None
            self._is_anim_slide = is_animation_slide

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

        def is_animation_slide(self):
            """
            Returns if slide is marked as animation slide.
            """
            return self._is_anim_slide

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
        def __init__(self, name, father=None, is_animation_slide=False):
            super().__init__(name, father, is_animation_slide)
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
            slide = GallerynpySlide(str(name), self._father_slider if include_father else None, self._is_anim_slide)
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

        def create_slide(self, name, is_animation_slide=False):
            """
            Creates a GallerynpySlide object with the specified name and the current slider as its father
            Args:
                name: A string variable
                is_animation_slide: If is True, the slide is marked as an animation slide
            """
            return GallerynpySlide(name, self, is_animation_slide)

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

        def slides(self, sort=False):
            """
            Returns all slide names
            Args:
                sort: If is True, sort the list before return it.
            """
            names = list(self._items.keys())
            if sort:
                names.sort()
            return names

        def __getitem__(self, key):
            return self.get(key)
