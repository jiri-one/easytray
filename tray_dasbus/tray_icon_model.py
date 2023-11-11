from enum import Enum
from functools import partial
from itertools import filterfalse, chain
from typing import Iterable

from gi.repository import GLib, GObject, Gio, Dbusmenu, Gtk, Gdk
from dasbus.connection import SessionMessageBus
from dasbus.server.interface import dbus_interface, dbus_signal, dbus_class
from dasbus.server.template import InterfaceTemplate
from dasbus.identifier import DBusServiceIdentifier, DBusObjectIdentifier
from dasbus.typing import Str, UInt32, Bool, Int, Byte, ObjPath, List, Tuple
from pathlib import Path

xml_file = "/usr/share/dbus-1/interfaces/kf5_org.kde.StatusNotifierItem.xml"
#print(xml_file.exists())
#@dbus_interface("org.kde.StatusNotifierItem")
class TrayIconInterface:
    with open(xml_file) as xml:
        __dbus_xml__ = xml.read()
    
    # def __init__(self, implementation):
    #     super().__init__(implementation)



class TrayIcon(TrayIconInterface, InterfaceTemplate):
    def __init__(
        self,
        category: str,
        id: str,
        title: str,
        status: str,
        icon: str,
        icon_theme_path: str,
        object_path: str,
        window_id: int = 0,
        overlay_icon: str | None = None,
        attention_icon: str | None = None,
        tooltip: tuple[Gio.Icon | None, str, str] | None = None,
        item_is_menu: bool = True,
    ):
        #super().__init__(self)
        self.category = category
        self.id = id
        self.title = title
        self.status = status
        self.icon = icon
        self.icon_theme_path = icon_theme_path
        self.object_path = object_path
        self.window_id = window_id
        self.overlay_icon = overlay_icon
        self.attention_icon = attention_icon
        self.tooltip = tooltip
        self.item_is_menu = item_is_menu

    @property
    def Category(self) -> Str:
        return self.category

    @property
    def Id(self) -> Str:
        return self.id

    @property
    def Title(self) -> Str:
        return self.title

    @property
    def Status(self) -> Str:
        return self.status

    @property
    def WindowId(self) -> UInt32:
        return self.window_id

    @property
    def IconName(self) -> Str:
        return self.icon
    
    @IconName.setter
    def IconName(self, icon: str) -> None:
        self.icon = icon
        #self.interface.NewIcon.emit()

    @property
    def IconThemePath(self) -> Str:
        return self.icon_theme_path

    @property
    def IconPixmap(self) -> List[Tuple[Int, Int, List[Byte]]]:
        return ""

    @property
    def OverlayIconName(self) -> Str:
        return ""

    @property
    def OverlayIconPixmap(self) -> List[Tuple[Int, Int, List[Byte]]]:
        return ""

    @property
    def AttentionIconName(self) -> Str:
        return ""

    @property
    def AttentionIconPixmap(self) -> List[Tuple[Int, Int, List[Byte]]]:
        return ""

    @property
    def AttentionMovieName(self) -> Str:
        return ""

    @property
    def ItemIsMenu(self) -> Bool:
        return True

    @property
    def Menu(self) -> ObjPath:
        return self.object_path

    @property
    def ToolTip(self) -> Tuple[Str, List[Tuple[Int, Int, List[Byte]]], Str, Str]:
        return "", [], "", ""


    @dbus_signal
    def NewTitle(self) -> None:
        pass

    @dbus_signal
    def NewIcon(self) -> None:
        pass

    @dbus_signal
    def NewMenu(self) -> None:
        pass

    @dbus_signal
    def NewAttentionIcon(self) -> None:
        pass

    @dbus_signal
    def NewOverlayIcon(self) -> None:
        pass

    @dbus_signal
    def NewToolTip(self) -> None:
        pass

    @dbus_signal
    def NewStatus(self, status: Str) -> None:
        pass

    def ContextMenu(self, x: int, y: int) -> None:
        pass

    def Activate(self, x: int, y: int) -> None:
        pass

    def SecondaryActivate(self, x: int, y: int) -> None:
        pass

    def Scroll(self, delta: int, orientation: str) -> None:
        pass

    def ProvideXdgActivationToken(self, token: str) -> str:
        pass


