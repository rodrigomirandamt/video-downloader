import os
import sys
from pathlib import Path

def setup_environment():
    """
    Ensures the application can find necessary external tools (like ffmpeg)
    and its own modules, especially when bundled as an app.
    """
    # Add Homebrew and local bin paths for tools like ffmpeg
    homebrew_paths = ["/opt/homebrew/bin", "/usr/local/bin"]
    current_path = os.environ.get("PATH", "")
    for p in homebrew_paths:
        if p not in current_path:
            current_path += os.pathsep + p
    os.environ["PATH"] = current_path

    # If running as a bundled app, the current directory needs to be set right
    if getattr(sys, 'frozen', False):
        app_path = Path(sys.executable).parent
        os.chdir(app_path)

def main():
    """The main entry point for the MediaSlayer application."""
    setup_environment()
    
    try:
        from mediaslayer.app import Application
        app = Application()
        
        # Set the window close protocol
        app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        app.run()

    except Exception as e:
        # Basic fallback error UI if Tkinter is available
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "MediaSlayer Fatal Error",
                f"An unexpected error occurred and MediaSlayer must close.\n\n"
                f"Error: {e}"
            )
            root.destroy()
        except ImportError:
            # If tkinter itself fails, just print to stderr
            print(f"A fatal error occurred: {e}", file=sys.stderr)
        
        sys.exit(1)

if __name__ == "__main__":
    main()



