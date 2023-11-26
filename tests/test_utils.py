from PIL import Image

# pytest imports
import pytest

# internal imports
from easytray.dbus_backends.utils import install_icon_to_xdg_data_home


@pytest.fixture
def image_png(tmp_path):
    width = 100
    height = 100
    img_path = tmp_path / "image.png"
    img = Image.new(mode="RGB", size=(width, height), color="red")
    img.save(img_path, bitmap_format="png")
    return img_path


def test_install_icon_to_xdg_data_home_png(image_png):
    new_icon_path = install_icon_to_xdg_data_home(icon_path=image_png, icon_size=100)
