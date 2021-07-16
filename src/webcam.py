import threading
from sys import platform
from threading import Thread
from typing import List, Tuple

from asciimatics.renderers import DynamicRenderer

from asciiGen import ASCIIGen, Blocks
from CamReader import CamReader
from data.constants import palette8
from fileIO import ImageIO


class Webcam(DynamicRenderer):
    """Webcam widget for ASCIImatics"""

    def __init__(self, asciiGen: ASCIIGen, height: int = 30, width: int = 30):
        """
        The init function

        :param ascii_renderer: Converter from image data to ASCII art
        :param height: The allocated height for the widget
        :param width: The allocated width for the widget
        """
        super().__init__(height, width)
        self.camera = CamReader()
        self.ascii = asciiGen
        self.image = None
        self.stopped = False

    def resize(self, height: int, width: int) -> None:
        """Resize output"""
        super().__init__(height, width)

    def take_picture_and_save(self) -> None:
        """Takes an Image snapshot and saves it"""
        image_to_save = self.image
        img_io = ImageIO()
        img_io.write(image=image_to_save)

    def start(self) -> None:
        """Starting a thread for renderer"""
        self.stopped = False
        Thread(target=self._render_now, args=()).start()
        return self

    def _render_now(self) -> Tuple[List, List]:
        """Extract image from camera, convert to ASCII, print to terminal"""
        # image = self.camera.convert_cv2_to_pil(self.camera.capture_image())
        # while not self.stopped:
        print(self.camera.frame)
        if self.camera.frame is None:
            return
        print("oof")
        self.image = self.ascii.convert(self.camera.get_image())
        print(self.image)
        for y, row in enumerate(self.image):
            for x, i in enumerate(row):
                if platform == "win32":
                    self._write(i[0], x, y, palette8[i[2]], i[1], palette8[i[3]])
                else:
                    self._write(i[0], x, y, i[2], i[1], i[3])
        # self.rendered_text(self._plain_image)
        print(self._colour_map)
        # return self._plain_image, self._colour_map

    def close_camera(self) -> None:
        """Close webcam"""
        self.stopped = True
        self.camera.close_camera()


if __name__ == '__main__':
    converter = Blocks(
        int(200), int(200), uni=True, fill_background=True)
    webcam = Webcam(converter, int(200 / 1.2), int(200 / 1.2))
    count = 0
    cam = webcam.camera.start()
    show = webcam.start()

    while (not webcam.stopped) and count < 500:
        for thread in threading.enumerate():
            print(thread.name)
        show._render_now()
        cam.read_cam()
        print(count)
        count = count + 1
    webcam.close_camera()
