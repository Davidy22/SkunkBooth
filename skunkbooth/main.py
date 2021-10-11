import logging
from datetime import datetime
from functools import partial
from multiprocessing import Process, Queue
from time import monotonic
from typing import List, Tuple

from asciimatics.effects import Print
from asciimatics.event import Event, KeyboardEvent
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from skunkbooth.utils.asciiGen import Blocks
from skunkbooth.utils.filterManager import filterManager
from skunkbooth.utils.frame import ImageSelectionModel
from skunkbooth.utils.frames.filter_frame import FilterFrame
from skunkbooth.utils.frames.gallery_frame import GalleryFrame
from skunkbooth.utils.frames.main_frame import MainFrame
from skunkbooth.utils.frames.preview_frame import PreviewFrame
from skunkbooth.utils.frames.settings_frame import SettingsFrame
from skunkbooth.utils.settings import settings
from skunkbooth.utils.videoManager import videoManager
from skunkbooth.utils.webcam import Webcam

# Initialize logger
logging.basicConfig(
    filename=settings["LOG_FILE"],
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
)


def global_shortcuts(event: Event) -> None:
    """Event handler for global shortcuts"""
    ctrlQCode = Screen.ctrl("q")
    ctrlWCode = Screen.ctrl("w")
    if isinstance(event, KeyboardEvent):
        c = event.key_code
        # Stop on q, esc, ctrl+q and ctrl+w
        if c in (Screen.KEY_ESCAPE, ord("q"), ctrlQCode, ctrlWCode):
            raise StopApplication("User pressed quit")


def main() -> None:
    """Main driver function"""
    # Video saving
    vidBuf = Queue(32767)
    vid = Process(target=videoManager, args=[vidBuf])
    vid.start()

    def toggleFlag(flag: List[int]) -> int:
        """Temp function for toggling video recording from inside screen"""
        flag[0] = not flag[0]
        # re-initialize VideoIO for new file name
        if flag[0]:
            VID_FILE = (
                f"{settings['PIC_DIR']}/Video-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.avi"
            )
            logging.info(f"Recording new video - {VID_FILE}")
            vidBuf.put(VID_FILE)
        else:
            logging.info("Recording stopped.")
        return flag[0]

    TOP_MARGIN = 4
    image_selection = ImageSelectionModel()
    record = [True]
    toggleRecord = partial(toggleFlag, record)
    screen = Screen.open(unicode_aware=True)

    logging.info("Screen initialized Height:{} Width:{}".format(screen.height - 8, screen.width))

    # last_scene = None
    filters = filterManager()
    converter = Blocks(screen.height - 8, screen.width, uni=True, fill_background=True)

    def CamDimensions(height: int, width: int) -> Tuple[int, int, int]:
        """Calculate dimensions for vertical squeeze screen sizes"""
        if width / height >= 4:
            height -= 8
            var_dim = int(height * 4)  # Max width is around twice height in most cases
            offset = int(width / 2 - var_dim / 4 - width / 5)
            return (height, var_dim, offset)
        # Add margins of 1/6x,y if no vertical squeeze
        height = int(height * 2 / 3)
        width = int(width * 2 / 3)
        return (height, width, 2)

    (webcam_height, webcam_width, offset) = CamDimensions(screen.height, screen.width)

    logging.info(
        "Webcam Height:{} Webcam Width:{} Offset:{}".format(webcam_height, webcam_width, offset)
    )

    webcam = Webcam(converter, filters, webcam_height, webcam_width)

    effects = []
    camera_effect = Print(
        screen, webcam, y=TOP_MARGIN - 1, x=int(screen.width / 6) + offset, transparent=False
    )
    effects.append(MainFrame(screen, webcam, toggleRecord, camera_effect))

    fFrame = FilterFrame(screen, filters)
    scenes = [
        Scene(effects, -1, name="Main"),
        Scene([GalleryFrame(screen, model=image_selection)], -1, name="Gallery"),
        Scene([fFrame], -1, name="Filters"),
        Scene([SettingsFrame(screen)], -1, name="Settings"),
        Scene([PreviewFrame(screen, model=image_selection)], -1, name="Preview"),
    ]
    screen.set_scenes(scenes, unhandled_input=global_shortcuts)
    screen.lang_switch = False
    b = a = 0
    frame = 1 / 40
    while True:
        try:
            if screen.has_resized() or screen.lang_switch:
                screen.close()
                screen = Screen.open(unicode_aware=True)
                screen.lang_switch = False
                effects = []
                (webcam_height, webcam_width, offset) = CamDimensions(screen.height, screen.width)
                webcam.resize(webcam_height, webcam_width)
                converter.resize(screen.height - 8, screen.width)
                camera_effect = Print(
                    screen, webcam, y=TOP_MARGIN - 1, x=int(screen.width / 6) + offset
                )
                record = [True]
                effects.append(
                    MainFrame(screen, webcam, partial(toggleFlag, record), camera_effect)
                )
                fNext = FilterFrame(screen, filters, data=fFrame._data)
                fFrame = fNext
                scenes = [
                    Scene(effects, -1, name="Main"),
                    Scene([GalleryFrame(screen, model=image_selection)], -1, name="Gallery"),
                    Scene([fFrame], -1, name="Filters"),
                    Scene([SettingsFrame(screen)], -1, name="Settings"),
                    Scene([PreviewFrame(screen, model=image_selection)], -1, name="Preview"),
                ]

                screen.set_scenes(scenes, unhandled_input=global_shortcuts)

            screen.draw_next_frame()

            if webcam.image is not None and record[0]:
                vidBuf.put(webcam.image)
            b = monotonic()
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
