import cv2
import numpy as np


class Filter():
    """A generic superclass for filters"""

    def __init__(self, image: np.ndarray):
        """
        """
        self.image = image

    def _apply_detector(self, path: str, grayscale: bool = False,
                        reject_levels: float = 1.3, level_weights: float = 5) -> tuple:
        """Apply the given detector the the image"""
        detector = cv2.CascadeClassifier(path)
        print(detector)
        if grayscale:
            image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        print(image)
        results = detector.detectMultiScale(image, reject_levels, level_weights)

        return results


class DogEars(Filter):
    """A filter to add dog ears around the given image"""

    def __init__(self, image: np.ndarray):
        super().__init__(image)

    def apply_filter(self, mask: np.ndarray) -> np.ndarray:
        """Apply the given mask over the image at appropriate position"""
        faces = super()._apply_detector(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml', grayscale=True)
        filtered_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2BGRA)
        print(faces)
        for (x, y, w, h) in faces:
            ex = x
            ey = y-40
            ew = w+10
            eh = h-40
            mask = cv2.resize(mask, (ew, eh))
            w, h, _ = mask.shape
            for i in range(0, w):
                for j in range(0, h):
                    if mask[i, j][3] != 0:
                        filtered_image[ey + i, ex + j] = mask[i, j]

        return filtered_image
