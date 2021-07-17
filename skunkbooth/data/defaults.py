from os import makedirs, path
from pathlib import Path

LOG_FILE = f"{Path.home()}/skunkbooth/.logs/skunkbooth.log"
PIC_DIR = f"{Path.home()}/skunkbooth/pictures"

try:
    makedirs(path.dirname(path.abspath(LOG_FILE)))
    makedirs(path.abspath(PIC_DIR))
except FileExistsError:
    pass
