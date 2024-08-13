import sys
import random
import string
import json
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QLineEdit
from PyQt6.QtCore import Qt

# Файл для хранения настроек
settings_file = "settings.json"

def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, "r") as file:
            return json.load(file)
    return {"password_length": 16}  # Значение по умолчанию

def save_settings(settings):
    with open(settings_file, "w") as file:
        json.dump(settings, file)

class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PasGen")
        self.setFixedSize(555, 200)

        # Загрузка настроек
        self.settings = load_settings()
        initial_length = self.settings["password_length"]

        self.layout = QVBoxLayout()

        self.label = QLabel("The initial password length is 16 characters to change, move the slider below")
        self.layout.addWidget(self.label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(16)
        self.slider.setMaximum(64)
        self.slider.setValue(initial_length)  # Установка начального значения из настроек
        self.slider.valueChanged.connect(self.update_password_length)
        self.layout.addWidget(self.slider)

        self.password_field = QLineEdit()
        self.password_field.setReadOnly(True)
        self.password_field.setText("Your password will be here")
        self.layout.addWidget(self.password_field)

        self.generate_button = QPushButton("Generate a password")
        self.generate_button.clicked.connect(self.generate_password)
        self.layout.addWidget(self.generate_button)

        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.layout.addWidget(self.copy_button)

        self.setLayout(self.layout)

        # Обновление метки с длиной пароля
        self.update_password_length()

    def update_password_length(self):
        length = self.slider.value()
        self.label.setText(f"Password length: {length}")

        # Сохранение настроек при изменении длины пароля
        self.settings["password_length"] = length
        save_settings(self.settings)

    def generate_password(self):
        length = self.slider.value()
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_field.setText(password)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_field.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec())
