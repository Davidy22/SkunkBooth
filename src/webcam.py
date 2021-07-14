from asciimatics.renderers import DynamicRenderer

from CamReader import CamReader
from asciiGen import ASCIIGen


class Webcam(DynamicRenderer):
    """Webcam widget for ASCIImatics"""

    def __init__(self, asciiGen: ASCIIGen, height: int = 30, width: int = 30):
        """The init function

        :param ascii_renderer: Converter from image data to ASCII art
        :param height: The allocated height for the widget
        :param width: The allocated width for the widget
        """
        super().__init__(height, width)
        self.camera = CamReader()
        self.ascii = asciiGen
        self.image = None

    def _render_now(self):
        """Extract image from camera, convert to ASCII, print to terminal"""
        # TODO: Use actual webcam resolution
        image = self.camera.convert_cv2_to_pil(self.camera.capture_image(400, 300))

        self.image = self.ascii.convert(image)

        for y, row in enumerate(self.image):
            for x, i in enumerate(row):
                self._write(i[0], x, y, i[2], i[1], i[3])
        return self._plain_image, self._colour_map

    def close_camera(self):
        self.camera.close_camera()
