import logging
from functools import lru_cache
from os import path
from sys import platform
from typing import List, Tuple

from cv2 import VideoWriter, VideoWriter_fourcc, imwrite
from numpy import array
from PIL import Image, ImageDraw, ImageFont

from skunkbooth.data import constants


class IOBase:
    """ASCII conversion module, subclass for access to convert()"""

    def __init__(self, font: str = "Hack", fontSize: int = 30):
        self.fx, self.fy = 0, 0
        self.setFont(font, fontSize)

    def setFont(self, fp: str, size: int) -> None:
        """Set render font, fall back to Input if font name is invalid"""
        fp = f'{path.join(path.dirname(path.abspath(__file__)), "..", "data", fp)}.ttf'
        try:
            self.font = ImageFont.truetype(fp, size)
        except OSError:
            logging.error(f"Font {fp} not found, falling back.")
            fp = f'{path.join(path.dirname(path.abspath(__file__)), "..", "data", "Hack.ttf")}'
            self.font = ImageFont.truetype(fp, size)

        px, py = self.fx, self.fy
        self.fx, self.fy = self.font.getsize("g")
        self.renderPixel.cache_clear()
        self.renderGlyph.cache_clear()
        self.bold = max(1, size // 30)

        if (px, py) != (self.fx, self.fy):
            self.colours = {i: Image.new("RGB", (self.fx, self.fy)) for i in range(256)}
            for i in self.colours:
                self.colours[i].paste(
                    tuple(reversed(constants.palette[i * 3:i * 3 + 3])),
                    (0, 0, self.fx, self.fy),
                )
            self.underline = Image.new("L", (self.fx, self.fy))
            self.underline.paste(255, (0, self.fy - self.fy // 11, self.fx, self.fy))

    def write(self, image: List[List[Tuple[int, int, int]]]) -> bool:
        """Template method for write()"""
        return False

    def convert(self, image: List[List[Tuple[int, int, int, int]]]) -> array:
        """
        Converts ASCII images to opencv format images to use in opencv writers.

        Pixels formatted as (keycode, attribute, 8 bit colour)
        """
        ay = len(image)
        ax = len(image[0])
        out = Image.new("RGB", (ax * self.fx, ay * self.fy))

        for y in range(ay):
            for x in range(ax):
                out.paste(self.renderPixel(image[y][x]), (x * self.fx, y * self.fy))
        return array(out)

    @lru_cache(maxsize=None)
    def renderPixel(self, pixel: Tuple) -> Image:
        """Cached full "pixel" render method"""
        # Just draw background if character is empty
        if len(pixel) == 1:
            return self.colours[pixel[0]]

        # Render character, (text colour, bg colour, char, attribute)
        fg = self.colours[pixel[2]]
        bg = self.colours[pixel[3]]
        attr = pixel[1]
        char = pixel[0]

        # Attributes
        # TODO: Generalise attribute code flattening for more than just bold chars
        glyph = self.renderGlyph(char, constants.A_BOLD if attr in constants.L_BOLD else constants.A_NORMAL)
        if attr in constants.L_REVERSE:
            fg, bg = bg, fg
        if attr in constants.L_UNDERLINE:
            glyph = glyph.copy()
            glyph.paste(self.underline, (0, 0), self.underline)
        return Image.composite(fg, bg, glyph)

    @lru_cache(maxsize=None)
    def renderGlyph(self, char: str, attr: str) -> Image:
        """Cached glyph render method"""
        glyph = Image.new("L", (self.fx, self.fy))
        ImageDraw.Draw(glyph).text(
            (0, 0), char, 255, font=self.font, stroke_width=self.bold if attr in constants.L_BOLD else 0
        )
        return glyph


class VideoIO(IOBase):  # TODO: Other video filetypes
    """ASCII to video saver"""

    def __init__(
        self,
        dim: Tuple[int, int] = None,
        fps: int = 60,
        dest: str = "out.avi",
        **kwargs,
    ):
        """
        Set image dimensions and destination, dimensions must remain constant while recording.

        dim: Character dimensions of the ASCII video. Inferred from first frame if missing
        dest: File destination to save to.
        """
        super().__init__(**kwargs)
        if dim is None:
            self.dest = dest
            self.fps = fps
        else:
            self.dest = VideoWriter(
                dest,
                VideoWriter_fourcc(*"DIVX"),
                fps,
                (dim[0] * self.fx, dim[1] * self.fy),
            )

    def write(self, image: List[List[Tuple[int, int, int]]]) -> bool:
        """Write a frame to the video."""
        if self.dest is None:
            raise Exception("Attempted write to closed file")
        elif isinstance(self.dest, str):
            self.dest = VideoWriter(
                self.dest,
                VideoWriter_fourcc(*"DIVX"),
                self.fps,
                (len(image[0]) * self.fx, len(image) * self.fy),
            )

        try:
            self.dest.write(self.convert(image))
            return True
        except Exception:
            return False

    def close(self) -> None:
        """Close and save the video file."""
        try:
            self.dest.release()
        except Exception:
            return
        self.dest = None


class ImageIO(IOBase):
    """ASCII to image saver"""

    def __init__(self, dest: str = "Gallery/SaveImage.jpg", **kwargs):
        super().__init__(**kwargs)
        self.dest = dest

    def write(self, image: List[List[Tuple[int, int, int]]], dest: str = None) -> bool:
        """For writing image to file"""
        return imwrite(dest if dest else self.dest, self.convert(image))


class AsciiIO(IOBase):
    """ASCII to text saver"""

    def __init__(self, dest: str = "out", **kwargs):
        super().__init__(**kwargs)
        self.dest = dest
        if platform == "win32":
            self.dest += ".txt"

    def write(self, image: List[List[Tuple[int, int, int]]], dest: str = None) -> bool:
        """For writing image to file"""
        with open(dest if dest else self.dest, "w") as f:
            return f.write("\n".join("".join(j[0] for j in i) for i in image))
