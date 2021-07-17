from typing import List, Tuple

from PIL import Image

from skunkbooth.data.constants import palette


class ASCIIGen:
    """Base class for image to ASCII converters"""

    def __init__(self, height: int, width: int):
        """
        Init base generator attributes

        :param height: Maximum character height.
        :param width: Maximum character width.
        """
        self.height = height
        self.width = width

    def convert(self, image: Image) -> List[List[Tuple[int, int, int, int]]]:
        """Return an ASCII image"""
        return []

    def resize(self, height: int, width: int) -> None:
        """Resize output"""
        self.height = height
        self.width = width


class Blocks(ASCIIGen):
    """Render image to ASCII art drawn with colored ▄ or # characters"""

    def __init__(
        self,
        height: int,
        width: int,
        bg: int = 0,
        fill_background: bool = False,
        uni: bool = False,
        dither: bool = False,
    ):
        """
        Init params for full block character conversion

        :param height: Maximum character height.
        :param width: Maximum character width.
        :param bg: The default background colour for this image.
        :param fill_background: Whether to set background colours too.
        :param uni: Whether to use unicode box characters or not.
        :param dither: Whether to dither the rendered image or not.
        """
        super().__init__(height, width)
        self.bg = bg
        self.fill_background = fill_background
        self.uni = uni
        self.dither = dither

        # Decide what "brush" we're going to use for the rendering.
        self.brush = "▄" if self.uni else "#"

    def _get_size(self, image: Image) -> Tuple:
        """Get size to which image should be resized."""
        if self.height << 1 <= self.width:
            return (
                image.size[0] * self.height * 2 // int(image.size[1]),
                self.height << 1 if self.uni else self.height,
            )
        else:
            return (
                self.width,
                int(image.size[1] * self.width * (1 if self.uni else 0.5)
                    // int(image.size[0])),
            )

    def convert(self, image: Image) -> List[List[Tuple[int, int, int, int]]]:
        """Return an ASCII image"""
        image = image.resize(self._get_size(image), Image.BILINEAR)
        tmp_img = Image.new("P", (1, 1))
        tmp_img.putpalette(palette)

        # Avoid dithering - this requires a little hack to get directly
        # at the underlying library in PIL.
        new_frame = image.convert("RGB")
        tmp_img.load()
        new_frame.load()
        new_frame = new_frame._new(
            new_frame.im.convert("P", 3 if self.dither else 0, tmp_img.im)
        )

        out = []
        # Convert the resulting image to coloured ASCII codes.
        for y, py in enumerate(range(0, new_frame.size[1], 2 if self.uni else 1)):
            out.append(row := [])
            for px in range(0, new_frame.size[0]):
                col = new_frame.getpixel((px, py))
                try:
                    col2 = new_frame.getpixel((px, py + 1)) if self.uni else col
                except IndexError:
                    col2 = col
                if col == col2 in [0, 16]:
                    if self.fill_background or self.uni:
                        cell = (".", 2, self.bg, self.bg)
                    else:
                        row.append((self.bg,))
                        continue
                else:
                    if self.fill_background or self.uni:
                        cell = (self.brush, 2, col2, col)
                    else:
                        cell = ("#", 2, col, self.bg)
                row.append(cell)
        return out
