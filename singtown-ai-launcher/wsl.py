import subprocess
import settings


podman_service_process = None


def portproxy_start():
    subprocess.run(
        f"netsh interface portproxy add v4tov4 listenport={settings.get_port()} listenaddress=0.0.0.0 connectport={settings.get_port()} connectaddress=localhost",
        shell=True,
        check=True,
    )


def portproxy_stop():
    subprocess.run(
        f"netsh interface portproxy delete v4tov4 listenport={settings.get_port()} listenaddress=0.0.0.0",
        shell=True,
        check=False,
    )


def get_volume_dir() -> str:
    win_dir = settings.get_appdir() / "volume"
    result = subprocess.run(
        f"wsl -d SingTownAI wslpath '{str(win_dir)}'",
        shell=True,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def terminate():
    subprocess.run("wsl --terminate SingTownAI", shell=True, check=True)


def enable_cuda():
    subprocess.run(
        "wsl -d SingTownAI nvidia-ctk cdi generate --output=/var/run/cdi/nvidia.yaml",
        shell=True,
        check=True,
    )


def podman_service_stop():
    global podman_service_process
    if podman_service_process is not None:
        podman_service_process.terminate()
        podman_service_process.wait()
        podman_service_process = None


def podman_service_start():
    podman_service_stop()
    global podman_service_process
    podman_service_process = subprocess.Popen(
        "wsl -d SingTownAI podman system service --time=0", shell=True
    )


def compose_up():
    cmd = "wsl -d SingTownAI --cd /root"
    cmd += f" PORT={settings.get_port()}"
    cmd += f" REGISTRY={settings.get_registry()}"
    cmd += f" VOLUME_DIR={get_volume_dir()}"
    cmd += f" LAUNCHER_VERSION={settings.get_version()}"
    cmd += " podman-compose up -d --force-recreate"
    subprocess.run(cmd, shell=True, check=True)


def compose_down():
    cmd = "wsl -d SingTownAI --cd /root"
    cmd += f" PORT={settings.get_port()}"
    cmd += f" REGISTRY={settings.get_registry()}"
    cmd += f" VOLUME_DIR={get_volume_dir()}"
    cmd += f" LAUNCHER_VERSION={settings.get_version()}"
    cmd += " podman-compose down"
    subprocess.run(cmd, shell=True, check=False)


def compose_pull():
    cmd = "wsl -d SingTownAI --cd /root"
    cmd += f" PORT={settings.get_port()}"
    cmd += f" REGISTRY={settings.get_registry()}"
    cmd += f" VOLUME_DIR={get_volume_dir()}"
    cmd += f" LAUNCHER_VERSION={settings.get_version()}"
    cmd += " podman-compose pull"
    subprocess.run(cmd, shell=True, check=True)
