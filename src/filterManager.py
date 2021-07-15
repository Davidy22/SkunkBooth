import sys
from glob import glob
from importlib import import_module
from os.path import abspath, basename, dirname, join
from typing import List, Tuple

from PIL import Image


class filterManager:
    """
    Loader and manager for all filters.

    Filters are expected to have the following attributes/methods:

    :textOp bool:   True = operation on ASCII art, False = operation on PIL image
    :name   str:    The name of the filter to be used for display/indexing

    load():         Load required data for filter operation
    unload():       Unload required data for filter operation
    filter(image):  Perform the filter operation. Input and return types are the same
    """

    def __init__(self):
        sys.path.extend(abspath("filters"))
        modules = glob(join(dirname(__file__), "filters", "*.py"))
        f = [import_module(f"filters.{basename(f)[:-3]}").filter() for f in modules]
        self.pil, self.ascii = {}, {}
        for i in f:
            (self.pil, self.ascii)[i.textOp][i.name] = i
        self.loadedPil, self.loadedAscii = {}, {}

    def load(self, name: str) -> None:
        """Load specified filter"""
        if name in self.ascii:
            self.loadedAscii[name] = self.ascii.pop(name)
            self.loadedAscii[name].load()
        elif name in self.pil:
            self.loadedPil[name] = self.pil.pop(name)
            self.loadedPil[name].load()
        else:
            print("error")

    def unload(self, name: str) -> None:
        """Unload specified filter"""
        if name in self.loadedAscii:
            self.ascii[name] = self.loadedAscii.pop(name)
            self.ascii[name].load()
        elif name in self.loadedPil:
            self.pil[name] = self.loadedPil.pop(name)
            self.pil[name].load()
        else:
            print("error")

    def ascii_filter(
        self, image: List[List[Tuple[int, int, int, int]]]
    ) -> List[List[Tuple[int, int, int, int]]]:
        """Run all loaded ASCII filters"""
        for i in self.loadedAscii:
            image = self.loadedAscii[i].filter(image)
        return image

    def pil_filter(self, image: Image.Image) -> Image.Image:
        """Run all loaded PIL filters"""
        for i in self.loadedPil:
            image = self.loadedPil[i].filter(image)
        return image
