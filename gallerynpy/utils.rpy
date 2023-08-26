init -3 python:
    import renpy as renpy_module

    try:
        import json as json_module
    except:
        pass

    import os


    def is_image(obj):
        return isinstance(obj, im.Image)

    def is_animation(obj):
        return isinstance(obj, renpy_module.display.transform.ATLTransform)
    
    def is_video_loadable(path):
        return is_string(path) and path.endswith(GallerynpyExtensions.video_extensions) and renpy.loadable(path)

    def is_image_loadable(path):
        return is_string(path) and path.endswith(GallerynpyExtensions.image_extensions) and renpy.loadable(path)
    
    def is_image_path(path):
        try:
            head, tail = os.path.splitext(path)
            return tail in GallerynpyExtensions.image_extensions if tail else False
        except ValueError:
            pass

        return False

    def game_fullpath():
        return join_paths(renpy_module.config.basedir, "game")
    
    def exists_path(path):
        return os.path.exists(path)

    def make_dir(path):
        os.mkdir(path)

    def join_paths(first, second):
        return os.path.join(first, second)
    
    def renpy_join(first, second):
        return first + "/" + second

    def renpy_path(path):
        return path.replace('\\', '/')

    def gallerynpy_path(path):
        return renpy_join("gallerynpy", path)

    def gallerynpy_images_path(path):
        return gallerynpy_path(renpy_join("images", path))

    def gallerynpy_fonts_path(path):
        return gallerynpy_path(renpy_join("fonts", path))

    def is_string(obj):
        return isinstance(obj, str)

    def is_gallerynpy_size(obj):
        return isinstance(obj, GallerynpySize)

    def is_gallerynpy_slider(obj):
        return isinstance(obj, GallerynpySlider)

    def is_gallerynpy_slide(obj):
        return isinstance(obj, GallerynpySlide)

    def is_gallerynpy_item(obj):
        return isinstance(obj, GallerynpyItem)
    
    class GallerynpySize:
        def __init__(self, width, height):
            self.width = width
            self.height = height

        def __eq__(self, other):
            if is_gallerynpy_size(other):
                return self.width == other.width and self.height == other.height

            return False

        def __ne__(self, other):
            if is_gallerynpy_size(other):
                return self.width != other.width or self.height != other.height
            return False


    class GallerynpyExtensions:
        video_extensions = ('.webm', '.avi', '.mp4', '.wav', '.mkv', '.ogv')
        image_extensions = ('.png', '.jpg', '.web', '.jpeg', '.webp')


    class GallerynpyTypes:
        image = 'image'
        video = 'video'
        animation = 'animation'



    class GallerynpyDb:
        def __init__(self):
            self.__folder = join_paths("gallerynpy", "db")
            self.__source = join_paths(self.__folder, "images.json")
            self.__sizes = {}
            self.__save = False
            try:
                self.__sizes = json_module.load(renpy.file(renpy_path(self.__source), encoding="utf-8"))
            except:
                pass   
        
        def __file(self, mode='r'):
            return open(join_paths(game_fullpath(), self.__source), mode=mode, encoding='utf-8')

        def __size(self, path):
            obj = self.__sizes
            folders, name = self.__keys(path)
            for folder in folders:
                if name in obj.keys():
                    if len(obj[name]) != 2:
                        return None

                    return GallerynpySize(obj[name][0], obj[name][1])

                if folder not in obj.keys():
                    return None

                obj = obj[folder]

            return None

        def imagesize(self, path, folder=None):
            if folder is not None:
                path = join_paths(folder, path)
            return self.__size(path)

        def named_imagesize(self, name):
            return self.imagesize(name, "gallerynpyNamed")

        def put_imagesize(self, path, size, folder=None):
            if not is_gallerynpy_size(size):
                return
            if folder is not None:
                path = join_paths(folder, path)

            folders, name = self.__keys(path)
            obj = self.__sizes
            for f in folders:
                if f:
                    if f not in obj.keys():
                        obj[f] = {}
                    obj = obj[f]
            self.__save = name not in obj.keys() if not self.__save else self.__save
            obj[name] = [size.width, size.height]

        def put_named_imagesize(self, path, size):
            self.put_imagesize(path, size, "gallerynpyNamed")

        def contains(self, path):
            return self.__size(path) is not None

        def save(self):
            if self.__save:
                try:
                    dirname = join_paths(game_fullpath(), self.__folder)
                    if not exists_path(dirname):
                        make_dir(dirname)
                    json_module.dump(self.__sizes, self.__file('w'))
                except:
                    pass

        def __contains__(self, item):
            if is_string(item):
                if not item.contains("."):
                    item = "gallerynpyNamed" + "/" + item
                return self.contains(item)

            return False

        def __keys(self, path):
            name = os.path.basename(path)
            return renpy_path(path.replace(name, "")).split("/"), name

        def __str__(self):
            return str(self.__sizes)

    gallerynpy_db = GallerynpyDb()
