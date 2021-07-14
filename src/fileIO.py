from json import load
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

        cLookup = load(open("data/colours.json"))
        self.colours = {i: Image.new("RGB", (self.fx, self.fy)) for i in range(256)}
        for i in self.colours:
            self.colours[i].paste(
                tuple(cLookup[str(i)]["rgb"].values()), (0, 0, self.fx, self.fy)
            )
        self.underline = Image.new("RGBA", (self.fx, self.fy))
        ImageDraw.Draw(self.underline).line(
            (0, self.fy - self.fy // 11, self.fx, self.fy - self.fy // 11),
            width=self.fy // 8,
        )

    def convert(self, image: List[List[Tuple[int, int, int]]]) -> array:
        """
        Converts ASCII images to opencv format images to use in opencv writers.

        Pixels formatted as (keycode, attribute, 8 bit colour)
        """
        ay = len(image)
        ax = len(image[0])
        out = Image.new("RGB", (ax * self.fx, ay * self.fy))

        for y in range(ay):
            for x in range(ax):
                # TODO: Implement effects parameter
                # TODO: Implement background color
                char = chr(image[y][x][0])
                if char not in self.glyphs:
                    # Cache character glyphs
                    glyph = Image.new("RGBA", (self.fx, self.fy))
                    ImageDraw.Draw(glyph).text((0, 0), char, font=self.font)
                    self.glyphs[char] = glyph

                # Render character, (text colour, bg colour, char, attribute)
                charD = (image[y][x][2], 0, char, image[y][x][1])
                if charD in self.renderCache:
                    render = self.renderCache[charD]
                else:
                    fg = self.colours[charD[0]]
                    bg = self.colours[charD[1]]
                    glyph = self.glyphs[charD[2]]

                    # Attributes
                    if charD[3] in constants.L_BOLD:
                        if charD[2] + "bold" in self.glyphs:
                            glyph = self.glyphs[charD[2] + "bold"]
                        else:
                            temp = glyph.copy()
                            temp.paste(glyph, (self.fx // 20, 0), glyph)
                            temp.paste(glyph, (0, self.fy // 20), glyph)
                            glyph = self.glyphs[charD[2] + "bold"] = temp
                    if charD[3] in constants.L_REVERSE:
                        fg, bg = bg, fg
                    if charD[3] in constants.L_UNDERLINE:
                        glyph = glyph.copy()
                        glyph.paste(self.underline, (0, 0), self.underline)
                    render = self.renderCache[charD] = Image.composite(fg, bg, glyph)

                    if len(self.renderCache) > self.maxCache:
                        self.renderCache.pop(next(iter(self.renderCache)))

                out.paste(render, (x * self.fx, y * self.fy))
        return array(out)


class videoIO(IOBase):  # TODO: Other video filetypes
    """ASCII to video saver"""

    def __init__(self, dim: Tuple[int, int] = None, dest: str = "out.avi"):
        """
        Set image dimensions and destination, dimensions must remain constant while recording.

        dim: Character dimensions of the ASCII video. Inferred from first frame if missing
        dest: File destination to save to.
        """
        super().__init__()
        if dim is None:
            self.dest = dest
        else:
            self.dest = VideoWriter(
                dest,
                VideoWriter_fourcc(*"DIVX"),
                20,
                (dim[0] * self.fx, dim[1] * self.fy),
            )

    def write(self, image: List[List[Tuple[int, int, int]]]) -> None:
        """Write a frame to the video."""
        if self.dest is None:
            raise Exception("Attempted write to closed file")
        elif isinstance(self.dest, str):
            self.dest = VideoWriter(
                self.dest,
                VideoWriter_fourcc(*"DIVX"),
                20,
                (len(image[0]) * self.fx, len(image) * self.fy),
            )

        self.dest.write(self.convert(image))

    def close(self) -> None:
        """Close and save the video file."""
        self.dest.release()
        self.dest = None


class ImageIO(IOBase):
    """ASCII to image saver"""

    def __init__(self, dest: str = "SaveImage.jpg"):
        self.dest = dest
        super().__init__()

    def write_to_file(self, image: List[List[Tuple[int, int, int]]]) -> bool:
        """For writing image to file"""
        return imwrite(self.dest, self.convert(image))


if __name__ == "__main__":
    import random

    v = videoIO()
    [
        v.write(
            [
                [
                    (
                        random.randint(97, 122),
                        random.randint(1, 8),
                        (i + (j + 1) * (k + 1)) % 255,
                    )
                    for j in range(20)
                ]
                for k in range(20)
            ]
        )
        for i in range(400)
    ]
    v.close()

    image = [[(
        chr(random.randint(97, 122)),
        random.randint(1, 8),
        (0 + (j + 1) * (k + 1)) % 255,
        random.randint(250, 255),
    ) for j in range(20)] for k in range(20)]
    wtr_img = ImageIO()
    wtr_img.write_to_file(image=image)
