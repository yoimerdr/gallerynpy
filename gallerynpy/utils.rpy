init -3 python:

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