from dbus_fast.aio import MessageBus
from dbus_fast.service import ServiceInterface, method, dbus_property, signal
from dbus_fast import Variant, DBusError

import asyncio


class StatusNotifierIconInterface(ServiceInterface):
    def __init__(self):
        super().__init__("org.kde.StatusNotifierItem")
        self.category = "ApplicationStatus"
        self.icon_name = "easydict-tray-icon"
        self.icon_theme_path = "/home/jiri/.local/share/icons/hicolor/285x285/apps/"
        self.id = "org.jiri.easydict"
        self.title = "First open source translator."
        self.status = "Active"
        self.window_id = 0
        self.menu = "/SNIMenu"
        self.item_is_menu = True

    @dbus_property()
    def Category(self) -> "s":
        return self.category

    @Category.setter
    def Category(self, val: "s"):
        if self.category == val:
            return

        self.category = val

    @dbus_property()
    def Id(self) -> "s":
        return self.id

    @Id.setter
    def Id(self, val: "s"):
        if self.id == val:
            return

        self.id = val

    @dbus_property()
    def Title(self) -> "s":
        return self.title

    @Title.setter
    def Title(self, val: "s"):
        if self.title == val:
            return

        self.title = val

    @dbus_property()
    def Status(self) -> "s":
        return self.status

    @Status.setter
    def Status(self, val: "s"):
        if self.status == val:
            return

        self.status = val

    @dbus_property()
    def WindowId(self) -> "i":
        return self.window_id

    @WindowId.setter
    def WindowId(self, val: "i"):
        if self.window_id == val:
            return

        self.window_id = val

    @dbus_property()
    def IconThemePath(self) -> "s":
        return "/home/jiri/.local/share/icons/hicolor/285x285/apps/"

    @IconThemePath.setter
    def IconThemePath(self, val: "s"):
        if self.icon_theme_path == val:
            return

        self.icon_theme_path = val

    @dbus_property()
    def Menu(self) -> "o":
        return self.menu

    @Menu.setter
    def Menu(self, val: "o"):
        if self.menu == val:
            return

        self.menu = val

    @dbus_property()
    def ItemIsMenu(self) -> "b":
        return self.item_is_menu

    @ItemIsMenu.setter
    def ItemIsMenu(self, val: "b"):
        if self.item_is_menu == val:
            return

        self.item_is_menu = val

    @dbus_property()
    def IconName(self) -> "s":
        return self.icon_name

    @IconName.setter
    def IconName(self, val: "s"):
        if self.icon_name == val:
            return

        self.icon_name = val

    @method()
    def context_menu(
        self,
        x: "i",
        y: "i",
    ) -> None:
        pass


async def main():
    bus = await MessageBus().connect()
    # the introspection xml would normally be included in your project, but
    # this is convenient for development
    snw_introspection = await bus.introspect(
        "org.kde.StatusNotifierWatcher", "/StatusNotifierWatcher"
    )

    obj = bus.get_proxy_object(
        "org.kde.StatusNotifierWatcher", "/StatusNotifierWatcher", snw_introspection
    )
    snw_interface = obj.get_interface("one.jiri.easydict")

    sni_interface = StatusNotifierIconInterface()
    bus.export("/SNIMenu", sni_interface)

    # await bus.request_name("one.jiri.easydict")

    await snw_interface.call_register_status_notifier_item("/SNIMenu")
    sni_interface.changed()

    await bus.wait_for_disconnect()
    await bus.wait_for_disconnect()

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
