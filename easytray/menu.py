import gi

gi.require_versions({"Dbusmenu": "0.4"})
from gi.repository import Dbusmenu
from dataclasses import dataclass
from typing import Callable


@dataclass
class EasyTrayMenu:
    menu_items: dict[str, Callable]
    dbus_path: str

    def create_dbus_menu(self):
        """Create Dbusmenu with calling instance of this class."""
        root_menuitem = Dbusmenu.Menuitem()
        self.server = Dbusmenu.Server(  # this has to be in self, part of GTK app or GTK object paired with GTK app
            dbus_object=self.dbus_path, root_node=root_menuitem
        )
        for name, callback in self.menu_items.items():
            item = Dbusmenu.Menuitem()
            item.property_set("label", name)
            item.connect("item-activated", callback)
            root_menuitem.child_append(item)
