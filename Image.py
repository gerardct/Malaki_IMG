import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QPushButton, \
    QStackedWidget
from PyQt5.QtGui import QPixmap, QColor, QPalette
from PyQt5.QtCore import Qt
from PIL import Image


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
    # Resize the image to fit within the max_width and max_height while maintaining the aspect ratio
    width, height = img.size
    aspect_ratio = width / height
    if width > height:
        new_width = max_width
        new_height = int(max_width / aspect_ratio)
    else:
        new_height = max_height
        new_width = int(max_height * aspect_ratio)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return img


class MoodApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mood Selector")
        self.setGeometry(100, 100, 600, 700)

        # Set background color
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(240, 240, 240))  # Light gray background
        self.setPalette(palette)

        self.stacked_widget = QStackedWidget()
        self.setLayout(QVBoxLayout())

        # Create the Question Page
        self.question_page = QWidget()
        self.question_layout = QVBoxLayout()

        # Add the question label at the top
        self.question_label = QLabel("Quin és el teu mood malaki d'avui?", self)
        self.question_label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center; color: #2d2d2d;")
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_layout.addWidget(self.question_label)

        # Create a container layout for the radio buttons (below the question)
        self.radio_layout = QVBoxLayout()
        self.radio_buttons = {}

        for mood in images.keys():
            radio_button = QRadioButton(mood)
            radio_button.setStyleSheet("font-size: 20px; padding: 12px; margin: 10px; color: #2d2d2d;")
            radio_button.clicked.connect(self.display_image)
            self.radio_buttons[mood] = radio_button
            self.radio_layout.addWidget(radio_button, alignment=Qt.AlignCenter)

        self.question_layout.addLayout(self.radio_layout)

        self.question_page.setLayout(self.question_layout)

        # Create the Result Page (for displaying the image)
        self.result_page = QWidget()
        self.result_layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.image_label.setStyleSheet("border: 5px solid #2d2d2d; border-radius: 10px;")
        self.result_layout.addWidget(self.image_label)

        self.error_label = QLabel(self)
        self.error_label.setStyleSheet("color: red; font-size: 14px; text-align: center;")
        self.result_layout.addWidget(self.error_label)

        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet("""
            font-size: 18px; padding: 10px 20px; background-color: #4CAF50; color: white;
            border-radius: 5px; border: none; margin-top: 20px; 
            text-align: center;
        """)
        self.back_button.clicked.connect(self.show_question_page)
        self.result_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        self.result_page.setLayout(self.result_layout)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.question_page)
        self.stacked_widget.addWidget(self.result_page)

        self.layout().addWidget(self.stacked_widget)

    def display_image(self):
        selected_mood = None
        for mood, radio_button in self.radio_buttons.items():
            if radio_button.isChecked():
                selected_mood = mood
                break

        if selected_mood and selected_mood in images:
            image_path = images[selected_mood]
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = resize_image_to_max(img, 600, 600)  # Resize image
                img_qpixmap = QPixmap(image_path)
                self.image_label.setPixmap(img_qpixmap.scaled(600, 600, Qt.KeepAspectRatio))
                self.error_label.setText("")  # Clear any error messages
                self.stacked_widget.setCurrentIndex(1)  # Switch to the result page
            else:
                self.error_label.setText("Image file not found!")
        else:
            self.error_label.setText("Invalid selection!")

    def show_question_page(self):
        self.stacked_widget.setCurrentIndex(0)  # Switch back to the question page


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MoodApp()
    window.show()
    sys.exit(app.exec_())
