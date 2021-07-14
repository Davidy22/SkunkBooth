from asciimatics.effects import Print
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from tqdm import tqdm

from asciiGen import Blocks
from fileIO import VideoIO
from webcam import Webcam

vid = VideoIO()
screen = Screen.open(unicode_aware=True)
converter = Blocks(screen.height, screen.width, uni=True, fill_background=True)
webcam = Webcam(converter, screen.height, screen.width)
screen.set_scenes([Scene([Print(screen, webcam, y=0, x=0)], 0)])

try:
    for i in tqdm(range(99999)):
        screen.draw_next_frame()
        if webcam.image is not None:
            vid.write(webcam.image)
except KeyboardInterrupt:
    webcam.close_camera()
    screen.close()
screen.close()
vid.close()
