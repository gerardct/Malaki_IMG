import tkinter as tk
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

# Create a dictionary of options and their corresponding image paths
images = {
    "Happy": resource_path("Fotos/709C34D4-9F44-498B-989E-6EF514B05C43.JPEG"),
    "Sad": resource_path("Fotos/709C34D4-9F44-498B-989E-6EF514B05C43.JPEG"),
    "Excited": resource_path("Fotos/709C34D4-9F44-498B-989E-6EF514B05C43.JPEG"),
}


def resize_image_to_max(img, max_width, max_height):
    # Get the current size of the image
    width, height = img.size

    # Calculate the ratio of the dimensions
    aspect_ratio = width / height

    # Determine new width and height that maintain the aspect ratio
    if width > height:
        # If the image is wider than tall, resize based on max_width
        new_width = max_width
        new_height = int(max_width / aspect_ratio)
    else:
        # If the image is taller than wide, resize based on max_height
        new_height = max_height
        new_width = int(max_height * aspect_ratio)

    # Resize the image with the new dimensions
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    return img


# Function to display the selected image
def display_image():
    selection = selection_var.get()
    if selection in images:
        image_path = images[selection]
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img = resize_image_to_max(img, 600, 600) # Resize for display
            img_tk = ImageTk.PhotoImage(img)

            # Update the image label
            image_label.config(image=img_tk)
            image_label.image = img_tk
            error_label.config(text="")  # Clear any error messages
        else:
            error_label.config(text="Image file not found!")
    else:
        error_label.config(text="Invalid selection!")

# Initialize the main window
root = tk.Tk()
root.title("Mood Selector")

# Add a question label
question_label = tk.Label(root, text="Quin és el teu mood d'avui?", font=("Arial", 14))
question_label.pack(pady=10)

# Selection variable for the radiobuttons
selection_var = tk.StringVar()
selection_var.set(None)  # Default is no selection

# Create radiobuttons for each mood
for mood in images.keys():
    rb = tk.Radiobutton(
        root,
        text=mood,
        variable=selection_var,
        value=mood,
        command=display_image,
        font=("Arial", 12)
    )
    rb.pack(anchor="w", padx=20)

# Label to display the image
image_label = tk.Label(root)
image_label.pack(pady=10)

# Label to display error messages
error_label = tk.Label(root, fg="red", font=("Arial", 10))
error_label.pack(pady=5)

# Run the application
root.mainloop()
