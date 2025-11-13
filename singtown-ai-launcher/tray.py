import webbrowser
import socket
from tkinter import messagebox
import threading

from pystray import Icon, Menu, MenuItem
from PIL import Image

import page
import settings
import modal
import wsl
from translations import translate as _


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def on_open(icon, item):
    page.open_window(f"http://localhost:{settings.get_port()}/")


def on_update(icon, item):
    with modal.Loading(
        _("Updating SingTown AI..."),
        _("This may take a few moments, please wait..."),
    ):
        wsl.compose_down()
        wsl.compose_pull()
        wsl.compose_up()

    threading.Thread(
        target=messagebox.showinfo,
        args=("SingTown AI", _("Update completed successfully.")),
    ).start()


def on_share_open(icon, item):
    webbrowser.open(f"http://{get_local_ip()}:{settings.get_port()}/")


def on_share_enable(icon, item):
    if settings.get_share_enabled():
        return
    wsl.portproxy_stop()
    wsl.portproxy_start()
    settings.set_share_enabled(True)


def on_share_disable(icon, item):
    if not settings.get_share_enabled():
        return
    wsl.portproxy_stop()
    settings.set_share_enabled(False)


def on_auto_update_enable(icon, item):
    if settings.get_auto_update_enabled():
        return
    settings.set_auto_update_enabled(True)


def on_auto_update_disable(icon, item):
    if not settings.get_auto_update_enabled():
        return
    settings.set_auto_update_enabled(False)


def on_use_china_source(icon, item):
    if settings.get_download_source() == "china":
        return
    settings.set_download_source("china")


def on_use_github_source(icon, item):
    if settings.get_download_source() == "github":
        return
    settings.set_download_source("github")


def run():
    img = Image.open("assets/fav.ico")

    menu = Menu(
        MenuItem(_("Open"), on_open, default=True),
        Menu.SEPARATOR,
        MenuItem(
            _("Open Share URL"),
            on_share_open,
            enabled=lambda item: settings.get_share_enabled(),
        ),
        MenuItem(
            _("Share Enable"),
            on_share_enable,
            checked=lambda item: settings.get_share_enabled(),
        ),
        MenuItem(
            _("Share Disable"),
            on_share_disable,
            checked=lambda item: not settings.get_share_enabled(),
        ),
        Menu.SEPARATOR,
        MenuItem(
            _("Auto Update Enable"),
            on_auto_update_enable,
            checked=lambda item: settings.get_auto_update_enabled(),
        ),
        MenuItem(
            _("Auto Update Disable"),
            on_auto_update_disable,
            checked=lambda item: not settings.get_auto_update_enabled(),
        ),
        MenuItem(_("Update Now"), on_update),
        Menu.SEPARATOR,
        MenuItem(
            _("Use China Download Source"),
            on_use_china_source,
            checked=lambda item: settings.get_download_source() == "china",
        ),
        MenuItem(
            _("Use GitHub Download Source"),
            on_use_github_source,
            checked=lambda item: settings.get_download_source() == "github",
        ),
        Menu.SEPARATOR,
        MenuItem(_("Exit"), lambda icon, item: icon.stop()),
    )

    icon = Icon("SingTown AI", img, menu=menu)
    icon.run()


if __name__ == "__main__":
    run()
