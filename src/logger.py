import logging
import os


class CustomLogger:
    """A class for helping in logging"""

    def __init__(self, fileoutpath: str) -> None:
        self.fileoutpath = fileoutpath

        try:
            os.mkdir(
                os.path.dirname(os.path.abspath(__file__)) + os.sep + "Logs")
        except FileExistsError:
            pass
        """Initializing logging module"""
        logging.basicConfig(
            filename=self.fileoutpath,
            filemode="w",
            level=logging.DEBUG,
            format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
        )
