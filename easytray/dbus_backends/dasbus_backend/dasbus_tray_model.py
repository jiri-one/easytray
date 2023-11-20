from gi.repository import Gio
from dasbus.server.interface import dbus_signal, dbus_class
from dasbus.server.template import InterfaceTemplate
from dasbus.identifier import DBusServiceIdentifier, DBusObjectIdentifier
from dasbus.typing import Str, UInt32, Bool, Int, Byte, ObjPath, List, Tuple
from pathlib import Path

XML_FILE = Path(__file__).parent / "kf5_org.kde.StatusNotifierItem.xml"
assert XML_FILE.exists()


class TrayIconInterface:
    with open(XML_FILE) as xml:
        __dbus_xml__ = xml.read()


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
        # self.interface.NewIcon.emit()

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
        print("primary activated")

    def SecondaryActivate(self, x: int, y: int) -> None:
        pass

    def Scroll(self, delta: int, orientation: str) -> None:
        print(delta, orientation)

    def ProvideXdgActivationToken(self, token: str) -> str:
        pass
