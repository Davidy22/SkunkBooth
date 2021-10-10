from gettext import translation

from skunkbooth.utils.settings import settings

temp = translation("base", localedir="locales", languages=[settings["LANGUAGE"]])
temp.install()
_ = temp.gettext
APP_TITLE = _("Skunkbooth")


class ImageSelectionModel(object):
    """Model to hold selected image path"""

    def __init__(self, path: str = "") -> None:
        """Initialize model"""
        self._path = path

    def set_path(self, path: str) -> None:
        """Setter"""
        self._path = path

    def get_path(self) -> str:
        """Getter"""
        return self._path
