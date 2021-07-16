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
converter = Blocks(
    screen.height, screen.width, uni=True, fill_background=True
)
webcam = Webcam(converter, int(screen.height*2/3), int(screen.width*2/3))
header_figlet = Print(screen, FigletText("Photobooth", width=screen.width), 0,
                      colour=Screen.COLOUR_RED)
effects = []
effects.append(header_figlet)
effects.append(MainFrame(screen, webcam))
effects.append(Print(screen, webcam, y=FIGLET_MAXHEIGHT+3, x=int(screen.width/6)))
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
            webcam.resize(int(screen.height*2/3), int(screen.width*2/3))
            converter.resize(screen.height, screen.width)
            effects.append(header_figlet)
            effects.append(MainFrame(screen, webcam))
            effects.append(Print(screen, webcam, y=FIGLET_MAXHEIGHT+3, x=int(screen.width/6)))
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
