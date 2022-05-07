
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from sdbus import (DbusInterfaceCommonAsync, dbus_method_async,
                   dbus_property_async, dbus_signal_async)

ed_image = open("ed_icon.rgba", "rb").read()

class OrgKdeStatusNotifierItemInterface(
    DbusInterfaceCommonAsync,
    interface_name='org.kde.StatusNotifierItem',
):

    # @dbus_method_async(
    #     input_signature='s',
    # )
    # async def provide_xdg_activation_token(
    #     self,
    #     token: str,
    # ) -> None:
    #     print("token: ", token)

    @dbus_method_async(
        input_signature='ii',
    )
    async def context_menu(
        self,
        x: int,
        y: int,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='ii',
    )
    async def activate(
        self,
        x: int,
        y: int,
    ) -> None:
        print("activated by primary button", x, y)

    @dbus_method_async(
        input_signature='ii',
    )
    async def secondary_activate(
        self,
        x: int,
        y: int,
    ) -> None:
        print("secondary_activate", x, y)

    @dbus_method_async(
        input_signature='is',
    )
    async def scroll(
        self,
        delta: int,
        orientation: str,
    ) -> None:
        print("Scroll", delta, orientation)

    @dbus_property_async(
        property_signature='s',
    )
    def category(self) -> str:
        return "ApplicationStatus"

    @dbus_property_async(
        property_signature='s',
    )
    def id(self) -> str:
        return "org.jiri.easydict"

    @dbus_property_async(
        property_signature='s',
    )
    def title(self) -> str:
        return "First open source translator."

    @dbus_property_async(
        property_signature='s',
    )
    def status(self) -> str:
        return "Active"

    @dbus_property_async(
        property_signature='i',
    )
    def window_id(self) -> int:
        return 0

    # @dbus_property_async(
    #     property_signature='s',
    # )
    # def icon_theme_path(self) -> str:
    #     raise NotImplementedError

    # @dbus_property_async(
    #     property_signature='o',
    # )
    # def menu(self) -> str:
    #     raise NotImplementedError

    @dbus_property_async(
        property_signature='b',
    )
    def item_is_menu(self) -> bool:
        return False

    # @dbus_property_async(
    #     property_signature='s',
    # )
    # def icon_name(self) -> str:
    #     return "mail-read"

    @dbus_property_async(
        property_signature='a(iiay)',
    )
    def icon_pixmap(self) -> List[Tuple[int, int, bytes]]:
        return [(22,22,ed_image)]

    # @dbus_property_async(
    #     property_signature='s',
    # )
    # def overlay_icon_name(self) -> str:
    #     raise NotImplementedError

    # @dbus_property_async(
    #     property_signature='a(iiay)',
    # )
    # def overlay_icon_pixmap(self) -> List[Tuple[int, int, bytes]]:
    #     return [(255,256,ed_image)]

    @dbus_property_async(
        property_signature='s',
    )
    def attention_icon_name(self) -> str:
        return "mail-read"

    # @dbus_property_async(
    #     property_signature='a(iiay)',
    # )
    # def attention_icon_pixmap(self) -> List[Tuple[int, int, bytes]]:
    #     return [(255,256,ed_image)]

    # @dbus_property_async(
    #     property_signature='s',
    # )
    # def attention_movie_name(self) -> str:
    #     return "mail-read"

    # @dbus_property_async(
    #     property_signature='(sa(iiay)ss)',
    # )
    # def tool_tip(self) -> Tuple[str, List[Tuple[int, int, bytes]], str, str]:
    #     raise NotImplementedError

    @dbus_signal_async(
    )
    def new_title(self) -> None:
        raise NotImplementedError

    @dbus_signal_async(
    )
    def new_icon(self) -> None:
        raise NotImplementedError

    @dbus_signal_async(
    )
    def new_attention_icon(self) -> None:
        raise NotImplementedError

    @dbus_signal_async(
    )
    def new_overlay_icon(self) -> None:
        raise NotImplementedError

    @dbus_signal_async(
    )
    def new_menu(self) -> None:
        raise NotImplementedError

    @dbus_signal_async(
    )
    def new_tool_tip(self) -> None:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='s',
    )
    def new_status(self) -> str:
        raise NotImplementedError
