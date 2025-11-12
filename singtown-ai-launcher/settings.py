import os
import json
from pathlib import Path
import tomllib

appdata = Path(os.environ["APPDATA"])
setting_path = appdata / "SingtownAI" / "settings.json"
setting_path.parent.mkdir(parents=True, exist_ok=True)
if not setting_path.exists():
    setting_path.write_text("{}", encoding="utf-8")
setting_dict = json.loads(setting_path.read_text(encoding="utf-8"))


def get_appdir() -> Path:
    return appdata / "SingtownAI"


def get_setting(key, default=None):
    return setting_dict.get(key, default)


def set_setting(key, value):
    setting_dict[key] = value
    with setting_path.open("w", encoding="utf-8") as f:
        json.dump(setting_dict, f, ensure_ascii=False, indent=4)


def get_share_enabled():
    return get_setting("share_enabled", False)


def set_share_enabled(value: bool):
    set_setting("share_enabled", value)


def get_auto_update_enabled():
    return get_setting("auto_update_enabled", True)


def set_auto_update_enabled(value: bool):
    set_setting("auto_update_enabled", value)


def get_port():
    return get_setting("port", 34527)


def set_port(value: int):
    set_setting("port", value)


def get_download_source():
    return get_setting("download_source", "china")


def set_download_source(value: str):
    set_setting("download_source", value)


def get_registry():
    source = get_download_source()
    if source == "china":
        return "registry.cn-shenzhen.aliyuncs.com/singtown-ai/"
    else:
        return "ghcr.io/singtown-ai/"


def get_version():
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        data = tomllib.load(f)
    return data["project"]["version"]
