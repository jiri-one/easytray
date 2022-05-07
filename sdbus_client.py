from asyncio import run
from StatusNotifierWatcher import OrgKdeStatusNotifierWatcherInterface as sn_watcher


proxy = sn_watcher.new_proxy(service_name="org.kde.StatusNotifierWatcher",object_path="/StatusNotifierWatcher")

async def register_and_test() -> None:
    """after start service (or server) you need to register StatusNotifierItem to StatusNotifierWatcher"""
    await proxy.register_status_notifier_item("one.jiri.easydict")
    # and print all items which are registred in StatusNotifierWatcher
    print(await proxy.registered_status_notifier_items)

run(register_and_test())
