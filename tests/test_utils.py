from PIL import Image
from pathlib import Path

# pytest imports
import pytest

# internal imports
from easytray.dbus_backends import install_icon_to_xdg_data_home


SVG_IMAGE = """
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="800" height="800" baseProfile="full" viewBox="-21 -21 42 42">
  <defs>
    <radialGradient id="b" cx=".2" cy=".2" r=".5" fx=".2" fy=".2">
      <stop offset="0" stop-color="#fff" stop-opacity=".7"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="a" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="#ff0"/>
      <stop offset=".75" stop-color="#ff0"/>
      <stop offset=".95" stop-color="#ee0"/>
      <stop offset="1" stop-color="#e8e800"/>
    </radialGradient>
  </defs>
  <circle r="20" fill="url(#a)" stroke="#000" stroke-width=".15"/>
  <circle r="20" fill="url(#b)"/>
  <g id="c">
    <ellipse cx="-6" cy="-7" rx="2.5" ry="4"/>
    <path fill="none" stroke="#000" stroke-linecap="round" stroke-width=".5" d="M10.6 2.7a4 4 0 0 0 4 3"/>
  </g>
  <use xlink:href="#c" transform="scale(-1 1)"/>
  <path fill="none" stroke="#000" stroke-width=".75" d="M-12 5a13.5 13.5 0 0 0 24 0 13 13 0 0 1-24 0"/>
</svg>
"""


@pytest.fixture
def image_svg(tmp_path):
    img_path = tmp_path / "image.svg"
    img_path.write_text(SVG_IMAGE)
    return img_path


@pytest.fixture
def image_png(tmp_path):
    width = 100
    height = 100
    img_path = tmp_path / "image.png"
    img = Image.new(mode="RGB", size=(width, height), color="red")
    img.save(img_path, bitmap_format="png")
    return img_path


def test_install_icon_to_xdg_data_home_png(image_png):
    new_icon_path_str = install_icon_to_xdg_data_home(
        icon_path=image_png, icon_size=100
    )
    new_icon_path = Path(new_icon_path_str)
    assert new_icon_path.is_dir()


def test_install_icon_to_xdg_data_home_svg(image_svg):
    new_icon_path_str = install_icon_to_xdg_data_home(icon_path=image_svg)
    new_icon_path = Path(new_icon_path_str)
    assert new_icon_path.is_dir()
