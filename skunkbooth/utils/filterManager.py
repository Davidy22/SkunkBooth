import logging
import sys
from importlib import import_module
from pathlib import Path
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
        filters_path = Path(__file__).absolute().parents[1] / "filters"
        sys.path.extend(f"{filters_path}")
        modules = filters_path.glob("*.py")
        f = [
            import_module(f"skunkbooth.filters.{f.name[:-3]}").filter()
            for f in modules if "__init__.py" not in f.name
        ]
        self.pil, self.ascii = {}, {}
        for i in f:
            (self.pil, self.ascii)[i.textOp][i.name] = i
        self.loadedPil, self.loadedAscii = {}, {}

    @property
    def loaded(self) -> List:
        """Get loaded filters"""
        return list(self.loadedPil.values()) + list(self.loadedAscii.values())

    @property
    def unloaded(self) -> List:
        """Get unloaded filters"""
        return list(self.pil.values()) + list(self.ascii.values())

    @property
    def filters(self) -> List:
        """Get all filters"""
        return self.loaded + self.unloaded

    def is_loaded(self, filterID: str) -> bool:
        """Check if filter is loaded"""
        return filterID in self.loadedPil or filterID in self.loadedAscii

    def toggle(self, name: str) -> None:
        """Toggle specified filter"""
        if name in self.ascii or name in self.pil:
            self.load(name)
        elif name in self.loadedAscii or name in self.loadedPil:
            self.unload(name)

    def load(self, name: str) -> None:
        """Load specified filter"""
        if name in self.ascii:
            self.loadedAscii[name] = self.ascii.pop(name)
            self.loadedAscii[name].load()
        elif name in self.pil:
            self.loadedPil[name] = self.pil.pop(name)
            self.loadedPil[name].load()
        else:
            logging.error(f"Error loading filter {name}")

    def unload(self, name: str) -> None:
        """Unload specified filter"""
        if name in self.loadedAscii:
            self.ascii[name] = self.loadedAscii.pop(name)
            self.ascii[name].load()
        elif name in self.loadedPil:
            self.pil[name] = self.loadedPil.pop(name)
            self.pil[name].load()
        else:
            logging.error(f"Error unloading filter {name}")

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
