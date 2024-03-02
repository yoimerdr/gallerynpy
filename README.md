# Gallerynpy

Gallerynpy are Ren'Py scripts which allows you to display a gallery screen in your visual novel. 
The gallery screen displays all images, animations and videos that have been inserted 
into gallerynpy.

## Usage

Before using gallerynpy, you need to download the [latest version](https://github.com/yoimerdr/gallerynpy/releases/latest) and copy it to your game.

Below is a simple use of gallerynpy. The game in which it is used is in `tutorial (renpy 8.2.0)`.

```renpy
image gallerynpy img example = "images/concert1.png"

image gallerynpy animation:
    # the concert# is an image file inside the images folder, renpy treats it automatically as an `image` type
    "concert1" with Dissolve(.1)
    pause .4
    "concert2" with Dissolve(.1)
    pause .4
    "concert3" with Dissolve(.1)
    pause .4
    "concert2" with Dissolve(.1)
    pause .4
    repeat

init python:
    gallerynpy.put_item("images", "gallerynpy img example")
    gallerynpy.put_item("animations", "gallerynpy animation", "concert1")
    gallerynpy.put_item("videos", "oa4_launch.webm")
    gallerynpy.properties.font_size = 18
    
```

And after adding and customising, you can add some button to display the gallerynpy screen

```renpy
# the renpy default navigation
screen navigation():
    vbox:
        # ..... other options
        textbutton _("Gallerynpy") action ShowMenu("gallerynpy")
        # ..... other options
```

## Docs

The web page of the documentation is still under development, for now you should read it directly 
from the methods/variables inside the .rpy files (or .py if you want to read it in the repository).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Problems

If you encounter any problems or bugs while using the script, please open an issue in the GitHub repository.

Thanks for using my script! If you have any questions or suggestions, feel free to contact me.
