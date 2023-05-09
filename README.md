# Gallerynpy

Gallerynpy is a Ren'Py script that allows you to display a gallery screen in your visual novel. The gallery screen displays all images, animations and videos that have been inserted into the gallerynpy object.

## Usage

To use Gallerynpy, simply add the script and all resource files to your Ren'Py project and call the "gallerynpy" menu whenever you want to display the gallery screen. You can customize the appearance of the gallery display by modifying the provided screens and styles.

Before displaying the gallerynpy screen you should add some images, animations or videos into the gallerynpy object. I recommend that you do this in a python init block with a high wait number such as 999.

```renpy
init 999 python:

    ### IMPORTANT
    """
    About the thumbnails to be displayed on the gallerynpy screen:

        For images, you don't need to create or specify any file, since by default the same image will be displayed as thumbnail.

        For videos, you need to create a image file in the path 'images/gallerynpy/thumbnails' with name videoname_thumbnail.jpg 
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
    # You also can specify the condition for unlock the video add the condition argument
    gallerynpy.put_video("videos/wonderful.mp4", "videos", condition="persistent.valid_condition")

    # For add a animation, you need to specify at least the first two arguments, first the name of 
    # an atl (animation) block declaration in your renpy project and second a path or a valid name of 
    # an image declaration in renpy for use as thumbnail.
    gallerynpy.put_animation("wonderful_screen_animation", "wonderful_screen")
    # You also can specify the slide (where) and the condition for unlock the animation
    # if you don't specify the third argument, default slide is 'animations'
    gallerynpy.put_animation("wonderful_screen_animation", "wonderful_screen", "anim", condition="persistent.valid_condition")  

    # You can also change some properties in gallerynpy
    # for specify the initial slide to show
    gallerynpy.current_page = "images"  
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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This script was inspired by similar scripts created by the Ren'Py community.

## Problems

If you encounter any problems or bugs while using the script, please open an issue in the GitHub repository.

Thanks for using my script! If you have any questions or suggestions, feel free to contact me.
