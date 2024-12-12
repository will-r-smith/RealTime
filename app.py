import tkinter as tk
from tkinter import ttk
import os 
import sys

from styles import *
from init import initialise_app


class App:
    def __init__(self, root):
        # Initialize the main Tkinter window
        self.root = root
        self.root.title("LyoSync")
        self.root.overrideredirect(False)
        self.root.geometry("1000x800")  # Set default window size

        style = get_style(self.root, "awdark")
    
        if hasattr(sys, "_MEIPASS"):
            icon_path = os.path.join(sys._MEIPASS, "icon.ico")
        else:
            icon_path = "icon.ico"  # Path when running locally
        self.root.iconbitmap(icon_path)


        # Add a style object for consistent theming
        #self.style = get_style(self.root, "awdark")

        initialise_app(self.root)

    def run(self):
        """Run the main application loop."""
        self.root.mainloop()

