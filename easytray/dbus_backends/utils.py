from pathlib import Path
from os import environ
import asyncio
from mimetypes import guess_type


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


async def run_xdg_icon_resource(icon_path: Path, icon_size: int):
    icon_file_path = str(icon_path.resolve())
    process = await asyncio.create_subprocess_shell(
        f"xdg-icon-resource install --novendor --size {icon_size} {icon_file_path}"
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")
        raise IconInstallationException(icon_path)
    else:
        icon_type = guess_type(icon_path.name)[0]
        data_home = get_xdg_data_home()
        if icon_type == "image/svg+xml":
            icon_new_path = data_home / f"icons/hicolor/scalable/apps/{icon_path.name}"
        elif icon_type is not None and "image" in icon_type:
            icon_new_path = (
                data_home
                / f"icons/hicolor/{icon_size}x{icon_size}/apps/{icon_path.name}"
            )
        if not icon_new_path.exists():
            raise IconInstallationException(icon_path)
        return str(icon_new_path)


def install_icon_to_xdg_data_home(icon_path: Path, icon_size: int):
    """This function will call xdg-icon-resource asynchronously"""
    if not icon_path.exists():
        raise FileNotFoundError("Icon doesn't exists!")
    return asyncio.run(run_xdg_icon_resource(icon_path, icon_size))
