import os
from datetime import datetime
from typing import Any, Callable

from asciimatics.effects import Effect, Print
from asciimatics.exceptions import NextScene, StopApplication
from asciimatics.renderers import Box, StaticRenderer
from asciimatics.widgets import (
    Button, CheckBox, FileBrowser, Frame, Label, Layout
)

from logger import CustomLogger
from webcam import Webcam

logger = CustomLogger(fileoutpath="Logs" + os.sep + "ui.log")

APP_TITLE = "Photobooth"


class MainFrame(Frame):
    """Recreatable frame to implement main ui"""

    def __init__(self, screen: Any, webcam: Webcam, toggle: Callable, camera_effect: Effect) -> None:
        """Initialize frame"""
        super(MainFrame, self).__init__(
            screen,
            3,
            screen.width-4,
            x=2,
            y=screen.height-4,
            hover_focus=True,
            can_scroll=False,
            title=APP_TITLE,
            has_border=False)
        # Made the labels below short so as to fit small screens
        self._gallery_button = Button(u"🖼 Gallery",
                                      self._gallery,
                                      add_box=True)
        self._effects_button = Button(u"🖌 Effects",
                                      self._filters,
                                      add_box=True)
        self._camera_button = Button(u"📷 Shoot", self._shoot, add_box=True)
        self._video_recording = CheckBox(text=u"⏯︎ Record", on_change=toggle)
        self._quit_button = Button(u"🛑 Quit", self._quit, add_box=True)

        box = Box(screen.width, screen.height, uni=True)
        box_effect = Print(screen, box, y=0)
        self.add_effect(box_effect)

        title_effect = Print(
            screen,
            StaticRenderer(images=[APP_TITLE]),
            y=1,
            x=int(((screen.width-4)/2)-5),
            attr=1
        )
        self.add_effect(title_effect)

        self.add_effect(camera_effect)

        controls_layout = Layout([1, 1, 1, 1, 1])
        self.add_layout(controls_layout)
        controls_layout.add_widget(self._gallery_button, 0)
        controls_layout.add_widget(self._video_recording, 1)
        controls_layout.add_widget(self._camera_button, 2)
        controls_layout.add_widget(self._effects_button, 3)
        controls_layout.add_widget(self._quit_button, 4)
        self.set_theme("bright")
        self.fix()
        self.webcam = webcam

        logger._log_info("Mainframe initialized")

    @ staticmethod
    def _filters() -> None:
        """Open effects"""
        logger._log_info("Effects was clicked")
        raise NextScene("Filters")

    @ staticmethod
    def _gallery() -> None:
        """Open gallery"""
        logger._log_info("Gallery was clicked")
        raise NextScene("Gallery")

    # @staticmethod
    def _shoot(self) -> None:
        """Take an image"""
        logger._log_info("Camera was clicked")
        img_name = f"gallery/Image-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.jpg"
        self.webcam.take_picture_and_save(img_name)
        self._screen.refresh()

    @ staticmethod
    def _quit() -> None:
        """Quit application"""
        logger._log_info("Application was stopped")
        raise StopApplication("User pressed quit")


class GalleryFrame(Frame):
    """Recreatable frame to implement gallery ui"""

    def __init__(self, screen: Any) -> None:
        """Initialize frame"""
        super(GalleryFrame, self).__init__(
            screen,
            screen.height,
            screen.width,
            y=0,
            hover_focus=True,
            has_border=True,
            can_scroll=False,
            title=APP_TITLE)
        self._back_camera_button = Button(u"👈 Back to 📷",
                                          self._switch_to_camera,
                                          add_box=True)
        self._browser = FileBrowser(screen.height // 2, "gallery/")
        title_layout = Layout([1])
        self.add_layout(title_layout)
        files_layout = Layout([100], fill_frame=True)
        self.add_layout(files_layout)
        controls_layout = Layout([1, 1, 1])
        self.add_layout(controls_layout)
        title_layout.add_widget(
            Label("Gallery", align="^", height=screen.height // 16))
        files_layout.add_widget(self._browser)
        controls_layout.add_widget(self._back_camera_button, 1)
        self.set_theme("bright")
        self.fix()

        logger._log_info("Galleryframe initialized")

    @ staticmethod
    def _switch_to_camera() -> None:
        """Switch to Camera from Gallery"""
        logger._log_info("Switched to Camera from Gallery")
        raise NextScene("Main")


class FilterFrame(Frame):
    """Recreatable frame to implement gallery ui"""

    def __init__(self, screen: Any, filters: Any, data: Any = None) -> None:
        """Initialize frame"""
        super().__init__(
            screen,
            screen.height,
            screen.width,
            hover_focus=True,
            can_scroll=True,
            title=APP_TITLE,
            data=data,
        )
        self._back_camera_button = Button("👈 Back to 📷",
                                          self._switch_to_camera,
                                          add_box=True)
        self.filters = filters
        self.filterList = [[i, None] for i in filters.filters]

        title_layout = Layout([1])
        self.add_layout(title_layout)
        title_layout.add_widget(
            Label("Filters", align="^", height=screen.height // 16))

        filters_layout = Layout([100], fill_frame=True)
        self.add_layout(filters_layout)

        for f in self.filterList:
            temp = CheckBox(f[0].name, name=f[0].name)
            f[1] = temp
            logger._log_info(f"{f[0].name} button created")
            filters_layout.add_widget(temp)

        controls_layout = Layout([1, 1, 1])
        self.add_layout(controls_layout)
        controls_layout.add_widget(self._back_camera_button, 1)

        self.set_theme("bright")
        self.fix()

        logger._log_info("Galleryframe initialized")

    def _switch_to_camera(self) -> None:
        """Switch to Camera from Filters"""
        logger._log_info("Switched to Camera from Filters")
        for i in self.filterList:
            logger._log_info(
                f"{i[0]}, {self.filters.is_loaded(i[0])}, {i[1].value}")
            if self.filters.is_loaded(i[0].name) != i[1].value:
                self.filters.toggle(i[0].name)
        self.save()
        raise NextScene("Main")
