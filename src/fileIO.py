from json import load
from typing import List, Tuple

from cv2 import VideoWriter, VideoWriter_fourcc
from numpy import array
from PIL import Image, ImageDraw, ImageFont


class IOBase:
    """ASCII conversion module, subclass for access to convert()"""

    def __init__(self):
        self.font = ImageFont.truetype("data/Input.ttf", 30)  # TODO: Font config
        self.fx, self.fy = self.font.getsize(" ")
        self.glyphs = {}
        self.renderCache = {}
        self.maxCache = 5000

        cLookup = load(open("data/colours.json"))
        self.colours = {i: Image.new("RGB", (self.fx, self.fy)) for i in range(256)}
        for i in self.colours:
            self.colours[i].paste(
                tuple(cLookup[str(i)]["rgb"].values()), (0, 0, self.fx, self.fy)
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
                    ImageDraw.Draw(glyph).text(
                        (x * self.fx, y * self.fy),
                        char,
                        (255, 255, 255),
                        font=self.font,
                    )
                    self.glyphs[char] = glyph

                # Render character
                charD = (image[y][x][2], 0, char)
                if charD in self.renderCache:
                    render = self.renderCache[charD]
                else:
                    render = self.renderCache[charD] = Image.composite(
                        self.colours[charD[0]],
                        self.colours[charD[1]],
                        self.glyphs[charD[2]],
                    )
                    if len(self.renderCache) > self.maxCache:
                        self.renderCache.pop(next(iter(self.renderCache)))

                out.paste(render, (x * self.fx, y * self.fy))
        return array(out)


class videoIO(IOBase):  # TODO: Other video filetypes
    """ASCII to video saver"""

    def __init__(self, dim: Tuple[int, int], dest: str = "out.avi"):
        """
        Set image dimensions and destination, dimensions must remain constant while recording.

        dim: Character dimensions of the ASCII video.
        dest: File destination to save to.
        """
        super().__init__()
        self.dest = VideoWriter(
            dest, VideoWriter_fourcc(*"DIVX"), 20, (dim[0] * self.fx, dim[1] * self.fy)
        )

    def write(self, image: List[List[Tuple[int, int, int]]]) -> None:
        """Write a frame to the video."""
        if self.dest is None:
            raise Exception("Attempted write to closed file")

        self.dest.write(self.convert(image))

    def close(self) -> None:
        """Close and save the video file."""
        self.dest.release()
        self.dest = None


if __name__ == "__main__":
    import random

    v = videoIO((10, 10))
    for _ in range(4000):
        f = [[(102, 2, random.randint(0, 255)) for _ in range(10)] for _ in range(10)]
        v.write(f)
    v.close()
