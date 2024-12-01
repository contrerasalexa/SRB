from PyQt6.QtWidgets import QApplication
from src.views.login import Login


class App:
    def __init__(self):
        self.app = QApplication([])
        self.login = Login()
        self.app.exec()


if __name__ == "__main__":
    app = App()
