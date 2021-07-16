import os
from time import time
from typing import Tuple

from asciimatics.effects import Print
from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from asciiGen import Blocks
from fileIO import VideoIO
from frames import GalleryFrame, MainFrame
from logger import CustomLogger
from webcam import Webcam

logger = CustomLogger(fileoutpath="Logs" + os.sep + "ui.log")

FIGLET_MAXHEIGHT = 8
vid = VideoIO()
screen = Screen.open(unicode_aware=True)

logger._log_info("Screen initialized Height:{} Width:{}".format(screen.height, screen.width))

last_scene = None
converter = Blocks(screen.height,
                   screen.width,
                   uni=True,
                   fill_background=True)
# webcam_scale = 1.2
# webcam_height = int(screen.height / webcam_scale)
# webcam_width = int(screen.width / webcam_scale)


def CamDimensions(height: int, width: int) -> Tuple[int, int, int]:
    """Calculate dimensions for vertical squeeze screen sizes"""
    if(width/height >= 4):
        var_dim = int(height*2)  # Max width is around twice height in most cases
        offset = int(width/2-var_dim/2-width/6)
        return (height, var_dim, offset)
    # Add margins of 1/6x,y if no vertical squeeze
    height = int(height*2/3)
    width = int(width*2/3)
    return (height, width, 2)


(webcam_height, webcam_width, offset) = CamDimensions(screen.height, screen.width)

logger._log_info("Webcam Height:{} Webcam Width:{} Offset:{}".format(webcam_height, webcam_width, offset))

webcam = Webcam(converter, webcam_height, webcam_width)
effects = []
header_figlet = Print(screen, FigletText("Photobooth", width=screen.width), 0,
                      colour=Screen.COLOUR_RED)
effects.append(header_figlet)
effects.append(MainFrame(screen, webcam))

effects.append(
    Print(screen, webcam, y=FIGLET_MAXHEIGHT+3, x=int(screen.width/6)+offset
          #   y=screen.height - webcam_height >> 1,
          #   x=screen.width - webcam_width >> 1
          ))
scenes = [
    Scene(effects, -1, name="Main"),
    Scene([GalleryFrame(screen)], -1, name="Gallery"),
]
screen.set_scenes(scenes)
b = a = 0
while True:
    try:
        if screen.has_resized():
            screen.close()
            screen = Screen.open(unicode_aware=True)
            effects = []
            effects.append(header_figlet)
            (webcam_height, webcam_width, offset) = CamDimensions(screen.height, screen.width)
            webcam.resize(webcam_height, webcam_width)
            converter.resize(screen.height, screen.width)
            effects.append(header_figlet)
            effects.append(MainFrame(screen, webcam))
            # webcam_height = int(screen.height / webcam_scale)
            # webcam_width = int(screen.width / webcam_scale)
            effects.append(
                Print(screen, webcam,
                      y=FIGLET_MAXHEIGHT+3, x=int(screen.width/6)+offset,
                      #   y=screen.height - webcam_height >> 1,
                      #   x=screen.width - webcam_width >> 1
                      ))
            scenes = [
                Scene(effects, -1, name="Main"),
                Scene([GalleryFrame(screen)], -1, name="Gallery"),
            ]

            screen.set_scenes(scenes)
        screen.draw_next_frame()
        b = time()
        if b - a < 0.05:
            pause = max(0, min(0.007, a + 0.007 - b))
            screen.wait_for_input(pause)
        a = b
        # screen.play(scenes, stop_on_resize=True, allow_int=True)
        # screen.close()
        # sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
