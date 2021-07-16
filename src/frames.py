import os
import sys
from datetime import datetime
from multiprocessing import Process, Value, Pool
from typing import Any

from asciimatics.exceptions import (
    NextScene, ResizeScreenError, StopApplication
)
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import (
    Button, CheckBox, FileBrowser, Frame, Label, Layout
)

from logger import CustomLogger
from webcam import Webcam

logger = CustomLogger(fileoutpath="Logs" + os.sep + "ui.log")

val = Value('i', 0)


class MainFrame(Frame):
    """Recreatable frame to implement main ui"""

    def __init__(self, screen: Any, webcam: Webcam) -> None:
        """Initialize frame"""
        super(MainFrame, self).__init__(screen,
                                        int(screen.height//10),
                                        screen.width,
                                        x=0,
                                        y=7,  # depends on height occupied by figlet chosen
                                        hover_focus=True,
                                        can_scroll=False,
                                        title="Photobooth",
                                        has_border=False)
        # Made the labels below short so as to fit small screens
        self._gallery_button = Button(u"🖼 Gallery", self._gallery, add_box=True)
        self._effects_button = Button(u"🖌 Effects", self._filters, add_box=True)
        self._camera_button = Button(u"📷 Shoot", self._shoot, add_box=True)
        self._video_recording = CheckBox(text=u"⏯︎ Record", on_change=self._start_stop_recording)
        self._quit_button = Button(u"🛑 Quit", self._quit, add_box=True)

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

        """This is the part used for MP"""
        # pros = Process(name="Background work", target=self.webcam.recording_utility, args=(val,))
        # pros.daemon = True
        # pros.start()
        # p = Pool()
        # p.apply_async(func=self.webcam.recording_utility, args=(val,))
        logger._log_info("Mainframe initialized")

    @staticmethod
    def _filters() -> None:
        """Open effects"""
        logger._log_info("Effects was clicked")
        raise NextScene("Filters")

    def _start_stop_recording(self) -> None:
        """For the recording functionality"""
        if val.value == 1:
            logger._log_info("Recording started inside if, value= " + str(val.value))
            val.value = 0
            # queue.put(self.webcam)
            return None
        else:
            logger._log_info("Recording stopped inside else, value= " + str(val.value))
            val.value = 1
            return None

    @staticmethod
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
                                           screen.height-6,
                                           screen.width,
                                           y=6,  # depends on height occupied by figlet chosen
                                           hover_focus=True,
                                           has_border=False,
                                           can_scroll=False)
        self._back_camera_button = Button(u"🠔 Back to 📷", self._switch_to_camera, add_box=True)
        self._browser = FileBrowser(screen.height//2, "gallery/")
        title_layout = Layout([1])
        self.add_layout(title_layout)
        files_layout = Layout([100], fill_frame=True)
        self.add_layout(files_layout)
        controls_layout = Layout([1, 1, 1])
        self.add_layout(controls_layout)
        title_layout.add_widget(Label("Gallery", align="^", height=screen.height // 16))
        files_layout.add_widget(self._browser)
        controls_layout.add_widget(self._back_camera_button, 1)
        self.set_theme("bright")
        self.fix()

        logger._log_info("Galleryframe initialized")

    @staticmethod
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
            title="Photobooth",
            data=data,
        )
        self._back_camera_button = Button(
            "👈 Back to 📷", self._switch_to_camera, add_box=True
        )
        self.filters = filters
        self.filterList = [[i, None] for i in filters.filters]

        title_layout = Layout([1])
        self.add_layout(title_layout)
        title_layout.add_widget(Label("Filters", align="^", height=screen.height // 16))

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
            logger._log_info(f"{i[0]}, {self.filters.is_loaded(i[0])}, {i[1].value}")
            if self.filters.is_loaded(i[0].name) != i[1].value:
                self.filters.toggle(i[0].name)
        self.save()
        raise NextScene("Main")


def ScreenWrapper(screen: Any, scene: Any) -> None:
    """Add scenes to screen and display"""
    scenes = [
        Scene([MainFrame(screen)], -1, name="Main"),
        Scene([GalleryFrame(screen)], -1, name="Gallery"),
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


if __name__ == "__main__":
    """Main"""
    last_scene = None
    while True:
        try:
            Screen.wrapper(ScreenWrapper, catch_interrupt=True, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
