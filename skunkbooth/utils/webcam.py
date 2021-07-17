from sys import platform
from typing import List, Tuple

from asciimatics.renderers import DynamicRenderer

from skunkbooth.data.constants import palette8

from .asciiGen import ASCIIGen
from .CamReader import CamReader
from .fileIO import ImageIO
from .filterManager import filterManager


class Webcam(DynamicRenderer):
    """Webcam widget for ASCIImatics"""

    def __init__(
        self,
        asciiGen: ASCIIGen,
        filters: filterManager,
        height: int = 30,
        width: int = 30,
    ):
        """
        The init function

        :param ascii_renderer: Converter from image data to ASCII art
        :param height: The allocated height for the widget
        :param width: The allocated width for the widget
        """
        super().__init__(height, width)
        self.camera = CamReader()
        self.ascii = asciiGen
        self.filters = filters
        self.image = None

    def resize(self, height: int, width: int) -> None:
        """Resize output"""
        super().__init__(height, width)

    def take_picture_and_save(self, img_name: str) -> None:
        """Takes an Image snapshot and saves it"""
        image_to_save = self.image
        img_io = ImageIO(dest=img_name)
        img_io.write(image_to_save)

    def _render_now(self) -> Tuple[List, List]:
        """Extract image from camera, convert to ASCII, print to terminal"""
        image = self.camera.convert_cv2_to_pil(self.camera.capture_image())
        image = self.filters.pil_filter(image)

        self.image = self.ascii.convert(image)
        self.image = self.filters.ascii_filter(self.image)

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
