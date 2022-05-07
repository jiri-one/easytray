# kstatusnotifier_sdbus

KStatusNotifier tray icon solution writen in Python with sdbus (library for D-Bus).

If you copy content of this repo and run `python sdbus_server_and_client.py` you should see small icon in your KDE Plasma Tray area. You can use scroll/wheel button on your mouse and see in terminal, that this is working and primary button is working too. You can implement this in your project, where you need tray icon, because other linux solutions are little bit strange .... All settings are in `StatusNotifierItem.py` file, there you can implement other functionality. More infos are on site: https://notmart.org/misc/statusnotifieritem/index.html (**that is the main link about KStatusNotifier**)

Other useful links:
- [Lennart Poettering is explainin dbus](https://web.archive.org/web/20200522193008/http://0pointer.net/blog/the-new-sd-bus-api-of-systemd.html)
- [KStatusNotifier implementation in C in GTK3](https://github.com/jjk-jacky/statusnotifier/blob/master/src/statusnotifier.c)
- [python-sdbus documentation](https://python-sdbus.readthedocs.io/en/latest/general.html)
- [AppIndicator/KStatusNotifierItem support for GNOME Shell](https://github.com/ubuntu/gnome-shell-extension-appindicator)
- [Introduction to D-Bus from Freedesktop.org](https://www.freedesktop.org/wiki/IntroductionToDBus/)
- [All about D-Bus from KDE with examples in C++](https://develop.kde.org/docs/use/d-bus/)
- [NOT ACTUAL, but maybe useful DBus tutorial with PyKDE4](https://techbase.kde.org/Languages/Python/PyKDE_DBus_Tutorial)

Notes:
- I generated file `StatusNotifierItem.py` with this command:
`python -m sdbus gen-from-file /usr/share/dbus-1/interfaces/kf5_org.kde.StatusNotifierItem.xml` you should have this file on same place, if you are using Arch Linux
- I generated file `StatusNotifierWatcher.py` directly from dbus with this command: `python -m sdbus gen-from-connection org.kde.StatusNotifierWatcher /StatusNotifierWatcher` but I could do that with command `python -m sdbus gen-from-file /usr/share/dbus-1/interfaces/kf5_org.kde.StatusNotifierWatcher.xml` (I have tried it with the same result)
- the XML files are on internet too: https://github.com/KDE/knotifications/blob/master/src/org.kde.StatusNotifierWatcher.xml and https://github.com/KDE/knotifications/blob/master/src/org.kde.StatusNotifierWatcher.xml
- For simple notification you can use https://github.com/KDE/knotifications/blob/master/src/org.freedesktop.Notifications.xml but sdbus it already has done and easier with this binds: https://github.com/python-sdbus/python-sdbus-notifications



## This repository and this text is more my notes and my "storage" the regular repository, but you can use it tut you can use it to relieve digging about KStatusNotifier, because here is working solution in Python.
