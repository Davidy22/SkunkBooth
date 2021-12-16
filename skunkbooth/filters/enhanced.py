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
        self.name = "Enhanced"
        self.description = "Enhances the images (sharper/mored defined)"

    def load(self) -> None:
        """Load environment variables to be used in the filter operation"""
        pass

    def unload(self) -> None:
        """Unload environment variables to be used in the filter operation"""
        pass

    def filter(self, image: Image.Image) -> Image.Image:
        """Process a PIL image and return an image of the same format and dims"""
        #Define the object edges better
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        #improve sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(4.0)
        #Increase brightness to show more features
        enhancer_brightness = ImageEnhance.Brightness(image)
        image = enhancer_brightness.enhance(2.0)
        return image
