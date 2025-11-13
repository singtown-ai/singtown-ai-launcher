import sys
from pathlib import Path
from tkinter import messagebox

from filelock import FileLock, Timeout

import settings
from translations import translate as _
import page
import modal
import wsl
import tray

lock = FileLock(Path(sys.executable).with_suffix(".singtown-ai-lock"))
tray_process = None

if __name__ == "__main__":
    try:
        with lock.acquire(timeout=0):
            try:
                with modal.Loading(
                    _("Preparing SingTown AI"),
                    _("This may take a few moments, please wait..."),
                ):
                    wsl.compose_down()
                    wsl.terminate()
                    wsl.enable_cuda()
                    wsl.podman_service_start()

                if settings.get_auto_update_enabled():
                    with modal.Loading(
                        _("Updating SingTown AI"),
                        _("This may take a few moments, please wait..."),
                    ):
                        wsl.compose_pull()

                with modal.Loading(
                    _("Launching SingTown AI"),
                    _("This may take a few moments, please wait..."),
                ):
                    wsl.compose_up()
                    page.open_window(f"http://localhost:{settings.get_port()}/")
                    if settings.get_share_enabled():
                        wsl.portproxy_stop()
                        wsl.portproxy_start()

                tray.run()

            except Exception as e:
                messagebox.showerror(_("Error in SingTown AI"), str(e))

            finally:
                with modal.Loading(
                    _("Shutting down SingTown AI"),
                    _("This may take a few moments, please wait..."),
                ):
                    if tray_process is not None:
                        tray_process.terminate()
                        tray_process.join()
                    page.close_window()
                    wsl.portproxy_stop()
                    wsl.compose_down()
                    wsl.podman_service_stop()
                    wsl.terminate()

    except Timeout:
        print("exit: another instance is running")
        sys.exit(1)
