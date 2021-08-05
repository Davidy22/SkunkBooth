import logging
from functools import partial
from multiprocessing import Process, Queue
from time import time

from asciimatics.effects import Print
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from skunkbooth.data.defaults import LOG_FILE
from skunkbooth.utils.asciiGen import Blocks
from skunkbooth.utils.filterManager import filterManager
from skunkbooth.utils.frames import (
    FilterFrame, GalleryFrame, ImageSelectionModel, MainFrame, PreviewFrame
)
from skunkbooth.utils.videoManager import videoManager
from skunkbooth.utils.webcam import Webcam
from skunkbooth.utils.helpers import (
    global_shortcuts, toggleFlag, CamDimensions
)

# Initialize logger
logging.basicConfig(
    filename=LOG_FILE,
    filemode="w",
    level=logging.INFO,
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
)


def main() -> None:
    """Main driver function"""
    # Video saving
    vidBuf = Queue(32767)
    vid = Process(target=videoManager, args=[vidBuf])
    vid.start()

    TOP_MARGIN = 4
    image_selection = ImageSelectionModel()
    record = [True]
    toggleRecord = partial(toggleFlag, record)
    screen = Screen.open(unicode_aware=True)

    logging.info(
        "Screen initialized Height:{} Width:{}".format(screen.height-8, screen.width)
    )
    
    # last_scene = None
    filters = filterManager()
    converter = Blocks(screen.height, screen.width, uni=True, fill_background=True)
    (webcam_height, webcam_width, offset) = CamDimensions(screen.height, screen.width)

    logging.info(
        "Webcam Height:{} Webcam Width:{} Offset:{}".format(
            webcam_height, webcam_width, offset
        )
    )

    webcam = Webcam(converter, filters, webcam_height, webcam_width)

    effects = []
    camera_effect = Print(screen, webcam, y=TOP_MARGIN - 1, x=int(
        screen.width / 6) + offset, transparent=False)
    effects.append(MainFrame(screen, webcam, toggleRecord, camera_effect))

    fFrame = FilterFrame(screen, filters)
    scenes = [
        Scene(effects, -1, name="Main"),
        Scene([GalleryFrame(screen, model=image_selection)], -1, name="Gallery"),
        Scene([fFrame], -1, name="Filters"),
        Scene([PreviewFrame(screen, model=image_selection)], -1, name="Preview")
    ]
    screen.set_scenes(scenes, unhandled_input=global_shortcuts)
    b = a = 0
    frame = 1/40
    while True:
        try:
            if screen.has_resized():
                screen.close()
                screen = Screen.open(unicode_aware=True)
                effects = []
                (webcam_height, webcam_width, offset) = CamDimensions(
                    screen.height, screen.width
                )
                webcam.resize(webcam_height, webcam_width)
                converter.resize(screen.height, screen.width)
                camera_effect = Print(screen, webcam, y=TOP_MARGIN - 1, x=int(
                    screen.width / 6) + offset)
                record = [True]
                effects.append(MainFrame(screen, webcam, partial(toggleFlag, record), camera_effect))
                fNext = FilterFrame(screen, filters, data=fFrame._data)
                fFrame = fNext
                scenes = [
                    Scene(effects, -1, name="Main"),
                    Scene([GalleryFrame(screen, model=image_selection)], -1, name="Gallery"),
                    Scene([fFrame], -1, name="Filters"),
                    Scene([PreviewFrame(screen, model=image_selection)], -1, name="Preview")
                ]

                screen.set_scenes(scenes, unhandled_input=global_shortcuts)

            screen.draw_next_frame()

            if webcam.image is not None and record[0]:
                vidBuf.put(webcam.image)
            b = time()
            if b - a < frame:
                screen.wait_for_input(a - b + frame)
            else:
                screen.wait_for_input(0)
            a = b
        except ResizeScreenError:
            logging.info("Resizing screen")
            # last_scene = e.scene
        except (StopApplication, KeyboardInterrupt):
            vidBuf.put(None)
            logging.info("Stopping application")
            screen.close()
            if not vidBuf.empty():  # TODO: Make this nicer than a print statement
                logging.info("Program stopped, saving remaining video")
                print("Saving video...")
            vid.join()
            quit(0)


if __name__ == "__main__":
    main()
