import random
import string
from os import system
from time import sleep

import cv2 as cv
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


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
            print("Cannot open camera")
            return None

        sleep(1)
        return cap

    def _close_camera(self) -> None:
        """Closes the camera"""
        # When everything done, release the capture
        self.cap.release()
        cv.destroyAllWindows()

    def _convert_gray(self, im: np.ndarray) -> np.ndarray:
        """Coverts image to grayscale"""
        return cv.cvtColor(im, cv.COLOR_BGR2GRAY)

    def _capture_image(self, w: int, h: int) -> np.ndarray:
        """If camera is opened then reads the live camera buffer"""
        ret, frame = self.cap.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
        # rescaling image to lower dimension
        frame = cv.resize(frame, [w, h])
        # Display the resulting frame
        # frame is the coloured image
        #  gray is the grayscaled version
        # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return frame

    def _convert_cv2_to_pil(self, im: np.ndarray) -> Image.Image:
        """Converts numpy image to PIL image"""
        im_copy = cv.cvtColor(im, cv.COLOR_BGR2RGB)
        im_pil = Image.fromarray(im_copy)
        return im_pil

    def _print_to_dom_color(self, gray: np.ndarray, no_of_colors: int) -> None:
        """Function for printing photo to the screen in ascii"""
        flat_gray = gray.reshape([gray.shape[0] * gray.shape[1], 1])

        kmeans = KMeans(n_clusters=no_of_colors)
        kmeans.fit(flat_gray)

        colors = kmeans.cluster_centers_.astype('float')
        flat_im_dom_color = colors[abs(
            np.array(flat_gray[None, :], dtype=float) - colors[:, None]).argmin(axis=0)]
        im_dom_color = np.array(flat_im_dom_color.reshape(
            [gray.shape[0], gray.shape[1]]),
            dtype='uint8')
        cv.imshow("oof", im_dom_color)

        # print(im_dom_color.shape)
        # cv.imshow(im_dom_color)

        # r = lambda: random.randint(0,255)
        # asciis = np.array(["%06x" % random.randint(0, 0xFFFFFF) for n in range(no_of_colors)])
        asciis = np.array(
            [random.choice(string.punctuation) for n in range(no_of_colors)])
        flat_im_dom_color = asciis[abs(
            np.array(flat_gray[None, :], dtype=float) - colors[:, None]).argmin(axis=0)]
        im_dom_color = np.array(flat_im_dom_color.reshape(
            [gray.shape[0], gray.shape[1]]),
            dtype='str')
        # print(im_dom_color.shape)
        # print(asciis)
        with np.printoptions(threshold=np.inf):
            print('\n'.join(''.join(str(cell) for cell in row)
                            for row in im_dom_color))
        # print("\n\n\n\n\n\n")
        # Added this for the continous effect, might have to change 0.5 to frame rate later
        sleep(0.5)  # noqa: S605
        system("clear")


if __name__ == '__main__':
    camReader = CamReader()
    numpyImage = camReader._capture_image(100, 100)

    camReader._print_to_dom_color(camReader._convert_gray(numpyImage), 10)

    pilImage = camReader._convert_cv2_to_pil(numpyImage)
    pilImage.show()
    # cv.imshow('frame', numpyImage)
    camReader._close_camera()
