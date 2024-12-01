from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6 import uic

class Principal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/views/admin/pprincipal.ui", self)  # Carga el diseño de pprincipal.ui

        # Conectar botones a sus respectivas acciones
        self.btnUsuarios_2.clicked.connect(self.inicio)
        self.btnUsuarios.clicked.connect(self.usuarios)
        self.btnSalir.clicked.connect(self.cerrar_sesion)

    def usuarios(self):
        self.stackedWidget.setCurrentWidget(self.page_3)
    def inicio(self):
        """
        Cambia a la página de Usuarios en el QStackedWidget
        """
        self.stackedWidget.setCurrentWidget(self.page)  # Cambia a la página de Usuarios

    def cerrar_sesion(self):
        """
        Cierra la ventana principal y vuelve al login.
        """
        # Cerrar la ventana principal
        self.close()

        # Crear una nueva instancia de la ventana de login y mostrarla
        from src.views.login import Login
        self.login = Login()
        self.login.login.show()