@dbus_interface("org.kde.StatusNotifierItem")
class _TrayIconProxy(InterfaceTemplate):
    def __init__(self, tray_icon: "TrayIconOld", object_path: str) -> None:
        super().__init__(tray_icon)
        self.__object_path = object_path

    @property
    def Category(self) -> Str:
        return self.implementation.category

    @property
    def Id(self) -> Str:
        return self.implementation.id

    @property
    def Title(self) -> Str:
        return self.implementation.title

    @property
    def Status(self) -> Str:
        return self.implementation.status

    @property
    def WindowId(self) -> UInt32:
        return self.implementation.window_id

    @property
    def IconName(self) -> Str:
        return self.implementation.icon

    @property
    def IconThemePath(self) -> Str:
        return self.implementation.icon_theme_path

    @property
    def IconPixmap(self) -> List[Tuple[Int, Int, List[Byte]]]:
        return self.__icon_pixmap(self.implementation.icon)

    @property
    def OverlayIconName(self) -> Str:
        return self.__icon_name(self.implementation.overlay_icon)

    @property
    def OverlayIconPixmap(self) -> List[Tuple[Int, Int, List[Byte]]]:
        return self.__icon_pixmap(self.implementation.overlay_icon)

    @property
    def AttentionIconName(self) -> Str:
        return self.__icon_name(self.implementation.attention_icon)

    @property
    def AttentionIconPixmap(self) -> List[Tuple[Int, Int, List[Byte]]]:
        return self.__icon_pixmap(self.implementation.attention_icon)

    @property
    def AttentionMovieName(self) -> Str:
        return ""

    @property
    def ToolTip(self) -> Tuple[Str, List[Tuple[Int, Int, List[Byte]]], Str, Str]:
        if self.implementation.tooltip is None:
            return "", [], "", ""
        icon, title, description = self.implementation.tooltip
        return self.__icon_name(icon), self.__icon_pixmap(icon), title, description

    @property
    def ItemIsMenu(self) -> Bool:
        return self.implementation.item_is_menu

    @property
    def Menu(self) -> ObjPath:
        return self.__object_path

    def ContextMenu(self, x: Int, y: Int) -> None:
        self.implementation.emit("context-menu", x, y)

    def Activate(self, x: Int, y: Int) -> None:
        self.implementation.emit("activate", x, y)

    def SecondaryActivate(self, x: Int, y: Int) -> None:
        self.implementation.emit("secondary-activate", x, y)

    def Scroll(self, delta: Int, orientation: Str) -> None:
        self.implementation.emit("scroll", delta, orientation)

    @dbus_signal
    def NewTitle(self) -> None:
        pass

    @dbus_signal
    def NewIcon(self) -> None:
        pass

    @dbus_signal
    def NewAttentionIcon(self) -> None:
        pass

    @dbus_signal
    def NewOverlayIcon(self) -> None:
        pass

    @dbus_signal
    def NewToolTip(self) -> None:
        pass

    @dbus_signal
    def NewStatus(self, status: Str) -> None:
        pass

    @staticmethod
    def __icon_name(icon: Gio.Icon) -> str:
        if isinstance(icon, Gio.ThemedIcon):
            return icon.get_names()[0]
        else:
            return ""

    @staticmethod
    def __icon_pixmap(icon: Gio.Icon) -> List[Tuple[Int, Int, List[Byte]]]:
        return []


class TrayIconOld(GObject.Object):
    __bus = SessionMessageBus()
    __watcher = DBusServiceIdentifier(__bus, ("org", "kde", "StatusNotifierWatcher"))
    __watcher_object = DBusObjectIdentifier(("StatusNotifierWatcher",))

    def __init__(
        self,
        *,
        category: str,
        id: str,
        title: str,
        status: str,
        window_id=0,
        icon: str,
        overlay_icon: str | None = None,
        attention_icon: str | None = None,
        tooltip: tuple[Gio.Icon | None, str, str] | None = None,
        item_is_menu=True,
        icon_theme_path: str,
        object_path: str,
    ) -> None:
        super().__init__()
        self._category = category
        self._id = id
        self._title = title
        self._status = status
        self._window_id = window_id
        self._icon = icon
        self._overlay_icon = overlay_icon
        self._attention_icon = attention_icon
        self._tooltip = tooltip
        self._item_is_menu = item_is_menu
        self.interface = _TrayIconProxy(self, object_path)
        self._icon_theme_path = icon_theme_path

        self.__bus.publish_object(object_path, self.interface)
        proxy = self.__watcher.get_proxy(self.__watcher_object)
        proxy.RegisterStatusNotifierItem(object_path)

    @property
    def category(self) -> str:
        return self._category

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        self._title = title
        self.interface.NewTitle.emit()

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, status: str) -> None:
        self._status = status
        self.interface.NewStatus.emit(status)

    @property
    def window_id(self) -> int:
        return self._window_id

    @property
    def icon(self) -> str:
        return self._icon

    @icon.setter
    def icon(self, icon: str) -> None:
        self._icon = icon
        self.interface.NewIcon.emit()

    @property
    def icon_theme_path(self) -> str:
        return self._icon_theme_path

    @icon_theme_path.setter
    def icon_theme_path(self, icon_theme_path: str) -> None:
        self._icon_theme_path = icon_theme_path

    @property
    def overlay_icon(self) -> Gio.Icon:
        return self._overlay_icon

    @overlay_icon.setter
    def overlay_icon(self, overlay_icon: Gio.Icon) -> None:
        self._overlay_icon = overlay_icon
        self.interface.NewOverlayIcon.emit()

    @property
    def attention_icon(self) -> Gio.Icon:
        return self._attention_icon

    @attention_icon.setter
    def attention_icon(self, attention_icon: Gio.Icon) -> None:
        self._attention_icon = attention_icon
        self.interface.NewAttentionIcon.emit()

    @property
    def tooltip(self) -> tuple[Gio.Icon | None, str, str] | None:
        return self._tooltip

    @tooltip.setter
    def tooltip(self, tooltip: tuple[Gio.Icon | None, str, str] | None):
        self._tooltip = tooltip
        self.interface.NewToolTip.emit()

    @property
    def item_is_menu(self) -> bool:
        return self._item_is_menu

    @GObject.Signal("context-menu")
    def context_menu(self, x: int, y: int) -> None:
        pass

    @GObject.Signal("activate")
    def activate(self, x: int, y: int) -> None:
        pass

    @GObject.Signal("secondary-activate")
    def secondary_activate(self, x: int, y: int) -> None:
        pass

    @GObject.Signal("scroll")
    def scroll(self, delta: int, orientation: str) -> None:
        pass
