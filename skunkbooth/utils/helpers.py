import logging
from datetime import datetime
from multiprocessing.queues import Queue
from typing import List, Tuple

from asciimatics.screen import Screen
from asciimatics.event import Event, KeyboardEvent
from asciimatics.exceptions import StopApplication

from skunkbooth.data.defaults import LOG_FILE, PIC_DIR

def global_shortcuts(event: Event) -> None:
    """Event handler for global shortcuts"""
    ctrlQCode = Screen.ctrl('q')
    ctrlWCode = Screen.ctrl('w')
    if isinstance(event, KeyboardEvent):
        c = event.key_code
        # Stop on q, esc, ctrl+q and ctrl+w
        if c in (Screen.KEY_ESCAPE, ord('q'), ctrlQCode, ctrlWCode):
            raise StopApplication("User pressed quit")


def toggleFlag(flag: List[int]) -> None:
    """Temp function for toggling video recording from inside screen"""
    vidBuf = Queue(32767)
    flag[0] = not flag[0]
    # re-initialize VideoIO for new file name
    if flag[0]:
        VID_FILE = f"{PIC_DIR}/Video-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.avi"
        logging.info(f"Recording new video - {VID_FILE}")
        vidBuf.put(VID_FILE)
    else:
        logging.info("Recording stopped.")


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
    
    
