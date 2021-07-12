from json import load
from typing import List, Tuple

from cv2 import VideoWriter, VideoWriter_fourcc
from numpy import array
from PIL import Image, ImageDraw, ImageFont


class IOObj:
    """ASCII conversion module, subclass for access to convert()"""

    def __init__(self):
        self.colours = load(open("dat/colours.json"))
        self.font = ImageFont.truetype("dat/Input.ttf", 30)  # TODO: Font config
        self.fx, self.fy = self.font.getsize(" ")
        self.lookup = {}
        self.charBack = Image.new("RGB", (self.fx, self.fy))

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
                if char not in self.lookup:
                    # Cache character glyphs
                    glyph = Image.new("RGBA", (self.fx, self.fy))
                    ImageDraw.Draw(glyph).text(
                        (x * self.fx, y * self.fy),
                        char,
                        (255, 255, 255),
                        font=self.font,
                    )
                    glyph = array(glyph)
                    r, g, b, _ = glyph.T
                    self.lookup[char] = (
                        glyph,
                        ((r == 255) & (g == 255) & (b == 255)).T,
                    )

                # Recolor character
                char = self.lookup[char]
                char[0][..., :-1][char[1]] = tuple(
                    self.colours[str(image[y][x][2])]["rgb"].values()
                )
                char = Image.fromarray(char[0])

                # Render character
                out.paste(
                    Image.composite(char, self.charBack, char),
                    (x * self.fx, y * self.fy),
                )
        return array(out)


class videoIO(IOObj):  # TODO: Other video filetypes
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
    for _ in range(400):
        f = [[(102, 2, random.randint(0, 255)) for _ in range(10)] for _ in range(10)]
        v.write(f)
    v.close()
