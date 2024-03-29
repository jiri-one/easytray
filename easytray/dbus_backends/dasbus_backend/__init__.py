from dasbus.connection import SessionMessageBus

# internal imports
from easytray.dbus_backends.tray_abc import Tray
from .dasbus_tray_model import TrayIcon


class DasbusTray(Tray):
    def __init__(
        self,
        *,
        category: str,
        id: str,
        title: str,
        status: str,
        icon: str,
        object_path: str,
        icon_theme_path: str,
        primary_callback: callable = None,
        secondary_callback: callable = None,
        scroll_callback: callable = None,
    ):
        self.tray = TrayIcon(
            category=category,
            id=id,
            title=title,
            status=status,
            icon=icon,
            object_path=object_path,
            icon_theme_path=icon_theme_path,
            primary_callback=primary_callback,
            secondary_callback=secondary_callback,
            scroll_callback=scroll_callback,
        )

    def create_tray_icon(self):
        bus = SessionMessageBus()
        bus.publish_object(self.tray.object_path, self.tray)
        snw_proxy = bus.get_proxy(
            "org.kde.StatusNotifierWatcher", "/StatusNotifierWatcher"
        )
        snw_proxy.RegisterStatusNotifierItem(self.tray.object_path)
