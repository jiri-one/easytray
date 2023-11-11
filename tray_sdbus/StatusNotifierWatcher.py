from __future__ import annotations

from typing import Any, Dict, List, Tuple

from sdbus import (DbusInterfaceCommonAsync, dbus_method_async,
                   dbus_property_async, dbus_signal_async)


class OrgKdeStatusNotifierWatcherInterface(
    DbusInterfaceCommonAsync,
    interface_name='org.kde.StatusNotifierWatcher',
):

    @dbus_method_async(
        input_signature='s',
    )
    async def register_status_notifier_item(
        self,
        service: str,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='s',
    )
    async def register_status_notifier_host(
        self,
        service: str,
    ) -> None:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='as',
    )
    def registered_status_notifier_items(self) -> List[str]:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='b',
    )
    def is_status_notifier_host_registered(self) -> bool:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='i',
    )
    def protocol_version(self) -> int:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='s',
    )
    def status_notifier_item_registered(self) -> str:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='s',
    )
    def status_notifier_item_unregistered(self) -> str:
        raise NotImplementedError

    @dbus_signal_async(
    )
    def status_notifier_host_registered(self) -> None:
        raise NotImplementedError

    @dbus_signal_async(
    )
    def status_notifier_host_unregistered(self) -> None:
        raise NotImplementedError
