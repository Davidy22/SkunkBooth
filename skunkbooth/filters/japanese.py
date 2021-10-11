from random import randint
from typing import List, Tuple


class filter:
    """Japanese-letter soup filter"""

    def __init__(self):
        """
        Init required values.

        textOp True = operation on ASCII art, False = operation on PIL image
        name will be the name of the filter to be used for display/indexing
        """
        self.textOp = True
        self.name = "Japanese"
        self.description = "Fill the image with random japanese letters"

    def load(self) -> None:
        """Load environment variables to be used in the filter operation"""
        pass

    def unload(self) -> None:
        """Unload environment variables to be used in the filter operation"""
        pass

    def filter(
            self, image: List[List[Tuple[int, int, int, int]]]) -> List[List[Tuple[int, int, int, int]]]:
        """Process an ASCII image and return an image of the same format and dims"""
        symbols = ['あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ', 'さ', 'し', 'す', 'せ', 'そ', 'た', 'ち', 'つ', 'て', 'と',
                   'な', 'に', 'ぬ', 'ね', 'の', 'は', 'ひ', 'ふ', 'へ', 'ほ', 'ま', 'み', 'む', 'め', 'も', 'や', 'ゆ', 'よ', 'ら', 'り',
                   'る', 'れ', 'ろ', 'わ', 'を']
        return [[(symbols[randint(0, len(symbols))], j[1], j[2], 0) for j in i] for i in image]
