from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from src.database.connection import DBConnection
import pymysql


class ClienteDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/views/cliente.ui", self)
        self.db_connection = DBConnection()

        # Conectar botones
        self.btnGuardarCliente.clicked.connect(self.guardar_cliente)
        self.btnCancelarCliente.clicked.connect(self.cancelar)

    def guardar_cliente(self):
        """Guarda un nuevo cliente en la base de datos."""
        try:
            # Obtener datos del formulario
            nombre = self.lineNombre.text().strip()
            apellido_paterno = self.lineApellidoPaterno.text().strip()
            email = self.lineEmail.text().strip()

            # Validar datos
            if not nombre or not apellido_paterno or not email:
                QMessageBox.warning(self, "Advertencia", "Nombre, apellido paterno y email son obligatorios.")
                return

            conn = self.db_connection.connection()
            if conn is None:
                QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos.")
                return

            cursor = conn.cursor()

            # Insertar cliente en la base de datos
            query = """
                INSERT INTO clientes (nombre, apellido_paterno, email, estatus)
                VALUES (%s, %s, %s, '1')
            """
            cursor.execute(query, (nombre, apellido_paterno, email))
            conn.commit()

            QMessageBox.information(self, "Éxito", "El cliente se ha registrado correctamente.")
            self.close()

            cursor.close()
            self.db_connection.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar el cliente: {e}")

    def cancelar(self):
        """Cierra el diálogo sin realizar ninguna acción."""
        self.close()
