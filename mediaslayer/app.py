import tkinter as tk
from .ui.main_window import MainWindow

class Application:
    """The main application class that orchestrates the GUI."""

    def __init__(self):
        self.root = tk.Tk()
        self.main_window = MainWindow(self.root)

    def run(self):
        """Starts the Tkinter main event loop."""
        self.root.mainloop()

    def on_closing(self):
        """Handles the window closing event."""
        # In the future, we can add cleanup logic here if needed
        self.root.quit()
        self.root.destroy()



