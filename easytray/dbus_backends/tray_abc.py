from abc import ABC, abstractmethod


class Tray(ABC):
    @abstractmethod
    def create_tray_icon(self):
        """Mandatory method. This method will be calling on superior class to create tray icon."""
        pass
