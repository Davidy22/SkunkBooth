import logging
import threading
import time
from datetime import datetime
from functools import partial
from typing import Any, Callable

from asciimatics.effects import Effect, Print
from asciimatics.exceptions import NextScene, StopApplication
from asciimatics.renderers import Box, StaticRenderer
from asciimatics.widgets import Button, CheckBox, Frame, Label, Layout

from skunkbooth.utils.frame import APP_TITLE, _
from skunkbooth.utils.settings import settings
from skunkbooth.utils.webcam import Webcam


class MainFrame(Frame):
    """Recreatable frame to implement main ui"""

    def __init__(
        self, screen: Any, webcam: Webcam, toggle: Callable, camera_effect: Effect
    ) -> None:
        """Initialize frame"""
        super(MainFrame, self).__init__(
            screen,
            3,
            screen.width - 4,
            x=2,
            y=screen.height - 4,
            hover_focus=True,
            can_scroll=False,
            title=APP_TITLE,
            has_border=False,
            reduce_cpu=True,
        )
        # Made the labels below short so as to fit small screens
        self._gallery_button = Button(_("🖼 Gallery"), self._gallery, add_box=True)
        self._effects_button = Button(_("🖌 Effects"), self._filters, add_box=True)
        self._camera_button = Button(_("📷 Shoot"), self._shoot, add_box=True)
        self._settings_button = Button(_("🔧 Settings"), self._settings, add_box=True)
        self._video_recording = CheckBox(_("⏯︎ Record"), on_change=partial(self._record, toggle))
        self._video_length = Label("00:00")
        self._quit_button = Button(_("🛑 Quit"), self._quit, add_box=True)

        self._timer_event = threading.Event()
        box = Box(screen.width, screen.height, uni=True)
        box_effect = Print(screen, box, y=0)
        self.add_effect(box_effect)

        title_effect = Print(
            screen,
            StaticRenderer(images=[" " + APP_TITLE + " "]),
            y=0,
            transparent=False,
            x=int(((screen.width - 4) / 2) - 5),
            attr=1,
        )
        self.add_effect(title_effect)

        self.add_effect(camera_effect)

        controls_layout = Layout([1, 1, 1, 1, 1, 1, 1])
        self.add_layout(controls_layout)
        controls_layout.add_widget(self._gallery_button, 0)
        controls_layout.add_widget(self._video_recording, 1)
        controls_layout.add_widget(self._video_length, 2)
        controls_layout.add_widget(self._camera_button, 3)
        controls_layout.add_widget(self._effects_button, 4)
        controls_layout.add_widget(self._settings_button, 5)
        controls_layout.add_widget(self._quit_button, 6)
        self.set_theme("bright")
        self.fix()
        self.webcam = webcam

        logging.debug("Mainframe initialized")

    @staticmethod
    def _filters() -> None:
        """Open effects"""
        logging.debug("Effects was clicked")
        raise NextScene("Filters")

    @staticmethod
    def _gallery() -> None:
        """Open gallery"""
        logging.debug("Gallery was clicked")
        raise NextScene("Gallery")

    def _update_time(self, event: threading.Event) -> None:
        start = 0
        length_format = '{min}:{sec}'
        while not event.isSet():
            start += 1
            sec = start % 60
            minutes = start // 60
            self._video_length.text = length_format.format(min=minutes, sec=sec)
            time.sleep(1)

    def _record(self, toggle: Callable) -> None:
        """Record video"""
        logging.debug("Started recording video")
        res = toggle()
        if res:
            self._timer_event.clear()
            threading.Thread(target=self._update_time, args=(self._timer_event,)).start()
        else:
            self._timer_event.set()
            self._video_length.text = "00:00"

    def _shoot(self) -> None:
        """Take an image"""
        logging.debug("Camera was clicked")
        if settings["IMG_FORMAT"] == "ASCII":
            ext = ".txt"
        else:
            ext = f".{settings['IMG_FORMAT']}"
        img_name = (
            f"{settings['PIC_DIR']}/Image-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}{ext}"
        )
        logging.info(f"Saving image {img_name}")
        self.webcam.take_picture_and_save(img_name)
        self._screen.refresh()

    def _settings(self) -> None:
        """Go to settings page"""
        logging.debug("Settings was clicked")
        raise NextScene("Settings")

    @staticmethod
    def _quit() -> None:
        """Quit application"""
        logging.debug("Application was stopped")
        raise StopApplication("User pressed quit")
