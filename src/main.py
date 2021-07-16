from time import time

from asciimatics.effects import Print
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from asciiGen import Blocks
from fileIO import VideoIO
from filterManager import filterManager
from frames import GalleryFrame, MainFrame
from webcam import Webcam

vid = VideoIO()
screen = Screen.open(unicode_aware=True)
last_scene = None
converter = Blocks(
    int(screen.height), int(screen.width), uni=True, fill_background=True
)
filters = filterManager()
filters.load("Snowman")
filters.load("Invert")
webcam = Webcam(converter, filters, int(screen.height / 1.2), int(screen.width / 1.2))
effects = []
effects.append(MainFrame(screen, webcam))
effects.append(
    Print(screen, webcam, y=int(screen.height / 12), x=int(screen.width / 6))
)
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
            webcam.resize(int(screen.height / 1.2), int(screen.width / 1.2))
            converter.resize(int(screen.height), int(screen.width))
            effects.append(MainFrame(screen, webcam))
            effects.append(
                Print(screen, webcam, y=int(screen.height / 6), x=int(screen.width / 4))
            )
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
    except ResizeScreenError as e:
        last_scene = e.scene
        screen.close()
        quit(0)
    except (StopApplication, KeyboardInterrupt):
        screen.close()
        quit(0)
