import webview
from multiprocessing import Process

webview_process = None


def run_webview(url):
    screen = webview.screens[0]

    webview.create_window(
        "SingTown AI Standalone Edition",
        url,
        width=800,
        height=600,
        x=int((screen.width - 800) / 2),
        y=int((screen.height - 600) / 2),
    )
    webview.start()


def open_window(url):
    global webview_process
    if webview_process is None or not webview_process.is_alive():
        webview_process = Process(target=run_webview, args=(url,))
        webview_process.start()


def close_window():
    if webview_process is not None:
        webview_process.terminate()
        webview_process.join()


if __name__ == "__main__":
    import time

    open_window("https://www.google.com")
    time.sleep(10)
    close_window()
