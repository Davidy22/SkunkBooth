import random
import string
from os import system
from time import sleep

import cv2 as cv
import numpy as np
from sklearn.cluster import KMeans

#  0 -> camera number, if external camera is installed this number needs to be changed
cap = cv.VideoCapture(0)

# Since a hardware can be only accessible via one user, I/O limitation
if not cap.isOpened():
    print("Cannot open camera")
    exit()


def _capture_image_as_ascii() -> None:
    """:return: reads the camera"""
    count = 0
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # rescaling image to lower dimension

        h = 140
        w = 120

        frame = cv.resize(frame, [w, h])
        count = count + 1
        # Display the resulting frame
        # frame is the coloured image
        #  gray is the grayscaled version
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # @dha do the operation of converting a np object to asciimate object here
        _print_to_dom_color(gray, 7)

        # unless pressed: q don;t exit
        #  we can set the how do we want to exit this loop, currently
        # exiting after just 10 frames

        if cv.waitKey(1) == ord('q') or count > 10:
            break


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


# When everything done, release the capture
if __name__ == '__main__':
    _capture_image_as_ascii()
    cap.release()
    cv.destroyAllWindows()
