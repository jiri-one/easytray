import sys

import gi
from pathlib import Path

gi.require_versions({"Gtk": "4.0"})
from gi.repository import Gtk
import asyncio
import gbulb

# internal imports
from .dbus_backends import get_dbus_backend, install_icon_to_xdg_data_home, DasbusTray
from .menu import EasyTrayMenu

DEFAULT_TRAY_BACKEND = "dasbus"
DBUS_PATH = "/SNIMenu"


class EasyTray(Gtk.Application):
    def __init__(self, loop=None):
        super().__init__(application_id="one.jiri.easydict")
        # install the icon to the system
        icon = Path(__file__).parent / "easydict-tray-icon.png"
        icon_path = install_icon_to_xdg_data_home(icon_path=icon, icon_size=285)
        # get the dbus backend a set the tray icon
        dbus_tray_backend: DasbusTray = get_dbus_backend(DEFAULT_TRAY_BACKEND)
        tray = dbus_tray_backend(
            category="ApplicationStatus",
            id=self.get_application_id(),
            title="Tray icon example.",
            status="Active",
            icon="easydict-tray-icon",
            object_path=DBUS_PATH,  # dbus path has to be same like menu
            icon_theme_path=icon_path,
            primary_callback=self.primary_activated,
            secondary_callback=self.secondary_activated,
            scroll_callback=self.scroll_activated,
        )
        # you need to call that method to show tray icon
        tray.create_tray_icon()
        # and if you want, you can connect menu to the tray icon
        self.menu = EasyTrayMenu(
            menu_items={
                "Settings": self.menu_buttons_catcher,
                "Help": self.menu_buttons_catcher,
                "About": self.menu_buttons_catcher,
                "Quit": self.menu_buttons_catcher,
            },
            dbus_path=DBUS_PATH,
        )
        # you need to call that method to show menu
        self.menu.create_dbus_menu()

    def do_activate(self):
        parent = Gtk.ApplicationWindow(application=self)

    def menu_buttons_catcher(self, action, target):
        button_label = action.property_get("label")
        print(f"The button {button_label} was pressed.")

    def primary_activated(self, x: int, y: int):
        print("Primary button has been activated", x, y)

    def secondary_activated(self, x: int, y: int):
        print("Secondary button has been activated", x, y)

    def scroll_activated(self, delta: int, orientation: str):
        print("Scroll whell has been activated", delta, orientation)


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
