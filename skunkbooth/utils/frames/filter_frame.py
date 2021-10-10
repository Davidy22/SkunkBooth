import logging
from typing import Any

from asciimatics.event import Event, KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, CheckBox, Frame, Label, Layout

from skunkbooth.utils.frame import APP_TITLE, _


class FilterFrame(Frame):
    """Recreatable frame to implement filter ui"""

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
        self._back_camera_button = Button(_("👈 Back to 📷"), self._switch_to_camera, add_box=True)
        self.filters = filters
        self.filterList = [[i, None] for i in filters.filters]

        title_layout = Layout([1])
        self.add_layout(title_layout)
        title_layout.add_widget(Label(_("Filters"), align="^", height=screen.height // 16))

        filters_layout = Layout([100, 100], fill_frame=True)
        self.add_layout(filters_layout)

        for f in self.filterList:
            temp = CheckBox(f[0].name, name=f[0].name)
            f[1] = temp
            logging.debug(f"{f[0].name} button created")
            filters_layout.add_widget(temp)
            filters_layout.add_widget(Label(f"{f[0].description}   ]", align=">"), 1)

        controls_layout = Layout([1, 1, 1])
        self.add_layout(controls_layout)
        controls_layout.add_widget(self._back_camera_button, 1)

        self.set_theme("bright")
        self.fix()

        logging.debug("Galleryframe initialized")

    def _switch_to_camera(self) -> None:
        """Switch to Camera from Filters"""
        logging.debug("Switched to Camera from Filters")
        for i in self.filterList:
            logging.debug(f"{i[0]}, {self.filters.is_loaded(i[0])}, {i[1].value}")
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
