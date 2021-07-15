import sys

from asciimatics.effects import Print
from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from asciiGen import Blocks
from fileIO import VideoIO
from frames import GalleryFrame, MainFrame
from webcam import Webcam

vid = VideoIO()
screen = Screen.open(unicode_aware=True)
last_scene = None
print(screen.height, screen.width)
while True:
    try:
        converter = Blocks(screen.height, screen.width, uni=True, fill_background=True)
        webcam = Webcam(converter, int(screen.height*2/3), int(screen.width*2/3))
        header_figlet = Print(screen, FigletText("Photobooth", width=screen.width), 0,
                              colour=Screen.COLOUR_RED)
        effects = []
        effects.append(header_figlet)
        effects.append(MainFrame(screen, webcam))
        effects.append(Print(screen, webcam, y=int(screen.height/6)
                       if int(screen.height/6) > 10 else 10, x=int(screen.width/6)))
        scenes = [Scene(effects, -1, name="Main"),
                  Scene([header_figlet, GalleryFrame(screen)], -1, name="Gallery")
                  ]
        screen.play(scenes, stop_on_resize=True, allow_int=True)
        webcam.close_camera()
        screen.close()
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
