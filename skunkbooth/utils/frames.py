import logging
from datetime import datetime
from typing import Any, Callable

from asciimatics.effects import Effect, Print
from asciimatics.event import Event, KeyboardEvent
from asciimatics.exceptions import NextScene, StopApplication
from asciimatics.renderers import Box, ColourImageFile, StaticRenderer
from asciimatics.screen import Screen
from asciimatics.widgets import (
    Button, CheckBox, FileBrowser, Frame, Label, Layout
)

from skunkbooth.data.defaults import PIC_DIR

from .webcam import Webcam

APP_TITLE = "Skunkbooth"


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
        self._gallery_button = Button("🖼 Gallery", self._gallery, add_box=True)
        self._effects_button = Button("🖌 Effects", self._filters, add_box=True)
        self._camera_button = Button("📷 Shoot", self._shoot, add_box=True)
        self._video_recording = CheckBox(text="⏯︎ Record", on_change=toggle)
        self._quit_button = Button("🛑 Quit", self._quit, add_box=True)

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

        logging.info("Mainframe initialized")

    @staticmethod
    def _filters() -> None:
        """Open effects"""
        logging.info("Effects was clicked")
        raise NextScene("Filters")

    @staticmethod
    def _gallery() -> None:
        """Open gallery"""
        logging.info("Gallery was clicked")
        raise NextScene("Gallery")

    # @staticmethod
    def _shoot(self) -> None:
        """Take an image"""
        logging.info("Camera was clicked")
        img_name = f"{PIC_DIR}/Image-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.jpg"
        logging.info(f"Saving image {img_name}")
        self.webcam.take_picture_and_save(img_name)
        self._screen.refresh()

    @staticmethod
    def _quit() -> None:
        """Quit application"""
        logging.info("Application was stopped")
        raise StopApplication("User pressed quit")


