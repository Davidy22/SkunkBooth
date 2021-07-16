from multiprocessing import Manager, Value
from sys import platform
from typing import List, Tuple

from asciimatics.renderers import DynamicRenderer

from asciiGen import ASCIIGen
from CamReader import CamReader
from data.constants import palette8
from fileIO import ImageIO, VideoIO
from logger import CustomLogger


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
        manager = Manager()
        self.manager_lst = manager.list()
        self.manager_lst.append(self.image)

    def resize(self, height: int, width: int) -> None:
        """Resize output"""
        super().__init__(height, width)

    def take_picture_and_save(self, img_name: str) -> None:
        """Takes an Image snapshot and saves it"""
        image_to_save = self.image
        img_io = ImageIO(dest=img_name)
        img_io.write(image=image_to_save)

    def recording_utility(self, val: Value) -> None:
        """Coninuously run in the background and check if recording is true"""
        v = VideoIO()
        while True:
            if val.value == 0:
                try:
                    lst = list(self.manager_lst)
                    CustomLogger._log_info(v.write(lst[0]))
                except Exception as e:
                    CustomLogger._log_error(e)
                    pass

    def _render_now(self) -> Tuple[List, List]:
        """Extract image from camera, convert to ASCII, print to terminal"""
        image = self.camera.convert_cv2_to_pil(self.camera.capture_image())

        self.image = self.ascii.convert(image)

        # Putting the images in manager so that recording_utilty can pick them up
        if len(self.manager_lst) != 0:
            self.manager_lst.pop()
        self.manager_lst.append(self.image)

        for y, row in enumerate(self.image):
            for x, i in enumerate(row):
                if platform == "win32":
                    self._write(i[0], x, y, palette8[i[2]], i[1], palette8[i[3]])
                else:
                    self._write(i[0], x, y, i[2], i[1], i[3])
        return self._plain_image, self._colour_map

    def close_camera(self) -> None:
        """Close webcam"""
        self.camera.close_camera()
