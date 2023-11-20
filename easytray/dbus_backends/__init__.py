# internal imports
from .dasbus_backend import DasbusTray

# from dbusfast_backend import DbusFastTray
# from sdbus_backend import SdbusTray

KNOWN_BACKENDS: dict = {
    "dasbus": DasbusTray,
    # "dbusfast": DbusFastTray,
    # "sdbus": SdbusTray,
}


def get_dbus_backend(backend):
    return KNOWN_BACKENDS.get(backend, None)


__all__ = ["get_dbus_backend"]
