import locale

local, page = locale.getdefaultlocale()

tr = {
    "en": {
        "Open": "Open",
        "Exit": "Exit",
        "Auto Update Enable": "Auto Update Enable",
        "Auto Update Disable": "Auto Update Disable",
        "Update Now": "Update Now",
        "Open Share URL": "Open Share URL",
        "Share Enable": "Share Enable",
        "Share Disable": "Share Disable",
        "Share is not enabled.": "Share is not enabled.",
        "Update completed successfully.": "Update completed successfully.",
        "Use China Download Source": "Use China Download Source",
        "Use GitHub Download Source": "Use GitHub Download Source",
        "Updating SingTown AI": "Updating SingTown AI",
        "Preparing SingTown AI": "Preparing SingTown AI",
        "Launching SingTown AI": "Launching SingTown AI",
        "Shutting down SingTown AI": "Shutting down SingTown AI",
        "This may take a few moments, please wait...": "This may take a few moments, please wait...",
    },
    "zh_CN": {
        "Open": "打开",
        "Exit": "退出",
        "Auto Update Enable": "启用自动更新",
        "Auto Update Disable": "禁用自动更新",
        "Update Now": "立即更新",
        "Open Share URL": "打开共享链接",
        "Share Enable": "启用共享",
        "Share Disable": "禁用共享",
        "Share is not enabled.": "共享未启用。",
        "Update completed successfully.": "升级完成。",
        "Use China Download Source": "使用中国下载源",
        "Use GitHub Download Source": "使用 GitHub 下载源",
        "Updating SingTown AI": "正在更新 SingTown AI",
        "Preparing SingTown AI": "正在准备 SingTown AI",
        "Launching SingTown AI": "正在启动 SingTown AI",
        "Shutting down SingTown AI": "正在关闭 SingTown AI...",
        "This may take a few moments, please wait...": "这可能需要一点时间，请稍候...",
    },
}

fallback = tr["en"]
lang = tr.get(local, fallback)


def translate(message: str):
    result = lang.get(message, None)
    if result:
        return result
    return fallback.get(message, message)
