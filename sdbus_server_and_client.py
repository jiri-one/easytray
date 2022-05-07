from asyncio import new_event_loop

from StatusNotifierItem import OrgKdeStatusNotifierItemInterface
from StatusNotifierWatcher import OrgKdeStatusNotifierWatcherInterface as sn_watcher

from sdbus import request_default_bus_name_async

# instance of Status Notifier Item Interface
sn_item_interface = OrgKdeStatusNotifierItemInterface()

# this is server part
async def startup() -> None:
    """Perform async startup actions"""
    await request_default_bus_name_async(f'one.jiri.easydict')
    # Export the object to dbus
    sn_item_interface.export_to_dbus('/StatusNotifierItem')

# this is client part
proxy = sn_watcher.new_proxy(service_name="org.kde.StatusNotifierWatcher",object_path="/StatusNotifierWatcher")

async def register_sn_item() -> None:
    await proxy.register_status_notifier_item("one.jiri.easydict")
    # check if item is really registred
    print(await proxy.registered_status_notifier_items)

loop = new_event_loop()
loop.run_until_complete(startup()) # run of server/service part
loop.run_until_complete(register_sn_item()) # run of client part
#tasks = loop.create_task(register_sn_item()) # run (as task) client part
loop.run_forever()
