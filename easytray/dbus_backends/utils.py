from pathlib import Path
from os import environ
from mimetypes import guess_type
from shutil import copy2
from subprocess import run


class IconInstallationException(Exception):
    """Exception raised for errors catched during the 'xdg-icon-resource install' call.

    Attributes:
        icon -- the icon we tried to install
    """

    def __init__(self, icon_path, problem_description=None):
        icon_path = icon_path
        self.message = f"Intalation of icon with path {icon_path} was not successful."
        if problem_description:
            self.message += f"\n\n{problem_description}"
        super().__init__(self.message)


def get_xdg_data_home() -> Path:
    xdg_data_home_str = environ.get("XDG_DATA_HOME")
    if xdg_data_home_str:
        xdg_data_home = Path(xdg_data_home_str)
    else:
        xdg_data_home = Path.home() / ".local/share"

    return xdg_data_home


def run_xdg_icon_resource(
    icon_type: str, data_home: Path, icon_path: Path, icon_size: int | None
):
    # if the icon type is svg, then we can not run xdg-icon-resource and we will only simulate its functions
    if icon_type == "image/svg+xml":
        dst_dir = data_home / "icons/hicolor/scalable/apps"
        dst_dir.mkdir(exist_ok=True, parents=True)
        icon_new_path = Path(copy2(icon_path, dst_dir)).parent
        assert dst_dir == icon_new_path
        # try to update icon cache for GTK and Plasma apps
        process = run(
            ['gtk-update-icon-cache && rm "${HOME}/.cache/icon-cache.kcache"'],
            shell=True,
        )

    elif icon_type == "image/png":
        if icon_size is None:
            raise IconInstallationException(
                icon_path, "If you provide PNG icon, you have to provide icon size too."
            )
        icon_file_path = str(icon_path.resolve())
        process = run(
            [
                "xdg-icon-resource",
                "install",
                "--novendor",
                "--size",
                str(icon_size),
                icon_file_path,
            ]
        )
        if process.returncode != 0:
            if process.stdout:
                print(f"[stdout]\n{process.stdout.decode()}")
            if process.stderr:
                print(f"[stderr]\n{process.stderr.decode()}")
            raise IconInstallationException(icon_path)
        icon_new_path = data_home / f"icons/hicolor/{icon_size}x{icon_size}/apps"
    # at the end check, if the icon really exists
    if not icon_new_path.exists():
        raise IconInstallationException(icon_path)
    return str(icon_new_path)


def install_icon_to_xdg_data_home(icon_path: Path, icon_size: int | None = None):
    """This function will call xdg-icon-resource if the input is PNG image or copy SVG image do its destination and try to refresh GTK icon cache."""
    if not icon_path.exists():
        raise FileNotFoundError("Icon doesn't exists!")

    # check if icon isn't installed already
    icon_type = guess_type(icon_path.name)[0]
    data_home = get_xdg_data_home()

    if icon_type == "image/svg+xml":
        dst_dir = data_home / "icons/hicolor/scalable/apps"
    elif icon_type == "image/png":
        dst_dir = data_home / f"icons/hicolor/{icon_size}x{icon_size}/apps"
    else:
        raise IconInstallationException(
            icon_path=icon_path,
            problem_description="Only PNG and SVG formats are supported.",
        )

    if (dst_dir / icon_path.name).exists():
        # if icon in system exists already, then return its path (parent dir) directly
        return str(dst_dir)
    else:
        # if icon is not presented on system, then install it first
        return run_xdg_icon_resource(icon_type, data_home, icon_path, icon_size)
