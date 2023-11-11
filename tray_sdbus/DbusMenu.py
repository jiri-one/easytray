from __future__ import annotations

from typing import Any, Dict, List, Tuple

from sdbus import (
    DbusDeprecatedFlag,
    DbusInterfaceCommonAsync,
    DbusNoReplyFlag,
    DbusPropertyConstFlag,
    DbusPropertyEmitsChangeFlag,
    DbusPropertyEmitsInvalidationFlag,
    DbusPropertyExplicitFlag,
    DbusUnprivilegedFlag,
    dbus_method_async,
    dbus_property_async,
    dbus_signal_async,
)


class ComCanonicalDbusmenuInterface(
    DbusInterfaceCommonAsync,
    interface_name="com.canonical.dbusmenu",
):
    @dbus_method_async(
        input_signature="iias",
        result_signature="u(ia{sv}av)",
    )
    async def get_layout(
        self,
        parent_id: int,
        recursion_depth: int,
        property_names: List[str],
    ) -> Tuple[int, Tuple[int, Dict[str, Tuple[str, Any]], List[Tuple[str, Any]]]]:
        print(parent_id,
        recursion_depth,
        property_names,)
        raise NotImplementedError

    @dbus_method_async(
        input_signature="aias",
        result_signature="a(ia{sv})",
    )
    async def get_group_properties(
        self,
        ids: List[int],
        property_names: List[str],
    ) -> List[Tuple[int, Dict[str, Tuple[str, Any]]]]:
        raise NotImplementedError

    @dbus_method_async(
        input_signature="is",
        result_signature="v",
    )
    async def get_property(
        self,
        id: int,
        name: str,
    ) -> Tuple[str, Any]:
        print("ZDEEEEEEEEE", id, name)
        raise NotImplementedError

    @dbus_method_async(
        input_signature="isvu",
    )
    async def event(
        self,
        id: int,
        event_id: str,
        data: Tuple[str, Any],
        timestamp: int,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        input_signature="a(isvu)",
        result_signature="ai",
    )
    async def event_group(
        self,
        events: List[Tuple[int, str, Tuple[str, Any], int]],
    ) -> List[int]:
        raise NotImplementedError

    @dbus_method_async(
        input_signature="i",
        result_signature="b",
    )
    async def about_to_show(
        self,
        id: int,
    ) -> bool:
        raise NotImplementedError

    @dbus_method_async(
        input_signature="ai",
        result_signature="aiai",
    )
    async def about_to_show_group(
        self,
        ids: List[int],
    ) -> Tuple[List[int], List[int]]:
        raise NotImplementedError

    @dbus_property_async(
        property_signature="u",
    )
    def version(self) -> int:
        raise NotImplementedError

    @dbus_property_async(
        property_signature="s",
    )
    def text_direction(self) -> str:
        raise NotImplementedError

    @dbus_property_async(
        property_signature="s",
    )
    def status(self) -> str:
        raise NotImplementedError

    @dbus_property_async(
        property_signature="as",
    )
    def icon_theme_path(self) -> List[str]:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature="a(ia{sv})a(ias)",
    )
    def items_properties_updated(self) -> Tuple[List[Tuple[int, Dict[str, Tuple[str, Any]]]], List[Tuple[int, List[str]]]]:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature="ui",
    )
    def layout_updated(self) -> Tuple[int, int]:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature="iu",
    )
    def item_activation_requested(self) -> Tuple[int, int]:
        raise NotImplementedError
