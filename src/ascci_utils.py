import sys

from asciimatics.effects import Print
from asciimatics.exceptions import ResizeScreenError
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from asciiGen import Blocks
from fileIO import VideoIO
from frames import GalleryFrame, MainFrame
from webcam import Webcam

vid = VideoIO()
screen = Screen.open(unicode_aware=True)
last_scene = None
while True:
    try:
        converter = Blocks(int(screen.height), int(screen.width), uni=True, fill_background=True)
        webcam = Webcam(converter, int(screen.height/1.2), int(screen.width/1.2))
        effects = []
        effects.append(MainFrame(screen, webcam))
        effects.append(Print(screen, webcam, y=int(screen.height/12), x=int(screen.width/6)))
        scenes = [Scene(effects, -1, name="Main"),
                  Scene([GalleryFrame(screen)], -1, name="Gallery")
                  ]
        screen.play(scenes, stop_on_resize=True, allow_int=True)
        webcam.close_camera()
        screen.close()
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
