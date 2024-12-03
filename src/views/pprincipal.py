from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.views.renta import RentaDialog
from src.views.admin.table_users import UserTable


class Principal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/views/admin/pprincipal.ui", self)  # Carga el diseño de pprincipal.ui

        self.btnUsuarios.clicked.connect(self.administar_usuarios)
        self.btnRenta.clicked.connect(self.abrir_renta)
        self.btnSalir.clicked.connect(self.salir_programa)

    def abrir_renta(self):
        try:
            print("Abriendo formulario de renta...")
            renta_form = RentaDialog()  # Crear la ventana de renta
            renta_form.exec()  # Mostrar como diálogo modal
            print("Formulario de renta abierto correctamente.")
        except Exception as e:
            print(f"Error al abrir la ventana de renta: {e}")
    
    def administar_usuarios(self):
        self.close()
        self.table_users = UserTable(self)
        self.table_users.show()
        self.hide()     
    def salir_programa(self):
            """Cierra la aplicación."""
            print("Saliendo del programa...")
            self.close()  # Cierra la ventana principal
            sys.exit()  # Finaliza la aplicación

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Principal()  # Instanciar la clase Principal, no QMainWindow
    ventana.show()
    sys.exit(app.exec())
