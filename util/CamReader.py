import random
import string
from PIL import Image
import matplotlib.pyplot as plt
from os import system
from time import sleep
import cv2 as cv
import numpy as np
from sklearn.cluster import KMeans


def _open_camera():
    """

    :return: camera IO object
    """
    #  0 -> camera number, if external camera is installed this number needs to be changed
    # Since a hardware can be only accessible via one user, I/O limitation

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
    return cap


def _close_camera(cap):
    """
    :return: void : close the camera IO
    """
    # When everything done, release the capture
    cap.release()


def _capture_image(cap, w=120, h=140):
    """
    :return: the PIL image of live camera feed
    """
    # while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")

    # rescaling image to lower dimension

    frame = cv.resize(frame, [w, h])
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    # frame is the coloured image
    #  gray is the grayscaled version
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)\
    return frame
    # return np.array(frame, dtype=np.uint8)
    # @dha do the operation of converting a np object to asciimate object here
    # _print_to_dom_color(gray, 7)


def _convert_cv2_to_pil(im):
    """

    :param im: image as a numpy/cv2 array
    :return: image in PIL format
    """
    im_copy = cv.cvtColor(im, cv.COLOR_BGR2RGB)
    im_pil = Image.fromarray(im_copy)
    return im_pil


def _print_to_dom_color(gray: np.ndarray, no_of_colors: int) -> None:
    """Function for printing photo to the screen in ascii

    :param gray: gray scale image, size doesn't matter
    :param no_of_colors: number of colours you want to reduce your image to
    :return:
    """
    flat_gray = gray.reshape([gray.shape[0] * gray.shape[1], 1])

    kmeans = KMeans(n_clusters=no_of_colors)
    kmeans.fit(flat_gray)

    colors = kmeans.cluster_centers_.astype('float')
    flat_im_dom_color = colors[abs(np.array(flat_gray[None, :], dtype=float) - colors[:, None]).argmin(axis=0)]
    im_dom_color = np.array(flat_im_dom_color.reshape(
        [gray.shape[0], gray.shape[1]]), dtype='uint8')
    np.where(im_dom_color)
    # print(im_dom_color.shape)
    # cv.imshow(im_dom_color)

    # r = lambda: random.randint(0,255)
    # asciis = np.array(["%06x" % random.randint(0, 0xFFFFFF) for n in range(no_of_colors)])
    asciis = np.array(
        [random.choice(string.punctuation) for n in range(no_of_colors)])
    flat_im_dom_color = asciis[abs(np.array(flat_gray[None, :], dtype=float) - colors[:, None]).argmin(axis=0)]
    im_dom_color = np.array(flat_im_dom_color.reshape(
        [gray.shape[0], gray.shape[1]]), dtype='str')
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
    camera = _open_camera()
    # sleep for few seconds, since the cam is just opened so the
    # light won't have been properly caputured displaying dark images
    sleep(2)
    numpyImage = _capture_image(camera, 500, 500)

    pilImage = _convert_cv2_to_pil(numpyImage)
    # pilImage.show()
    # plt.plot()
    # cv.imshow('frame', numpyImage)
    plt.imshow(pilImage)
    plt.show()
    _close_camera(camera)
    cv.destroyAllWindows()
