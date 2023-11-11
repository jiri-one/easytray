import asyncio
from sys import argv
from queue import Queue
from threading import Thread

from StatusNotifierItem import OrgKdeStatusNotifierItemInterface
from StatusNotifierWatcher import OrgKdeStatusNotifierWatcherInterface as sn_watcher
from DbusMenu import ComCanonicalDbusmenuInterface

from sdbus import request_default_bus_name_async

import gi
gi.require_versions({"Gtk": "4.0", 'Dbusmenu': '0.4'})
from gi.repository import Gtk, Dbusmenu

# instance of Status Notifier Item Interface
sn_item_interface = OrgKdeStatusNotifierItemInterface()
dbusmenu_interface = ComCanonicalDbusmenuInterface()


def on_activate(app):
    app.textik = "hm"
    id=app.get_application_id()
    parent=Gtk.ApplicationWindow(application=app)
    root_menuitem = Dbusmenu.Menuitem()
    app.server = Dbusmenu.Server(
            dbus_object='/SNIMenu', root_node=root_menuitem
        )
    for name in ["Settings", "Help", "About", "Quit"]:
        item = Dbusmenu.Menuitem()
        item.property_set("label", name)
        item.connect("item-activated", lambda action, target: print(action, target))
        root_menuitem.child_append(item)

app = Gtk.Application(application_id="one.jiri.easydict")
app.connect("activate", on_activate)
# this is server part
async def startup() -> None:
    """Perform async startup actions"""
    #await request_default_bus_name_async(f'one.jiri.easydict', queue=True)
    # Export the object to dbus
    #sn_item_interface.export_to_dbus('/StatusNotifierItem')


# this is client part


async def register_sn_item() -> None:
    proxy = sn_watcher.new_proxy(service_name="org.kde.StatusNotifierWatcher",object_path='/StatusNotifierWatcher')
    await proxy.register_status_notifier_item('/SNIMenu')
    sn_item_interface.export_to_dbus('/SNIMenu')
    # check if item is really registred
    print(await proxy.registered_status_notifier_items)

def run_event_loop(q):
    """Run asyncio event loop in another Thread"""
    sdbus_loop = asyncio.new_event_loop()
    q.put(sdbus_loop)
    sdbus_loop.run_forever()

def main(args=argv[1:]):
    import hupper
    # start_reloader will only return in a monitored subprocess
    reloader = hupper.start_reloader("sdbus_server_and_client.main")
    # monitor an extra file
    # reloader.watch_files(['foo.ini'])
    q = Queue()
    thread = Thread(target=run_event_loop, args=(q,))
    thread.daemon = True
    thread.start()
    sdbus_loop = q.get()

    asyncio.run_coroutine_threadsafe(startup(), sdbus_loop) # run of server/service part
    asyncio.run_coroutine_threadsafe(register_sn_item(), sdbus_loop) # run of client part
    # loop = asyncio.new_event_loop()
    # task = loop.create_task(startup()) # run (as task) client part
    # task = loop.create_task(register_sn_item()) # run (as task) client part
    # loop.run_forever()
    app.run()


if __name__ == "__main__":
    main()
