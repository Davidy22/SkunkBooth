from typing import Tuple

from asciimatics.effects import Print
from asciimatics.exceptions import StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from asciimatics_mod import ColourImageFilePIL
from CamReader import CamReader


class ascci:
    """Generic ascii methods"""

    def __init__(self) -> None:
        pass

    def show_image(self, screen: Screen, image: ColourImageFilePIL,
                   position: Tuple) -> None:
        """Show ascii image in terminal

        :param screen: The screen to use when displaying the image.
        :param image: Color image from asccimatics.
        :param position: The position of image on terminal.
        """
        effects = [
            Print(screen, image, y=position[1], x=position[0], stop_frame=200),
        ]
        screen.set_scenes([Scene(effects, 0)])
        try:
            for _ in range(4):
                screen.draw_next_frame()
                if screen.has_resized():
                    # screen.force_update()
                    screen.set_scenes([Scene(effects, 100)])
        except StopApplication:
            # Time to stop  - just exit the function.
            return
        # screen.play([Scene(effects, 500)], stop_on_resize=True)
        return


if __name__ == "__main__":
    a = ascci()
    c = CamReader()
    # img = Image.open("src/data/bw.jpg")
    screen = Screen.open(unicode_aware=True)
    while True:
        try:
            img = c.convert_cv2_to_pil(c.capture_image(200, 200))
            image = ColourImageFilePIL(screen,
                                       img,
                                       screen.height // 2 + 5,
                                       uni=True,
                                       fill_background=True)
            # screen.force_update(True)
            a.show_image(
                screen,
                image,
                (0, 0),  # figure out how to center it
            )
        except KeyboardInterrupt:
            c.close_camera()
            screen.close()
        # sleep(0.1)
    screen.close()
