from PIL import Image
from PIL.ImageOps import grayscale


class filter:
    """Grayscale filter."""

    def __init__(self):
        """
        Init required values.

        textOp True = operation on ASCII art, False = operation on PIL image
        name will be the name of the filter to be used for display/indexing
        """
        self.textOp = False
        self.name = "Grayscale"
        self.description = "Grayscale effect"

    def load(self) -> None:
        """Load environment variables to be used in the filter operation"""
        pass

    def unload(self) -> None:
        """Unload environment variables to be used in the filter operation"""
        pass

    def filter(self, image: Image.Image) -> Image.Image:
        """Process a PIL image and return an image of the same format and dims"""
        return grayscale(image)
