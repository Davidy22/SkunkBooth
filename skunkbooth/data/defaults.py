from pathlib import Path

SKUNKBOOTH_DIR = (Path.home() / "skunkbooth").absolute()

_settings = {
    "LOG_FILE": f"{SKUNKBOOTH_DIR}/.logs/skunkbooth.log",
    "SETTINGS_FILE": f"{SKUNKBOOTH_DIR}/.settings/settings.conf",
    "PIC_DIR": f"{SKUNKBOOTH_DIR}/pictures",
    "IMG_FORMAT": "JPG",
    "LANGUAGE": "en",
    "DEVICE": str(0)
}


for i in ["LOG_FILE", "PIC_DIR", "SETTINGS_FILE"]:
    path = Path(_settings[i])
    if i[-3:] != "DIR":
        path = path.parent
    path.mkdir(parents=True, exist_ok=True)
