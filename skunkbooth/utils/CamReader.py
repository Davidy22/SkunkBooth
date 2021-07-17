import logging
from time import sleep

import cv2 as cv
import numpy as np
from PIL import Image


class CamReader():
    """Utility class to operate camera hardware and capture"""

    def __init__(self):
        self.cap = self._open_camera()

    @staticmethod
    def _open_camera() -> cv.VideoCapture:
        """Opens the camera"""
        #  0 -> camera number, if external camera is installed this number needs to be changed
        # Since a hardware can be only accessible via one user, I/O limitation
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            logging.error("Cannot open camera")
            return None

        sleep(1)
        return cap

    def close_camera(self) -> None:
        """Closes the camera"""
        # When everything done, release the capture
        self.cap.release()

    def convert_gray(self, im: np.ndarray) -> np.ndarray:
        """Coverts image to grayscale"""
        return cv.cvtColor(im, cv.COLOR_BGR2GRAY)

    def capture_image(self,
                      flip: int = 1,
                      w: int = 0,
                      h: int = 0) -> np.ndarray:
        """If camera is opened then reads the live camera buffer"""
        ret, frame = self.cap.read()

        # if frame is read correctly ret is True
        if not ret:
            logging.error("Can't receive frame (stream end?). Exiting ...")
            self.close_camera()
            exit(1)

        # flip the image
        frame = cv.flip(frame, flip)

        # rescaling image to lower dimension
        if w and h:
            frame = cv.resize(frame, [h, w])
        return frame

    def convert_cv2_to_pil(self, im: np.ndarray) -> Image.Image:
        """Converts numpy image to PIL image"""
        im_copy = cv.cvtColor(im, cv.COLOR_BGR2RGB)
        im_pil = Image.fromarray(im_copy)
        return im_pil
