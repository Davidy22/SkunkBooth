from PIL import Image
from PIL.ImageOps import colorize, grayscale


class filter:
    """Warm filter."""

    def __init__(self):
        """
        Init required values.

        textOp True = operation on ASCII art, False = operation on PIL image
        name will be the name of the filter to be used for display/indexing
        """
        self.textOp = False
        self.name = "Warm"
        self.description = "Warm filter effect"

    def load(self) -> None:
        """Load environment variables to be used in the filter operation"""
        pass

    def unload(self) -> None:
        """Unload environment variables to be used in the filter operation"""
        pass

    def filter(self, image: Image.Image) -> Image.Image:
        """Process a PIL image and return an image of the same format and dims"""
        return colorize(grayscale(image), black=(0, 0, 0), white=(255, 205, 116))
