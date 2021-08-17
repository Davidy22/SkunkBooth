from os import path
from pathlib import Path

_settings = {
    "LOG_FILE": f"{Path.home()}/skunkbooth/.logs/skunkbooth.log",
    "SETTINGS_FILE": f"{Path.home()}/skunkbooth/.settings/settings.conf",
    "PIC_DIR": f"{Path.home()}/skunkbooth/pictures",
    "IMG_FORMAT": "JPG"
}


for i in ["LOG_FILE", "PIC_DIR", "SETTINGS_FILE"]:
    if i[-3:] == "DIR":
        Path.mkdir(Path(path.abspath(_settings[i])), exist_ok=True)
    else:
        Path.mkdir(Path(path.dirname(path.abspath(_settings[i]))), exist_ok=True)
