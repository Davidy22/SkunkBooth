from time import time

from asciimatics.effects import Print
from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from asciiGen import Blocks
from fileIO import VideoIO
from frames import GalleryFrame, MainFrame
from webcam import Webcam

FIGLET_MAXHEIGHT = 7
vid = VideoIO()
screen = Screen.open(unicode_aware=True)
last_scene = None
converter = Blocks(int(screen.height),
                   int(screen.width),
                   uni=True,
                   fill_background=True)
webcam_scale = 1.2
webcam_height = int(screen.height / webcam_scale)
webcam_width = int(screen.width / webcam_scale)
webcam = Webcam(converter, webcam_height, webcam_width)
effects = []
header_figlet = Print(screen, FigletText("Photobooth", width=screen.width), 0,
                      colour=Screen.COLOUR_RED)
effects.append(header_figlet)
effects.append(MainFrame(screen, webcam))
effects.append(
    Print(screen,
          webcam,
          y=screen.height - webcam_height >> 1,
          x=screen.width - webcam_width >> 1))
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
            webcam.resize(webcam_height, webcam_width)
            converter.resize(int(screen.height), int(screen.width))
            effects.append(MainFrame(screen, webcam))
            webcam_height = int(screen.height / webcam_scale)
            webcam_width = int(screen.width / webcam_scale)
            effects.append(
                Print(screen,
                      webcam,
                      y=screen.height - webcam_height >> 1,
                      x=screen.width - webcam_width >> 1))
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
