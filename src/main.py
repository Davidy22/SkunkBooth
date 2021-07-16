from time import time

from asciimatics.effects import Print
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from asciiGen import Blocks
from fileIO import VideoIO
from filterManager import filterManager
from frames import FilterFrame, GalleryFrame, MainFrame
from webcam import Webcam

vid = VideoIO()
screen = Screen.open(unicode_aware=True)
last_scene = None
converter = Blocks(
    int(screen.height), int(screen.width), uni=True, fill_background=True
)
filters = filterManager()
webcam_scale = 1.2
webcam_height = int(screen.height / webcam_scale)
webcam_width = int(screen.width / webcam_scale)
webcam = Webcam(converter, filters, webcam_height, webcam_width)
effects = []
effects.append(MainFrame(screen, webcam))
effects.append(
    Print(
        screen,
        webcam,
        y=screen.height - webcam_height >> 1,
        x=screen.width - webcam_width >> 1,
    )
)
fFrame = FilterFrame(screen, filters)
scenes = [
    Scene(effects, -1, name="Main"),
    Scene([GalleryFrame(screen)], -1, name="Gallery"),
    Scene([fFrame], -1, name="Filters")
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
                Print(
                    screen,
                    webcam,
                    y=screen.height - webcam_height >> 1,
                    x=screen.width - webcam_width >> 1,
                )
            )
            fNext = FilterFrame(screen, filters, data=fFrame._data)
            fFrame = fNext
            scenes = [
                Scene(effects, -1, name="Main"),
                Scene([GalleryFrame(screen)], -1, name="Gallery"),
                Scene([fFrame], -1, name="Filters"),
            ]
            screen.set_scenes(scenes)

        screen.draw_next_frame()
        b = time()
        if b - a < 0.05:
            pause = max(0, min(0.001, a + 0.001 - b))
            screen.wait_for_input(pause)
        else:
            screen.wait_for_input(0)
        a = b
    except ResizeScreenError as e:
        last_scene = e.scene
        screen.close()
        quit(0)
    except (StopApplication, KeyboardInterrupt):
        screen.close()
        quit(0)
