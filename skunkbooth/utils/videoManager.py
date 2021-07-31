import logging

from .fileIO import VideoIO


class videoManager:
    """Wrapper for video IO multiprocessing"""

    def __init__(self, queue: object, dest: str = "gallery/out.avi"):
        self.vid = VideoIO()
        while True:
            val = queue.get()
            if isinstance(val, str):
                self.vid.close()
                self.vid = VideoIO(dest=val)
            elif val is None:
                self.vid.close()
                return
            else:
                logging.info(str(val))
                self.vid.write(val)
