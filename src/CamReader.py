import os
import random
import string
from threading import Thread
from time import sleep

import cv2 as cv
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

from logger import CustomLogger


class CamReader():
    """Utility class to operate camera hardware and capture"""

    def __init__(self):
        self.cap = self._open_camera()
        self.frame = None
        self.stopped = False
        self.clear_cam()

    @staticmethod
    def _open_camera() -> cv.VideoCapture:
        """Opens the camera"""
        #  0 -> camera number, if external camera is installed this number needs to be changed
        # Since a hardware can be only accessible via one user, I/O limitation
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            CustomLogger(fileoutpath="Logs" + os.sep + "ui.log")._log_error("Cannot open camera")
            return None

        sleep(3)
        return cap

    def close_camera(self) -> None:
        """Closes the camera"""
        # When everything done, release the capture
        self.stopped = True
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
            CustomLogger(
                fileoutpath="Logs" + os.sep + "ui.log"
            )._log_error("Can't receive frame (stream end?). Exiting ...")
            self.close_camera()
            exit(1)

        # flip the image
        frame = cv.flip(frame, flip)

        # rescaling image to lower dimension
        if w and h:
            frame = cv.resize(frame, [h, w])
        return frame

    def clear_cam(self) -> None:
        """Removing initial null frames from camera"""
        i = 0
        while i < 50:
            i = i + 1
            self.cap.read()

    def read_cam(self) -> None:
        """Ananlogues to capture_image but didn't want to touch it"""
        ret = True
        # while not self.stopped:
        print(self.cap)
        if not ret:
            print("sadge")
            self.close_camera()
        else:
            ret, frame = self.cap.read()
            print(ret, frame)
            self.frame = frame

    def get_image(self) -> Image:
        """:return pil image of captured in live frame"""
        print(self.frame)
        im_copy = cv.cvtColor(self.frame, cv.COLOR_BGR2RGB)
        im_pil = Image.fromarray(im_copy)
        # lock.release()
        return im_pil

    def start(self) -> None:
        """Initiate a thread to read camera"""
        self.stopped = False
        Thread(target=self.read_cam, args=()).start()
        return self

    def convert_cv2_to_pil(self, im: np.ndarray) -> Image.Image:
        """Converts numpy image to PIL image"""
        im_copy = cv.cvtColor(im, cv.COLOR_BGR2RGB)
        im_pil = Image.fromarray(im_copy)
        return im_pil

    def print_to_dom_color(self, gray: np.ndarray, no_of_colors: int) -> None:
        """Function for printing photo to the screen in ascii"""
        flat_gray = gray.reshape([gray.shape[0] * gray.shape[1], 1])

        kmeans = KMeans(n_clusters=no_of_colors)
        kmeans.fit(flat_gray)

        colors = kmeans.cluster_centers_.astype('float')
        flat_im_dom_color = colors[abs(
            np.array(flat_gray[None, :], dtype=float)
            - colors[:, None]).argmin(axis=0)]
        im_dom_color = np.array(flat_im_dom_color.reshape(
            [gray.shape[0], gray.shape[1]]), dtype='uint8')
        cv.imshow("oof", im_dom_color)

        # print(im_dom_color.shape)
        # cv.imshow(im_dom_color)

        # r = lambda: random.randint(0,255)
        # asciis = np.array(["%06x" % random.randint(0, 0xFFFFFF) for n in range(no_of_colors)])
        asciis = np.array(
            [random.choice(string.punctuation) for n in range(no_of_colors)])
        flat_im_dom_color = asciis[abs(
            np.array(flat_gray[None, :], dtype=float)
            - colors[:, None]).argmin(axis=0)]
        im_dom_color = np.array(flat_im_dom_color.reshape(
            [gray.shape[0], gray.shape[1]]), dtype='str')
        # print(im_dom_color.shape)
        # print(asciis)
        with np.printoptions(threshold=np.inf):
            print('\n'.join(''.join(str(cell) for cell in row)
                            for row in im_dom_color))
        # print("\n\n\n\n\n\n")
        # Added this for the continous effect, might have to change 0.5 to frame rate later
        sleep(0.5)


if __name__ == '__main__':
    camReader = CamReader()
    camReader.start()
    # numpyImage = camReader.capture_image(100, 100)
    #
    # camReader.print_to_dom_color(camReader.convert_gray(numpyImage), 10)
    #
    # pilImage = camReader.convert_cv2_to_pil(numpyImage)
    # pilImage.show()
    # cv.imshow('frame', numpyImage)
    # camReader.close_camera()
