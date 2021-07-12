import sys
from typing import Any

from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Frame, Layout


class MainFrame(Frame):
    """Recreatable frame to implement main ui"""

    def __init__(self, screen: Any) -> None:
        """Initialize frame"""
        super(MainFrame, self).__init__(screen,
                                        screen.height,
                                        screen.width,
                                        hover_focus=True,
                                        can_scroll=False,
                                        title="Photobooth")
        self._gallery_button = Button("Gallery", self._gallery, add_box=True)
        self._effects_button = Button("Effects", self._effects, add_box=True)
        self._camera_button = Button(u"📷", self._shoot, add_box=True)
        self._quit_button = Button("Quit", self._quit, add_box=True)
        camera_layout = Layout([100], fill_frame=True)
        self.add_layout(camera_layout)
        controls_layout = Layout([1, 1, 1, 1])
        self.add_layout(controls_layout)
        controls_layout.add_widget(self._gallery_button, 0)
        controls_layout.add_widget(self._camera_button, 1)
        controls_layout.add_widget(self._effects_button, 2)
        controls_layout.add_widget(self._quit_button, 3)
        self.set_theme("monochrome")
        self.fix()

    def _gallery(self) -> None:
        """Open gallery"""

    def _shoot(self) -> None:
        """Take an image"""

    def _effects(self) -> None:
        """Open effects"""

    @staticmethod
    def _quit() -> None:
        """Quit application"""
        raise StopApplication("User pressed quit")


def ScreenWrapper(screen: Any, scene: Any) -> None:
    """Add scenes to screen and display"""
    scenes = [
        Scene([MainFrame(screen)], -1, name="Main")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


if __name__ == "__main__":
    """Main"""
    last_scene = None
    while True:
        try:
            Screen.wrapper(ScreenWrapper, catch_interrupt=True,
                           arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
