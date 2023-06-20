# Gallerynpy

Gallerynpy is a Ren'Py script that allows you to display a gallery screen in your visual novel. The gallery screen displays all images, animations and videos that have been inserted into the gallerynpy object.

## Usage

To use Gallerynpy, simply add the gallerynpy folder to your Ren'Py project and call the "gallerynpy" menu whenever you want to display the gallery screen. You can customize the appearance of the gallery display by modifying the provided screens and styles.

Before displaying the gallerynpy screen you should add some images, animations or videos into the gallerynpy object. I recommend that you do this in a python init block with a high wait number such as 999.

```renpy
init 999 python:

    ### IMPORTANT
    """
    About the thumbnails to be displayed on the gallerynpy screen:

        For images, you don't need to create or specify any file, since by default the same image will be displayed as thumbnail.

        For videos, you need to create a image file in the path 'gallerynpy/images/thumbnails' with name pathtovideo/videoname_thumbnail.jpg 
        or videoname_thumbnail.png. If you don't do this, the default thumbnail is a not avaible image.

        For animations, you need to specify the name of a image declaration or a image path when you put the animation
        
    About the conditions to unlock the items:
        The conditions should be strings with valid expressions that renpy's Gallery class will evaluate. Be very careful with this.

    """

    # For add a image, you need to specify at least the first two arguments, first the path or a valid name of 
    # an image declaration in renpy and second on which slide you want that image to be displayed.
    gallerynpy.put_image("wonderful_screen", "images")
    # You also can specify the condition for unlock the image add the condition argument
    gallerynpy.put_image("wonderful_screen", "images", condition="persistent.valid_condition")


    # For add a video, you need to specify at least the first two arguments, first the path of 
    # an video in your renpy project and second on which slide you want that video to be displayed.
    gallerynpy.put_video("videos/wonderful.mp4", "videos")
    # You also can specify the condition for unlock the video add the condition argument or add the thumbnail image
    gallerynpy.put_video("videos/wonderful.mp4", "videos", thumbnail="wonderful_screen", condition="persistent.valid_condition")

    # For add a animation, you need to specify at least the first two arguments, first the name of 
    # an atl (animation) block declaration in your renpy project and second a path or a valid name of 
    # an image declaration in renpy for use as thumbnail.
    gallerynpy.put_animation("wonderful_screen_animation", "wonderful_screen")
    # You also can specify the slide (where) and the condition for unlock the animation
    # if you don't specify the third argument, default slide is 'animations'
    gallerynpy.put_animation("wonderful_screen_animation", "wonderful_screen", "anim", condition="persistent.valid_condition")  

    # You can also change some properties in gallerynpy
    # for specify the initial slide to show
    gallerynpy.change_slide("images")
    # for show a vertical bar at right of all slides buttons, default doesn't show
    gallerynpy_properties.show_pages_bar = True 
    # changes the thumbnail for locked items, default is images/locked.png
    gallernpy.change_locked("image_locked")  
    # change the transition to show a image or animation, default is dissolve. The argument must be a valid renpy transition
    gallernpy.change_transition(show_transition)  
    
```

And after adding everything, you can add some button to display the gallerynpy screen

```renpy
# For show the gallerynpy screen
screen main_menu():
    # .......
    # .......
    textbutton _("Gallery") action ShowMenu("gallerynpy")  # this will be show the gallerynpy screen
```

## Gallerynpy methods

The gallerynpy object has some methods you can use.

```text
put_image(image, where, song=None, condition=None)
  Args:
    image: Can be the filepath to image file or the name of the image declaration.
    where: The slide where the image will be put.
    song: The filepath to the song that will be played when image is showed, default is None.
    condition: The condition for unlock image, default is unlocked.
    
put_video(filename, where, thumbnail=None, song=None, condition=None)
  Args:
    filename: Must be the filepath to video file.
    where: The slide where the item video be put.
    thumbnail: The image name or image path for put as video thumbnail.
    song: The filepath to the song that will be played when video is played, default is None.
    condition: The condition for unlock image, default is unlocked.
    
put_animation(atl_object, thumbnail_name, where=gallerynpy_properties.animation_slide, song=None, condition=None)
  Args:
    atl_object: Must be the name's atl animation block.
    where: The slide where the animation will be put, default is animations.
    thumbnail_name: Can be the filepath to image file or the name of the image declaration to set as thumbnail.
    song: The filepath to the song that will be played when video is played, default is None.
    condition: The condition for unlock image, default is unlocked.
    
change_distribution(rows=None, columns=None)
  Change the distribution of items on screen.
  If config.screen_width is lees or equal to __min_screen (default 1280), columns and rows ever are 3
  I recommend you 3x3 (default) if your game screen width is equal to 1280 or 4x5 if is 1980
  Use this method before use put methods (put_image, put_video, put_animation).
  Args:
      rows: a valid rows number
      columns: a valid columns number 

change_locked(image)
  Changes the thumbnail for locked item
  Args:
    image: Can be the filepath to image file, the name of the image declaration or a Image object
  
change_transition(transition)
  Change the transition for show item (image and animation)
  Args:
    transition: A valid renpy transition object
  
slides()
  Returns the current all slide names
 
change_slide(slide):
  Changes the current slide.
  If slide isn't inside the current slides, doesnt change.
  Args:
      slide: the new current slide name
```

## Gallerynpy properties
For some styles, gallerynpy use some properties from gallerynpy_properties object. I recommend that you change only those shown below.

```text
font_size
 A valid font size, it's used for font size on gallerynpy screen.
 
font
 A valid path to font resource (ttf or otf), it's used as font on gallerynpy screen.
 
color
 A valid hexadecimal color, it's used for font color on gallerynpy screen.
 
hover_color
 A valid hexadecimal color, it's used for color when slide names are hovered
 
selected_color
 A valid hexadecimal color, it's used for color when slide name is selected
 
insensitive_color
 A valid hexadecimal color, it's used for color when slide name is not selected
```

## Gallerynpy names
To display the name of the slide as a text button, gallerynpy tries to use the value inside the gallerynpy_names dictionary if slide is a key of the dictionary. Otherwise the capitalized slide name will be used.
```renpy
init 999 python:
    # ........
    # ........
    # after adding all elements, for example, if you have only added elements to img and anim as slides (where) name.
    # the following will display Images and Animations instead of img and anim as button text
    gallerynpy_names['img'] = "Images"
    gallerynpy_names["anim"] = "Animations"
```

## License

This project is licensed under the MIT License - see the [LICENSE](gallerynpy/LICENSE) file for details.

## Acknowledgments

- This script was inspired by similar scripts created by the Ren'Py community.

## Problems

If you encounter any problems or bugs while using the script, please open an issue in the GitHub repository.

Thanks for using my script! If you have any questions or suggestions, feel free to contact me.
