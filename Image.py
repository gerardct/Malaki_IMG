import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

# Helper function to get the resource path (works with PyInstaller)
def resource_path(relative_path):
    """ Get the absolute path to a resource. Works for dev and for PyInstaller. """
    try:
        # PyInstaller creates a temp folder and stores files there
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
images = {
    "Option 1": resource_path("Fotos/709C34D4-9F44-498B-989E-6EF514B05C43.JPEG"),
    "Option 2": resource_path("Fotos/709C34D4-9F44-498B-989E-6EF514B05C43.JPEG")
    }

# Create a dictionary of options and their corresponding image paths

# Function to display the selected image
def display_image(selection):
    if selection in images:
        image_path = images[selection]
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize((400, 400))  # Resize for display
            img_tk = ImageTk.PhotoImage(img)

            # Update the image label
            image_label.config(image=img_tk)
            image_label.image = img_tk
            image_label.pack()
        else:
            error_label.config(text="Image file not found!")
    else:
        error_label.config(text="Invalid selection!")

# Initialize the main window
root = tk.Tk()
root.title("Image Selector")

# Dropdown menu for selection
selection_var = tk.StringVar()
selection_var.set("Select an option")

dropdown = ttk.OptionMenu(root, selection_var, *images.keys(), command=display_image)
dropdown.pack(pady=10)

# Label to display the image
image_label = tk.Label(root)
image_label.pack()

# Label to display error messages
error_label = tk.Label(root, fg="red")
error_label.pack()

# Run the application
root.mainloop()