class GalleryFrame(Frame):
    """Recreatable frame to implement gallery ui"""

    def __init__(self, screen: Any, model: ImageSelectionModel) -> None:
        """Initialize frame"""
        super(GalleryFrame, self).__init__(
            screen,
            screen.height,
            screen.width,
            y=0,
            hover_focus=True,
            has_border=True,
            can_scroll=False,
            on_load=self._render_browser,
            title=APP_TITLE,
            reduce_cpu=True,
        )
        self._model = model
        self._back_camera_button = Button("👈 Back to 📷", self._switch_to_camera, add_box=True)

        title_layout = Layout([1])
        self.add_layout(title_layout)
        self.files_layout = Layout([100], fill_frame=True)
        self.add_layout(self.files_layout)
        controls_layout = Layout([1, 1, 1])
        self.add_layout(controls_layout)
        title_layout.add_widget(Label("Gallery", align="^", height=screen.height // 16))
        controls_layout.add_widget(self._back_camera_button, 1)
        self.set_theme("bright")

        logging.info("Galleryframe initialized")

    def _render_browser(self) -> None:
        """Open file browser"""
        logging.info("File browser opened")
        self.files_layout.clear_widgets()
        self._browser = FileBrowser(self.screen.height - 8, PIC_DIR, on_select=self._open_image)
        self.files_layout.add_widget(self._browser)
        self.fix()

    def _open_image(self) -> None:
        """Opening image preview"""
        if self._browser.value.endswith(".jpg"):
            logging.info(f"Image selected in gallery :{self._browser.value}")
            self._model.set_path(self._browser.value)
            raise NextScene("Preview")
        else:
            pass

    @staticmethod
    def _switch_to_camera() -> None:
        """Switch to Camera from Gallery"""
        logging.info("Switched to Camera from Gallery")
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
            reduce_cpu=True,
        )
        self._back_camera_button = Button("👈 Back to 📷", self._switch_to_camera, add_box=True)
        self.filters = filters
        self.filterList = [[i, None] for i in filters.filters]

        title_layout = Layout([1])
        self.add_layout(title_layout)
        title_layout.add_widget(Label("Filters", align="^", height=screen.height // 16))

        filters_layout = Layout([100, 100], fill_frame=True)
        self.add_layout(filters_layout)

        for f in self.filterList:
            temp = CheckBox(f[0].name, name=f[0].name)
            f[1] = temp
            logging.info(f"{f[0].name} button created")
            filters_layout.add_widget(temp)
            filters_layout.add_widget(Label(f"{f[0].description}   ]", align=">"), 1)

        controls_layout = Layout([1, 1, 1])
        self.add_layout(controls_layout)
        controls_layout.add_widget(self._back_camera_button, 1)

        self.set_theme("bright")
        self.fix()

        logging.info("Galleryframe initialized")

    def _switch_to_camera(self) -> None:
        """Switch to Camera from Filters"""
        logging.info("Switched to Camera from Filters")
        for i in self.filterList:
            logging.info(f"{i[0]}, {self.filters.is_loaded(i[0])}, {i[1].value}")
            if self.filters.is_loaded(i[0].name) != i[1].value:
                self.filters.toggle(i[0].name)
        self.save()
        raise NextScene("Main")

    def _skip_to_next_page(self) -> None:
        """Function to skip to next page of filters"""
        pass

    def process_event(self, event: Event) -> None:
        """Deals with keyboard events that happen in this screen"""
        super(FilterFrame, self).process_event(event)
        if isinstance(event, KeyboardEvent):
            c = event.key_code
            layout = self._layouts[1]
            if c == Screen.KEY_HOME:
                self.switch_focus(layout, 0, 0)
            elif c == Screen.KEY_END:
                self.switch_focus(layout, 0, len(self.filterList) - 1)
            elif c == Screen.KEY_PAGE_UP:
                pass
            elif c == Screen.KEY_PAGE_DOWN:
                pass


class PreviewFrame(Frame):
    """Recreatable frame to implement preview ui"""

    def __init__(self, screen: Any, model: ImageSelectionModel) -> None:
        """Initialize frame"""
        super(PreviewFrame, self).__init__(
            screen,
            3,
            screen.width - 4,
            x=2,
            y=screen.height - 4,
            on_load=self._render_image,
            hover_focus=True,
            has_border=False,
            can_scroll=False,
            title=APP_TITLE,
            reduce_cpu=True,
        )
        self._model = model
        self._back_gallery_button = Button("👈 Back to 🖼", self._switch_to_gallery, add_box=True)
        box = Box(screen.width, screen.height, uni=True)
        box_effect = Print(screen, box, y=0)
        self.add_effect(box_effect)

        title_effect = Print(
            screen,
            StaticRenderer(images=[" " + APP_TITLE + " "]),
            y=0,
            x=int(((screen.width - 4) / 2) - 5),
            attr=1,
            transparent=False,
        )
        self.add_effect(title_effect)

        header_effect = Print(
            screen,
            StaticRenderer(images=["Photo Preview"]),
            y=1,
            x=int(((screen.width - 4) / 2) - 5),
            attr=1,
            colour=2,  # GreenColor
            transparent=False,
        )
        self.add_effect(header_effect)

        controls_layout = Layout([1, 1, 1])
        self.add_layout(controls_layout)
        controls_layout.add_widget(self._back_gallery_button, 1)
        self.set_theme("bright")
        self.fix()

        logging.info("Previewframe initialized")

    def _render_image(self) -> None:
        """Open selected image"""
        logging.info(f"Image opened in preview {self._model.get_path()}")
        preview_effect = Print(
            self.screen,
            ColourImageFile(
                self.screen, self._model.get_path(), height=self.screen.height - 8, uni=True
            ),
            y=4,
            speed=0,
            transparent=False,
        )
        self.add_effect(preview_effect)

    @staticmethod
    def _switch_to_gallery() -> None:
        """Switch to Gallery from Preview"""
        logging.info("Switched to Gallery from Preview")
        raise NextScene("Gallery")
