import logging
from typing import Any

from asciimatics.exceptions import NextScene
from asciimatics.widgets import Button, FileBrowser, Frame, Label, Layout

from skunkbooth.utils.frame import APP_TITLE, ImageSelectionModel, _
from skunkbooth.utils.settings import settings


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
        self._back_camera_button = Button(_("👈 Back to 📷"), self._switch_to_camera, add_box=True)

        title_layout = Layout([1])
        self.add_layout(title_layout)
        self.files_layout = Layout([100], fill_frame=True)
        self.add_layout(self.files_layout)
        controls_layout = Layout([1, 1, 1])
        self.add_layout(controls_layout)
        title_layout.add_widget(Label(_("Gallery"), align="^", height=screen.height // 16))
        controls_layout.add_widget(self._back_camera_button, 1)
        self.set_theme("bright")

        logging.debug("Galleryframe initialized")

    def _render_browser(self) -> None:
        """Open file browser"""
        logging.debug("File browser opened")
        self.files_layout.clear_widgets()
        self._browser = FileBrowser(
            self.screen.height - 8, settings["PIC_DIR"], on_select=self._open_image
        )
        self.files_layout.add_widget(self._browser)
        self.fix()

    def _open_image(self) -> None:
        """Opening image preview"""
        if self._browser.value.endswith(".jpg"):
            logging.info(f"Image selected in gallery :{self._browser.value}")
            self._model.set_path(self._browser.value)
            raise NextScene("Preview")

    @staticmethod
    def _switch_to_camera() -> None:
        """Switch to Camera from Gallery"""
        logging.debug("Switched to Camera from Gallery")
        raise NextScene("Main")
