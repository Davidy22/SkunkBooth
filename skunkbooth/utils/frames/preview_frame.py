import logging
from typing import Any

from asciimatics.effects import Print
from asciimatics.exceptions import NextScene
from asciimatics.renderers import Box, ColourImageFile, StaticRenderer
from asciimatics.widgets import Button, Frame, Layout

from skunkbooth.utils.frame import APP_TITLE, ImageSelectionModel, _


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
        self._back_gallery_button = Button(_("👈 Back to 🖼"), self._switch_to_gallery, add_box=True)
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
            StaticRenderer(images=[_("Photo Preview")]),
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

        logging.debug("Previewframe initialized")

    def _render_image(self) -> None:
        """Open selected image"""
        logging.debug(f"Image opened in preview {self._model.get_path()}")
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
        logging.debug("Switched to Gallery from Preview")
        raise NextScene("Gallery")
