import tkinter as tk
from tkinter import ttk
from multiprocessing import Process


def run_progress(title, description):
    root = tk.Tk()

    width = 300
    height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    root.geometry(f"{width}x{height}+{x}+{y}")
    root.title("SingTown AI")
    root.iconbitmap("assets/fav.ico")
    root.resizable(False, False)

    title_element = tk.Label(root, text=title, font=("SimHei", 16, "bold"))
    title_element.pack(pady=10)

    description_element = tk.Label(root, text=description, font=("Helvetica", 10))
    description_element.pack(pady=10)

    bar = ttk.Progressbar(root, orient="horizontal", length=250, mode="indeterminate")
    bar.pack(pady=10)
    bar.start()

    root.mainloop()


class Loading:
    def __init__(self, title, description=""):
        self.title = title
        self.description = description
        self.process = None

    def __enter__(self):
        if self.process is None or not self.process.is_alive():
            self.process = Process(
                target=run_progress, args=(self.title, self.description)
            )
            self.process.start()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.process is not None:
            self.process.terminate()
            self.process.join()


if __name__ == "__main__":
    with Loading("Loading...", "Please wait while loading."):
        import time

        time.sleep(5)
