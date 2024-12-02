from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
from src.views.admin.table_users import UserTable

class Principal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/views/admin/pprincipal.ui", self)  # Carga el diseño de pprincipal.ui

        # Asegúrate de conectar el botón después de cargar el diseño
        self.btnSalir.clicked.connect(self.cerrar_sesion)
        self.btnUsuarios.clicked.connect(self.administar_usuarios)

    def cerrar_sesion(self):
        print("El botón SALIR fue presionado.")  # Debug
        self.close()

        # Crear una nueva instancia de la ventana de login y mostrarla
        from src.views.login import Login
        self.login = Login()
        self.login.login.show()

    def administar_usuarios(self):
        self.close()
        self.table_users = UserTable(self)
        self.table_users.show()
        self.hide()     

