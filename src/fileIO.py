from sys import platform
from typing import List, Tuple

from cv2 import VideoWriter, VideoWriter_fourcc, imwrite
from numpy import array
from PIL import Image, ImageDraw, ImageFont

from data import constants


class IOBase:
    """ASCII conversion module, subclass for access to convert()"""

    def __init__(self):
        self.font = ImageFont.truetype("data/Input.ttf", 30)  # TODO: Font config
        self.fx, self.fy = self.font.getsize("g")
        self.glyphs = {}
        self.renderCache = {}
        self.maxCache = 5000

        self.colours = {i: Image.new("RGB", (self.fx, self.fy)) for i in range(256)}
        for i in self.colours:
            self.colours[i].paste(
                tuple(reversed(constants.palette[i * 3:i * 3 + 3])),
                (0, 0, self.fx, self.fy),
            )
        self.underline = Image.new("RGBA", (self.fx, self.fy))
        ImageDraw.Draw(self.underline).line(
            (0, self.fy - self.fy // 11, self.fx, self.fy - self.fy // 11),
            width=self.fy // 8,
        )

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
                # Just draw background if character is empty
                pixel = image[y][x]
                if len(pixel) == 1:
                    out.paste(self.colours[pixel[0]], (x * self.fx, y * self.fy))
                    continue

                char = pixel[0]
                if char not in self.glyphs:
                    # Cache character glyphs
                    glyph = Image.new("RGBA", (self.fx, self.fy))
                    ImageDraw.Draw(glyph).text((0, 0), char, font=self.font)
                    self.glyphs[char] = glyph

                # Render character, (text colour, bg colour, char, attribute)
                if pixel in self.renderCache:
                    render = self.renderCache[pixel]
                else:
                    fg = self.colours[pixel[2]]
                    bg = self.colours[pixel[3]]
                    glyph = self.glyphs[char]
                    attr = pixel[1]

                    # Attributes
                    if attr in constants.L_BOLD:
                        if char + "bold" in self.glyphs:
                            glyph = self.glyphs[char + "bold"]
                        else:
                            temp = glyph.copy()
                            temp.paste(glyph, (self.fx // 20, 0), glyph)
                            temp.paste(glyph, (0, self.fy // 20), glyph)
                            glyph = self.glyphs[char + "bold"] = temp
                    if attr in constants.L_REVERSE:
                        fg, bg = bg, fg
                    if attr in constants.L_UNDERLINE:
                        glyph = glyph.copy()
                        glyph.paste(self.underline, (0, 0), self.underline)
                    render = self.renderCache[pixel] = Image.composite(fg, bg, glyph)

                    if len(self.renderCache) > self.maxCache:
                        self.renderCache.pop(next(iter(self.renderCache)))

                out.paste(render, (x * self.fx, y * self.fy))
        return array(out)


class VideoIO(IOBase):  # TODO: Other video filetypes
    """ASCII to video saver"""

    def __init__(
        self, dim: Tuple[int, int] = None, fps: int = 60, dest: str = "out.avi"
    ):
        """
        Set image dimensions and destination, dimensions must remain constant while recording.

        dim: Character dimensions of the ASCII video. Inferred from first frame if missing
        dest: File destination to save to.
        """
        super().__init__()
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
        self.dest.release()
        self.dest = None


class ImageIO(IOBase):
    """ASCII to image saver"""

    def __init__(self, dest: str = "SaveImage.jpg"):
        self.dest = dest
        super().__init__()

    def write(self, image: List[List[Tuple[int, int, int]]]) -> bool:
        """For writing image to file"""
        return imwrite(self.dest, self.convert(image))


class AsciiIO(IOBase):
    """ASCII to text saver"""

    def __init__(self, dest: str = "out"):
        self.dest = dest
        if platform == "win32":
            self.dest += ".txt"
        super().__init__()

    def write(self, image: List[List[Tuple[int, int, int]]]) -> bool:
        """For writing image to file"""
        f = open(self.dest, "w")
        return f.write("\n".join("".join(j[0] for j in i) for i in image))


if __name__ == "__main__":
    import random

    v = VideoIO()
    [
        v.write(
            [
                [
                    (
                        chr(random.randint(97, 122)),
                        random.randint(1, 8),
                        (i + (j + 1) * (k + 1)) % 255,
                        random.randint(250, 255),
                    )
                    for j in range(20)
                ]
                for k in range(20)
            ]
        )
        for i in range(400)
    ]
    v.close()

    image = [
        [
            (
                chr(random.randint(97, 122)),
                random.randint(1, 8),
                (0 + (j + 1) * (k + 1)) % 255,
                random.randint(250, 255),
            )
            for j in range(20)
        ]
        for k in range(20)
    ]
    wtr_img = AsciiIO()
    wtr_img.write(image=image)
    wtr_img = ImageIO()
    wtr_img.write(image=image)
