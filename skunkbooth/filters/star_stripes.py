from random import randint
from typing import List, Tuple


class filter:
    """Sample filter for ASCII operations"""

    def __init__(self):
        """
        Init required values.

        textOp True = operation on ASCII art, False = operation on PIL image
        name will be the name of the filter to be used for display/indexing
        """
        self.textOp = True
        self.name = "Star-Stripes"
        self.description = "Intersperse some stars* across the image"

    def load(self) -> None:
        """Load environment variables to be used in the filter operation"""
        pass

    def unload(self) -> None:
        """Unload environment variables to be used in the filter operation"""
        pass

    def filter(
        self, image: List[List[Tuple[int, int, int, int]]]
    ) -> List[List[Tuple[int, int, int, int]]]:
        """Process an ASCII image and return an image of the same format and dims"""
        return [
            [("■" if randint(0, 50) else "*", j[1], j[2], 0) for j in i] for i in image
        ]
