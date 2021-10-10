import logging
from gettext import translation
from typing import Any

from asciimatics.event import Event, KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Frame, Label, Layout

from skunkbooth.utils.dropdownlist import DropdownList
from skunkbooth.utils.frame import APP_TITLE
from skunkbooth.utils.settings import settings


class SettingsFrame(Frame):
    """Recreatable frame to implement settings ui"""

    def __init__(self, screen: Any) -> None:
        """Initialize frame"""
        super().__init__(
            screen,
            screen.height,
            screen.width,
            hover_focus=True,
            can_scroll=True,
            title=APP_TITLE,
        )
        self._back_camera_button = Button(_("👈 Back to 📷"), self._switch_to_camera, add_box=True)

        title_layout = Layout([1])
        self.add_layout(title_layout)
        title_layout.add_widget(Label(_("Settings"), align="^", height=screen.height // 16))

        settings_layout = Layout([100], fill_frame=True)
        self.add_layout(settings_layout)

        imageFormat = DropdownList(
            [("JPG", "JPG"), ("PNG", "PNG"), ("ASCII", "ASCII")], _("Image output format")
        )
        imageFormat.value = settings["IMG_FORMAT"]
        imageFormat._on_change = lambda: settings.update({"IMG_FORMAT": imageFormat.value})
        settings_layout.add_widget(imageFormat)

        language = DropdownList([("English", "en"), ("Esperanto", "eo")], _("Language"))
        language.value = settings["LANGUAGE"]

        def _switchLanguage() -> None:
            settings.update({"LANGUAGE": language.value})
            temp = translation("base", localedir="locales", languages=[language.value])
            temp.install()
            global _
            _ = temp.gettext
            screen.lang_switch = True

        language._on_change = _switchLanguage
        settings_layout.add_widget(language)

        controls_layout = Layout([1, 1, 1])
        self.add_layout(controls_layout)
        controls_layout.add_widget(self._back_camera_button, 1)

        self.set_theme("bright")
        self.fix()

        logging.debug("Settingsframe initialized")

    def _switch_to_camera(self) -> None:
        """Switch to Camera from settings"""
        logging.debug("Switched to Camera from settings")
        raise NextScene("Main")

    def process_event(self, event: Event) -> None:
        """Deals with keyboard events that happen in this screen"""
        super(SettingsFrame, self).process_event(event)
        if isinstance(event, KeyboardEvent):
            c = event.key_code
            layout = self._layouts[1]
            if c == Screen.KEY_HOME:
                self.switch_focus(layout, 0, 0)
            elif c == Screen.KEY_END:
                self.switch_focus(layout, 0, len(self.settingsList) - 1)
            elif c == Screen.KEY_PAGE_UP:
                pass
            elif c == Screen.KEY_PAGE_DOWN:
                pass
