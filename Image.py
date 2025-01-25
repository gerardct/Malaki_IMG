import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QRadioButton, QPushButton, QStackedWidget
from PyQt5.QtGui import QPixmap, QColor, QPalette
from PyQt5.QtCore import Qt
from PIL import Image
from googletrans import Translator


# Helper function to get the resource path (works with PyInstaller)
def resource_path(relative_path):
    """ Get the absolute path to a resource. Works for dev and for PyInstaller. """
    try:
        # PyInstaller creates a temp folder and stores files there
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Dynamically load all image filenames from the "Fotos" directory
image_folder = resource_path("Fotos")
images = {}

for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.jpeg', '.jpg', '.png', '.gif')):
        # Use the image filename (without extension) as the radio button label
        mood_name = os.path.splitext(filename)[0]
        images[mood_name] = resource_path(f"Fotos/{filename}")


# Function to call the Free API to get a random fact
def get_random_fact():
    try:
        url = "https://uselessfacts.jsph.pl/random.json?language=en"  # Get the fact in English
        response = requests.get(url)

        if response.status_code == 200:
            response_data = response.json()
            fact = response_data['text']

            # Translate the fact to Spanish
            translator = Translator()
            fact_in_spanish = translator.translate(fact, src='en', dest='es').text

            return fact_in_spanish
        else:
            return "Could not retrieve fact at this moment."
    except Exception as e:
        return f"Error: {str(e)}"


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

        self.setWindowTitle("Naiarotis APP")
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
        self.radio_layout = QGridLayout()  # Use QGridLayout instead of QVBoxLayout
        self.radio_buttons = {}

        # Number of columns for the grid layout (you can adjust this number to fit your needs)
        columns = 3  # For example, this will try to create 3 columns

        # Create radio buttons for each mood and add them to the grid layout
        row = 0
        col = 0
        for mood in images.keys():
            radio_button = QRadioButton(mood)
            radio_button.setStyleSheet("font-size: 20px; padding: 12px; margin: 10px; color: #2d2d2d;")
            radio_button.clicked.connect(self.display_image)
            self.radio_buttons[mood] = radio_button

            # Add the radio button to the grid at the appropriate row and column
            self.radio_layout.addWidget(radio_button, row, col)

            # Move to the next column
            col += 1
            # If we've reached the max number of columns, move to the next row
            if col >= columns:
                col = 0
                row += 1

        # Add the grid layout of radio buttons to the question layout
        self.question_layout.addLayout(self.radio_layout)

        self.question_page.setLayout(self.question_layout)

        # Create the Result Page (for displaying the image)
        self.result_page = QWidget()
        self.result_layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.image_label.setStyleSheet("border: 5px solid #2d2d2d; border-radius: 10px;")
        self.result_layout.addWidget(self.image_label)

        # Add a title for the fact
        self.fact_title_label = QLabel("Factou random per la cara :)", self)
        self.fact_title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2d2d2d; margin-top: 20px;")
        self.result_layout.addWidget(self.fact_title_label)

        # Add a label for the fact
        self.fact_label = QLabel(self)
        self.fact_label.setStyleSheet("font-size: 18px; color: #2d2d2d; padding: 10px;")
        self.fact_label.setWordWrap(True)  # Enable word wrapping
        self.result_layout.addWidget(self.fact_label)

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

                # Adjust for the border by reducing the size slightly
                img_qpixmap = QPixmap(image_path)
                border_thickness = 5  # Border width (as per the style)
                self.image_label.setPixmap(img_qpixmap.scaled(600 - 2 * border_thickness, 600 - 2 * border_thickness, Qt.KeepAspectRatio))
                self.error_label.setText("")  # Clear any error messages

                # Get random fact and translate it to Spanish
                fact = get_random_fact()

                # Set the fact label text (no need to set width now)
                self.fact_label.setText(fact)

                # The label will adjust its width automatically, but we ensure it doesn't stretch beyond image width
                self.fact_label.setFixedWidth(600 - 2 * border_thickness)

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
