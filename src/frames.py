import os
import sys
from typing import Any

from asciimatics.exceptions import (
    NextScene, ResizeScreenError, StopApplication
)
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, FileBrowser, Frame, Label, Layout

from logger import CustomLogger
from webcam import Webcam

logger = CustomLogger(fileoutpath="Logs" + os.sep + "ui.log")


class MainFrame(Frame):
    """Recreatable frame to implement main ui"""

    def __init__(self, screen: Any, webcam: Webcam) -> None:
        """Initialize frame"""
        super(MainFrame, self).__init__(screen,
                                        screen.height,
                                        screen.width,
                                        hover_focus=True,
                                        can_scroll=False,
                                        title="Photobooth")
        self._gallery_button = Button("🖼 Gallery", self._gallery, add_box=True)
        self._effects_button = Button("🖌 Effects", self._effects, add_box=True)
        self._camera_button = Button(u"📷 Take a picture", self._shoot, add_box=True)
        self._video_recording = Button(u"⏯︎ Rec. Start/Stop", self._start_stop_recording, add_box=True)
        self._quit_button = Button("🛑 Quit", self._quit, add_box=True)
        camera_layout = Layout([100], fill_frame=True)
        self.add_layout(camera_layout)
        controls_layout = Layout([1, 1, 1, 1, 1])
        self.add_layout(controls_layout)
        controls_layout.add_widget(self._gallery_button, 0)
        controls_layout.add_widget(self._video_recording, 1)
        controls_layout.add_widget(self._camera_button, 2)
        controls_layout.add_widget(self._effects_button, 3)
        controls_layout.add_widget(self._quit_button, 4)
        self.set_theme("monochrome")
        self.fix()
        self.webcam = webcam

        logger._log_info("Mainframe initialized")

    def _effects(self) -> None:
        """Open effects"""
        logger._log_info("Effects was clicked")

    def _start_stop_recording(self) -> None:
        """For the recording functionality"""
        logger._log_info("Recording started/stopped")

    @staticmethod
    def _gallery() -> None:
        """Open gallery"""
        logger._log_info("Gallery was clicked")
        raise NextScene("Gallery")

    # @staticmethod
    def _shoot(self) -> None:
        """Take an image"""
        logger._log_info("Camera was clicked")
        self.webcam.take_picture_and_save()
        self._screen.refresh()

    @staticmethod
    def _quit() -> None:
        """Quit application"""
        logger._log_info("Application was stopped")
        raise StopApplication("User pressed quit")


class GalleryFrame(Frame):
    """Recreatable frame to implement gallery ui"""

    def __init__(self, screen: Any) -> None:
        """Initialize frame"""
        super(GalleryFrame, self).__init__(screen,
                                           screen.height,
                                           screen.width,
                                           hover_focus=True,
                                           can_scroll=False,
                                           title="Photobooth")
        self._back_camera_button = Button(u"🠔 Back to 📷", self._switch_to_camera, add_box=True)
        self._browser = FileBrowser(screen.height//2, root="Gallery/")
        title_layout = Layout([1])
        self.add_layout(title_layout)
        files_layout = Layout([100], fill_frame=True)
        self.add_layout(files_layout)
        controls_layout = Layout([1, 1, 1])
        self.add_layout(controls_layout)
        title_layout.add_widget(Label("Gallery", align="^", height=screen.height//16))
        files_layout.add_widget(self._browser)
        controls_layout.add_widget(self._back_camera_button, 1)
        self.set_theme("monochrome")
        self.fix()

        logger._log_info("Galleryframe initialized")

    @staticmethod
    def _switch_to_camera() -> None:
        """Switch to Camera from Gallery"""
        logger._log_info("Switched to Camera from Gallery")
        raise NextScene("Main")


def ScreenWrapper(screen: Any, scene: Any) -> None:
    """Add scenes to screen and display"""
    scenes = [Scene([MainFrame(screen)], -1, name="Main"),
              Scene([GalleryFrame(screen)], -1, name="Gallery")
              ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


if __name__ == "__main__":
    """Main"""
    last_scene = None
    while True:
        try:
            Screen.wrapper(ScreenWrapper,
                           catch_interrupt=True,
                           arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
