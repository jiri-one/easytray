from sys import argv

import gi

gi.require_versions({"Gtk": "4.0", "Dbusmenu": "0.4"})
from gi.repository import Gtk, Dbusmenu
import asyncio
import gbulb

from dbus_fast.aio import MessageBus

from fast_tray import StatusNotifierIconInterface


class EasyTray(Gtk.Application):
    def __init__(self, loop):
        super().__init__(application_id="one.jiri.easydict")
        self.loop = loop
        # self.connect("activate", on_activate)
        self.id = self.get_application_id()
        self.tray_task = self.loop.create_task(self.tray_dbus_service())
        self.create_dbus_menu()

    def do_activate(self):
        parent = Gtk.ApplicationWindow(application=self)

    async def tray_dbus_service(self):
        bus = await MessageBus().connect()
        # the introspection xml would normally be included in your project, but
        # this is convenient for development
        snw_introspection = await bus.introspect(
            "org.kde.StatusNotifierWatcher", "/StatusNotifierWatcher"
        )

        obj = bus.get_proxy_object(
            "org.kde.StatusNotifierWatcher", "/StatusNotifierWatcher", snw_introspection
        )
        snw_interface = obj.get_interface("org.kde.StatusNotifierWatcher")


        sni_interface = StatusNotifierIconInterface()
        bus.export("/SNIMenu", sni_interface)
        #await bus.request_name("one.jiri.easydict")

        await snw_interface.call_register_status_notifier_item("/SNIMenu")
        await bus.wait_for_disconnect()

        await asyncio.Event().wait()

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


def main(args=argv[1:]):
    if "--reload" in args:
        import hupper

        # start_reloader will only return in a monitored subprocess
        reloader = hupper.start_reloader("easy_tray.main")
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
