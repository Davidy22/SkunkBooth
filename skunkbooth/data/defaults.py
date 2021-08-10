from os import makedirs, path
from pathlib import Path

_settings = {
    "LOG_FILE": f"{Path.home()}/skunkbooth/.logs/skunkbooth.log",
    "PIC_DIR": f"{Path.home()}/skunkbooth/pictures",
    "SETTINGS_FILE": f"{Path.home()}/skunkbooth/.settings/settings.conf",
    "IMG_FORMAT": "JPG"
}


for i in ["LOG_FILE", "PIC_DIR", "SETTINGS_FILE"]:
    try:
        if i[-3:] == "DIR":
            makedirs(path.abspath(_settings[i]))
        else:
            makedirs(path.dirname(path.abspath(_settings[i])))
    except FileExistsError:
        pass
