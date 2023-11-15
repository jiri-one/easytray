import sys

import gi

gi.require_versions({"Gtk": "4.0"})
from gi.repository import Gtk
import asyncio
import gbulb

# internal imports
from dbus_backends import get_dbus_backend
from .menu import EasyTrayMenu

DEFAULT_TRAY_BACKEND = "dasbus"
DBUS_PATH = "/SNIMenu"


class EasyTray(Gtk.Application):
    def __init__(self, loop=None):
        super().__init__(application_id="one.jiri.easydict")
        # self.connect("activate", on_activate)
        dbus_tray_backend = get_dbus_backend(DEFAULT_TRAY_BACKEND)
        tray = dbus_tray_backend(
            category="ApplicationStatus",
            id=self.get_application_id(),
            title="First open source translator.",
            status="Active",
            icon="easydict-tray-icon",
            object_path="/SNIMenu",
            icon_theme_path="/home/jiri/.local/share/icons/hicolor/285x285/apps/",
        )

        tray.create_tray_icon()

        self.menu = EasyTrayMenu(
            menu_items={
                "Settings": self.menu_buttons_catcher,
                "Help": self.menu_buttons_catcher,
                "About": self.menu_buttons_catcher,
                "Quit": self.menu_buttons_catcher,
            },
            dbus_path=DBUS_PATH,
        )
        self.menu.create_dbus_menu()

    def do_activate(self):
        parent = Gtk.ApplicationWindow(application=self)

    def menu_buttons_catcher(self, action, target):
        button_label = action.property_get("label")
        print(f"The button {button_label} was pressed.")


def main(args=sys.argv[1:]):
    if "--reload" in args:
        import hupper

        # start_reloader will only return in a monitored subprocess
        reloader = hupper.start_reloader("easytray.easytray.main")
        # monitor an extra file
        # reloader.watch_files(['foo.ini'])
    gbulb.install(True)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    easytray = EasyTray(loop)
    try:
        loop.run_forever(application=easytray)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
