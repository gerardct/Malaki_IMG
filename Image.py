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
        self.question_label.setStyleSheet("font-size: 60px; font-weight: bold; text-align: center; color: #2d2d2d;")
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_layout.addWidget(self.question_label)

        # Add an image under the question label
        self.image_label = QLabel(self)
        image_path = resource_path("Icona-removebg-preview.png")  # Provide the path to the image
        pixmap = QPixmap(image_path)

        # Resize image to fit within a suitable size (optional)
        pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)  # Adjust width and height as needed

        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)  # Center the image
        self.question_layout.addWidget(self.image_label)

        # Add the grid layout of radio buttons to the question layout
        self.question_page.setLayout(self.question_layout)

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

            # Custom styling to make the radio button a square with the mood text inside
            radio_button.setStyleSheet("""
                QRadioButton {
                    font-size: 20px;
                    color: #2d2d2d;
                    background-color: #e0e0e0;  /* Light background for the button */
                    border: 3px solid #2d2d2d;  /* Dark border for square shape */
                    border-radius: 10px;  /* Optional rounded corners */
                    padding: 10px;
                    width: 120px;
                    height: 120px;
                    text-align: center;
                    display: flex;
                    justify-content: center;  /* Horizontally center the text */
                    align-items: center;  /* Vertically center the text */
                }
                QRadioButton::indicator {
                    width: 0px;
                    height: 0px;
                }
                QRadioButton:checked {
                    background-color: #4CAF50;  /* Green when selected */
                    border-color: #388E3C;  /* Darker green when selected */
                }
            """)
            radio_button.setFixedSize(400, 100)  # Make the button square-shaped
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

        # Make the result page fill the entire screen
        self.setWindowState(self.windowState() | Qt.WindowMaximized)

        # Create a container layout for the content of the result page
        self.result_content_layout = QVBoxLayout()

        # Image label setup: Make it bigger and ensure image fits
        self.image_label = QLabel(self)
        self.image_label.setStyleSheet("border: 5px solid #2d2d2d; border-radius: 10px;")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.result_content_layout.addWidget(self.image_label)

        # Title for the fact
        self.fact_title_label = QLabel("Factou random per la cara :)", self)
        self.fact_title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #2d2d2d; margin-top: 20px;")
        self.fact_title_label.setAlignment(Qt.AlignCenter)
        self.result_content_layout.addWidget(self.fact_title_label)

        # Label for the fact text: Centered horizontally and increased size
        self.fact_label = QLabel(self)
        self.fact_label.setStyleSheet("font-size: 24px; color: #2d2d2d; padding: 10px;")
        self.fact_label.setWordWrap(True)  # Enable word wrapping
        self.fact_label.setAlignment(Qt.AlignCenter)  # Horizontally centered text
        self.result_content_layout.addWidget(self.fact_label)

        # Error message label
        self.error_label = QLabel(self)
        self.error_label.setStyleSheet("color: red; font-size: 14px; text-align: center;")
        self.result_content_layout.addWidget(self.error_label)

        # Back button
        self.back_button = QPushButton("<-- Tria un altre mood")
        self.back_button.setStyleSheet(""" 
            font-size: 20px; padding: 15px 30px; background-color: #4CAF50; color: white;
            border-radius: 5px; border: none; margin-top: 20px; 
            text-align: center;
        """)
        self.back_button.clicked.connect(self.show_question_page)
        self.result_content_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        # Add the content layout to the main result layout
        self.result_layout.addLayout(self.result_content_layout)

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
                # Open and resize the image
                img = Image.open(image_path)
                img = resize_image_to_max(img, 800, 800)  # Make the image bigger

                # Convert the PIL image to QPixmap
                img_qpixmap = QPixmap(image_path)

                # Set the image to the label, without scaling it down for the border
                self.image_label.setPixmap(img_qpixmap.scaled(800, 800, Qt.KeepAspectRatio))

                # Clear any error messages
                self.error_label.setText("")

                # Get random fact and translate it to Spanish
                fact = get_random_fact()

                # Set the fact label text (no need to set width now)
                self.fact_label.setText(fact)

                # Apply the border separately without affecting the image size
                self.image_label.setStyleSheet(
                    "border: 10px solid #2d2d2d; border-radius: 10px;")  # Make border slightly thicker

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
