from random import randint
from typing import List, Tuple


class filter:
    """Alphabet soup filter"""

    def __init__(self):
        """
        Init required values.

        textOp True = operation on ASCII art, False = operation on PIL image
        name will be the name of the filter to be used for display/indexing
        """
        self.textOp = True
        self.name = "Shovels"
        self.description = "Render the image with shovels"

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
        out = []
        for i in image:
            flag = True
            last = 0
            out.append(row := [])
            for j in i:
                if flag:
                    row.append(("|", j[1], j[2], 0))
                    flag = False
                else:
                    if abs(last - j[2]) > 20:
                        row.append(("D", j[1], j[2], 0))
                        flag = True
                    else:
                        row.append(("=", j[1], j[2], 0))
                last = j[2]
        return out
        return [[(chr(randint(97, 122)), j[1], j[2], 0) for j in i] for i in image]
