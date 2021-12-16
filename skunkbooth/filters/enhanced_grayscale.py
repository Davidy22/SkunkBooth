from PIL import Image, ImageFilter, ImageEnhance


class filter:
    """Outlines user and surroundings."""

    def __init__(self):
        """
        Init required values.

        textOp True = operation on ASCII art, False = operation on PIL image
        name will be the name of the filter to be used for display/indexing
        """
        self.textOp = False
        self.name = "Enhanced_Grayscale"
        self.description = "Enhances an image in grayscale"

    def load(self) -> None:
        """Load environment variables to be used in the filter operation"""
        pass

    def unload(self) -> None:
        """Unload environment variables to be used in the filter operation"""
        pass

    def filter(self, image: Image.Image) -> Image.Image:
        """Process a PIL image and return an image of the same format and dims"""
        image = image.convert("L") #Convert to grayscale
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE) #enhance the edges
        image = image.filter(ImageFilter.FIND_EDGES) #outline the edges more clearly
        enhancer = ImageEnhance.Sharpness(image) #increase sharpness
        image = enhancer.enhance(2.0)
        return image
