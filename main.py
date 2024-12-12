import os
import sys
import tkinter as tk

# Ensure the src directory is in the import path
SRC_DIR = os.path.join(os.path.dirname(__file__), "src")
sys.path.insert(0, SRC_DIR)
# Ensure the app is not hosted on the 5000 locuual port
os.environ["FLASK_RUN_PORT"] = "5001"

root = tk.Tk()

from app import App  # Import the main application class


if __name__ == "__main__":
    # Start the application
    
    app = App(root)
    app.run()

