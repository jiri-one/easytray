# EasyTray

Many Linux users are still used to using the tray icon for some kinds of programs. KDE Plasma has supported tray icons practically since its inception, and the latest implementation that KDE has come up with is [KStatusNotifier](https://notmart.org/misc/statusnotifieritem/index.html). This solution is also programming language or library independent, as it is built entirely on top of DBUS. This allows you to use the tray icon in libraries and frameworks other than those associated with KDE/Qt.

So this repository contains an implementation of KStatusNotifier using the Python programming language and the Python library [dasbus](https://dasbus.readthedocs.io/en/latest/).
The repository also includes a sample/example of small [GTK/PyGObject](https://pygobject.readthedocs.io/en/latest/) application that implements the tray icon and KStatusNotifier, including the [menu](https://lazka.github.io/pgi-docs/#Dbusmenu-0.4).

**Note:** in the repository you will also find attempts to implement it in other DBUS libraries, namely [dbus-fast](https://dbus-fast.readthedocs.io/en/latest/) and also [sdbus](https://python-sdbus.readthedocs.io/en/latest/). In these libraries the **tray icon itself works perfectly**, but I have not yet managed to implement a menu for them, so the default implementation is dasbus, which is built on top of the GLib library, which is linked to the GTK library, and then in GTK applications you can simply use [Dbusmenu](https://lazka.github.io/pgi-docs/#Dbusmenu-0.4) for the menu.
