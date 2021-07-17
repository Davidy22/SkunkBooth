import logging
from datetime import datetime
from functools import partial
from time import time
from typing import List, Tuple

from asciimatics.effects import Print
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from skunkbooth.data.defaults import LOG_FILE, PIC_DIR
from skunkbooth.utils.asciiGen import Blocks
from skunkbooth.utils.fileIO import VideoIO
from skunkbooth.utils.filterManager import filterManager
from skunkbooth.utils.frames import (
    FilterFrame, GalleryFrame, ImageSelectionModel, MainFrame, PreviewFrame
)
from skunkbooth.utils.webcam import Webcam

# Initialize logger
logging.basicConfig(
    filename=LOG_FILE,
    filemode="w",
    level=logging.INFO,
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
)
vid = VideoIO()


def main() -> None:
    """Main driver function"""
    def toggleFlag(flag: List[int]) -> None:
        """Temp function for toggling video recording from inside screen"""
        flag[0] = not flag[0]
        # re-initialize VideoIO for new file name
        if flag[0]:
            global vid
            vid.close()
            VID_FILE = f"{PIC_DIR}/Video-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.avi"
            logging.info(f"Recording new video - {VID_FILE}")
            vid = VideoIO(dest=VID_FILE)
        else:
            logging.info("Recording stopped.")

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

    def CamDimensions(height: int, width: int) -> Tuple[int, int, int]:
        """Calculate dimensions for vertical squeeze screen sizes"""
        if width / height >= 4:
            height -= 8
            var_dim = int(height * 4)  # Max width is around twice height in most cases
            offset = int(width / 2 - var_dim / 2.5 - width / 5)
            return (height, var_dim, offset)
        # Add margins of 1/6x,y if no vertical squeeze
        height = int(height * 2 / 3)
        width = int(width * 2 / 3)
        return (height, width, 2)

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
    screen.set_scenes(scenes)
    b = a = 0
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

                screen.set_scenes(scenes)

            screen.draw_next_frame()

            if webcam.image is not None and record[0]:
                vid.write(webcam.image)
            b = time()
            if b - a < 0.05:
                pause = max(0, min(0.001, a + 0.001 - b))
                screen.wait_for_input(pause)
            else:
                screen.wait_for_input(0)
            a = b
        except ResizeScreenError:
            logging.info("Resizing screen")
            # last_scene = e.scene
        except (StopApplication, KeyboardInterrupt):
            logging.info("Stopping application")
            screen.close()
            quit(0)


if __name__ == "__main__":
    main()
