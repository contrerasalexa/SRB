from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6 import uic

class Principal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/views/admin/pprincipal.ui", self)  # Carga el diseño de pprincipal.ui

        # Asegúrate de conectar el botón después de cargar el diseño
        self.btnSalir.clicked.connect(self.cerrar_sesion)

    def cerrar_sesion(self):
        print("El botón SALIR fue presionado.")  # Debug
        self.close()

        # Crear una nueva instancia de la ventana de login y mostrarla
        from src.views.login import Login
        self.login = Login()
        self.login.login.show()


