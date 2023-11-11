from sys import argv

import gi

gi.require_versions({"Gtk": "4.0", "Dbusmenu": "0.4"})
from gi.repository import Gtk, Dbusmenu
import asyncio
import gbulb
from dasbus.connection import SessionMessageBus

from tray_icon_model import TrayIcon, TrayIconInterface


class EasyTray(Gtk.Application):
    def __init__(self, loop):
        super().__init__(application_id="one.jiri.easydict")
        self.loop = loop
        # self.connect("activate", on_activate)
        self.tray = TrayIcon(
            category="ApplicationStatus",
            id=self.get_application_id(),
            title="First open source translator.",
            status="Active",
            icon="easydict-tray-icon",
            object_path="/SNIMenu",
            icon_theme_path="/home/jiri/.local/share/icons/hicolor/285x285/apps/",
        )
        self.create_dbus_menu()
        self.create_tray_icon()

    def do_activate(self):
        parent = Gtk.ApplicationWindow(application=self)

    def create_dbus_menu(self):
        root_menuitem = Dbusmenu.Menuitem()
        self.server = Dbusmenu.Server(  # this has to be in self, part of GTK app or GTK object paired with GTK app
            dbus_object="/SNIMenu", root_node=root_menuitem
        )
        for name in ["Settings", "Help", "About", "Quit"]:
            item = Dbusmenu.Menuitem()
            item.property_set("label", name)
            item.connect("item-activated", lambda action, target: print(action, target))
            root_menuitem.child_append(item)

    def create_tray_icon(self):
        bus = SessionMessageBus()
        bus.publish_object("/SNIMenu", self.tray)
        snw_proxy = bus.get_proxy("org.kde.StatusNotifierWatcher", "/StatusNotifierWatcher")
        snw_proxy.RegisterStatusNotifierItem("/SNIMenu")



def main(args=argv[1:]):
    if "--reload" in args:
        import hupper

        # start_reloader will only return in a monitored subprocess
        reloader = hupper.start_reloader("easy_tray_dasbus.main")
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
