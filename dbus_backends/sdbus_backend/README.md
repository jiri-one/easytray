
sdbus has some helpers to create XML files:

- I generated file `StatusNotifierItem.py` with this command:
`python -m sdbus gen-from-file /usr/share/dbus-1/interfaces/kf5_org.kde.StatusNotifierItem.xml` you should have this file on same place, if you are using Arch Linux
- I generated file `StatusNotifierWatcher.py` directly from dbus with this command: `python -m sdbus gen-from-connection org.kde.StatusNotifierWatcher /StatusNotifierWatcher` but I could do that with command `python -m sdbus gen-from-file /usr/share/dbus-1/interfaces/kf5_org.kde.StatusNotifierWatcher.xml` (I have tried it with the same result)
- the XML files are on internet too: https://github.com/KDE/knotifications/blob/master/src/org.kde.StatusNotifierWatcher.xml and https://github.com/KDE/knotifications/blob/master/src/org.kde.StatusNotifierWatcher.xml
- For simple notification you can use https://github.com/KDE/knotifications/blob/master/src/org.freedesktop.Notifications.xml but sdbus it already has done and easier with this binds: https://github.com/python-sdbus/python-sdbus-notifications
