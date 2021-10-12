import logging
from gettext import translation
from typing import Any

import cv2 as cv
from asciimatics.event import Event, KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Frame, Label, Layout

from skunkbooth.utils.CamReader import CamReader
from skunkbooth.utils.dropdownlist import DropdownList
from skunkbooth.utils.frame import APP_TITLE
from skunkbooth.utils.settings import settings
from skunkbooth.utils.webcam import Webcam

MAX_DEVICES = 10


class SettingsFrame(Frame):
    """Recreatable frame to implement settings ui"""

    def __init__(self, screen: Any, webcam: Webcam) -> None:
        """Initialize frame"""
        super().__init__(
            screen,
            screen.height,
            screen.width,
            hover_focus=True,
            can_scroll=True,
            title=APP_TITLE,
        )
        self._webcam = webcam
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

        def _list_device_ids() -> [int]:
            """Returns a list of device IDs."""
            is_working = True
            dev_port = 0
            working_ports = []
            while is_working and dev_port < MAX_DEVICES:
                camera = cv.VideoCapture(dev_port)
                if camera.isOpened():
                    is_working = camera.read()[0]

                    if is_working:
                        working_ports.append(dev_port)
                dev_port += 1
            return working_ports

        def _make_device_dropdown_list(device_ids: list[int]) -> list(tuple(str, str)):
            return list((str(id), str(id)) for id in device_ids)

        def _update_device() -> None:
            settings.update({"DEVICE": device.value})
            webcam.camera = CamReader(int(device.value))
            screen.device_switch = True

        device_ids = _list_device_ids()
        device = DropdownList(_make_device_dropdown_list(device_ids), _("Device"))
        device.value = settings["DEVICE"]
        device._on_change = _update_device

        settings_layout.add_widget(device)

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
