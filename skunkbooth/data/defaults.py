import logging
from os import makedirs, path
from pathlib import Path

LOG_FILE = f"{Path.home()}/skunkbooth/.logs/skunkbooth.log"
PIC_DIR = f"{Path.home()}/skunkbooth/pictures"

try:
    logging.info(f"Creating {LOG_FILE}")
    makedirs(path.dirname(path.abspath(LOG_FILE)))
    logging.info(f"Creating {PIC_DIR}")
    makedirs(path.abspath(PIC_DIR))
except FileExistsError:
    logging.info("Paths are alreay present.")
