from typing import Tuple

from asciimatics.effects import Print
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
                                 screen.height // 2,
                                 uni=True,
                                 fill_background=True)
        # ascci = img.get_ascci()
        # print(ascci)
        # sleep(100)
        effects = [
            Print(screen, img, y=position[1], x=position[0], stop_frame=200),
        ]
        screen.play([Scene(effects, 500)], stop_on_resize=True)
        return


if __name__ == "__main__":
    a = ascci()
    img = Image.open("src/data/bw.jpg")
    Screen.wrapper(a.show_image, arguments=(
        img,
        (0, 0),
    ), catch_interrupt=True)
