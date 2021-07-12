from time import sleep
from typing import Tuple

from asciimatics.effects import Print
from asciimatics.exceptions import StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from PIL import Image

from ascii_images import ColourImageFilePIL

# Copying colors here for reference. Delete later
# COLOUR_BLACK = 0
# COLOUR_RED = 1
# COLOUR_GREEN = 2
# COLOUR_YELLOW = 3
# COLOUR_BLUE = 4
# COLOUR_MAGENTA = 5
# COLOUR_CYAN = 6
# COLOUR_WHITE = 7

# A_BOLD = 1
# A_NORMAL = 2
# A_REVERSE = 3
# A_UNDERLINE = 4


class ascci:
    """Generic ascii methods"""

    def __init__(self) -> None:
        pass

    def show_image(self, screen, image: Image, position: Tuple) -> None:
        """Show ascii image in terminal

        :param screen: The screen to use when displaying the image.
        :param image: The PIL image object.
        :param position: The position of image on terminal.
        """
        img = ColourImageFilePIL(screen,
                                 image,
                                 screen.height // 2 + 5,
                                 uni=True,
                                 fill_background=True)
        # ascci = img.get_ascci()
        # print(ascci)
        # sleep(100)
        effects = [
            Print(screen, img, y=position[1], x=position[0], stop_frame=200),
        ]
        screen.set_scenes([Scene(effects, 500)])
        try:
            for _ in range(4):
                screen.draw_next_frame()
                if screen.has_resized():
                    # screen.force_update()
                    screen.set_scenes([Scene(effects, 500)])
                    # screen.close()
                    # print("Dont resize :)")
                    # break
                # sleep(0.1)
        except StopApplication:
            # Time to stop  - just exit the function.
            return
        # screen.play([Scene(effects, 500)], stop_on_resize=True)
        return


if __name__ == "__main__":
    a = ascci()
    img = Image.open("src/data/bw.jpg")
    screen = Screen.open(unicode_aware=True)
    a.show_image(
        screen,
        img,
        (0, 0),  # figure out how to center it
    )
    # now we can control how long image stays on screen
    # using sleep()
    sleep(5)
    screen.close()
