import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QWidget, QHBoxLayout, QDialog
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt
import sqlite3

# Configuración de la base de datos
DB_NAME = "clientes.db"

def inicializar_base_datos():
    """Crea la base de datos si no existe."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido_paterno TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT NOT NULL,
            estatus TEXT NOT NULL,
            fecha_registro TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

class CRUDClientes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clientes")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #D0E8FF;
            }
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: #A9A9A9;
                font-size: 14px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                color: black;
                font-size: 14px;
            }
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid #A9A9A9;
                padding: 5px;
                font-size: 14px;
            }
        """)
        
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Email", "Teléfono", "Estatus", "Fecha Registro"])
        self.layout.addWidget(self.table)
        
        self.load_data()

        # Botones
        btn_layout = QHBoxLayout()
        self.btn_agregar = QPushButton("Agregar")
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_actualizar = QPushButton("Actualizar Lista")
        
        btn_layout.addWidget(self.btn_agregar)
        btn_layout.addWidget(self.btn_editar)
        btn_layout.addWidget(self.btn_eliminar)
        btn_layout.addWidget(self.btn_actualizar)
        
        self.layout.addLayout(btn_layout)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Eventos de botones
        self.btn_agregar.clicked.connect(self.agregar_cliente)
        self.btn_editar.clicked.connect(self.editar_cliente)
        self.btn_eliminar.clicked.connect(self.eliminar_cliente)
        self.btn_actualizar.clicked.connect(self.load_data)

    def load_data(self):
        """Carga los datos de clientes en la tabla."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))
        conn.close()

    def agregar_cliente(self):
        """Abre un diálogo para agregar un cliente."""
        dialog = ClienteDialog()
        if dialog.exec_() == QDialog.Accepted:
            nombre, apellido, email, telefono, estatus, fecha = dialog.get_data()
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clientes (nombre, apellido_paterno, email, telefono, estatus, fecha_registro) VALUES (?, ?, ?, ?, ?, ?)", 
                           (nombre, apellido, email, telefono, estatus, fecha))
            conn.commit()
            conn.close()
            self.load_data()

    def editar_cliente(self):
        """Edita el cliente seleccionado."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Selecciona un cliente para editar.")
            return

        id_cliente = self.table.item(selected_row, 0).text()
        dialog = ClienteDialog(edit=True)
        dialog.set_data(
            self.table.item(selected_row, 1).text(),
            self.table.item(selected_row, 2).text(),
            self.table.item(selected_row, 3).text(),
            self.table.item(selected_row, 4).text(),
            self.table.item(selected_row, 5).text(),
            self.table.item(selected_row, 6).text(),
        )

        if dialog.exec_() == QDialog.Accepted:
            nombre, apellido, email, telefono, estatus, fecha = dialog.get_data()
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE clientes 
                SET nombre = ?, apellido_paterno = ?, email = ?, telefono = ?, estatus = ?, fecha_registro = ?
                WHERE id = ?
            """, (nombre, apellido, email, telefono, estatus, fecha, id_cliente))
            conn.commit()
            conn.close()
            self.load_data()

    def eliminar_cliente(self):
        """Elimina el cliente seleccionado."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Selecciona un cliente para eliminar.")
            return
        
        id_cliente = self.table.item(selected_row, 0).text()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
        conn.commit()
        conn.close()
        self.load_data()

class ClienteDialog(QDialog):
    """Diálogo para agregar/editar un cliente."""
    def __init__(self, edit=False):
        super().__init__()
        self.setWindowTitle("Editar Cliente" if edit else "Agregar Cliente")
        self.layout = QVBoxLayout()
        self.setStyleSheet("""
            QDialog {
                background-color: #D0E8FF;
            }
        """)

        self.nombre = QLineEdit()
        self.apellido = QLineEdit()
        self.email = QLineEdit()
        self.telefono = QLineEdit()
        self.estatus = QLineEdit()
        self.fecha = QLineEdit()

        self.layout.addWidget(QLabel("Nombre:"))
        self.layout.addWidget(self.nombre)
        self.layout.addWidget(QLabel("Apellido Paterno:"))
        self.layout.addWidget(self.apellido)
        self.layout.addWidget(QLabel("Email:"))
        self.layout.addWidget(self.email)
        self.layout.addWidget(QLabel("Teléfono:"))
        self.layout.addWidget(self.telefono)
        self.layout.addWidget(QLabel("Estatus:"))
        self.layout.addWidget(self.estatus)
        self.layout.addWidget(QLabel("Fecha Registro (YYYY-MM-DD):"))
        self.layout.addWidget(self.fecha)

        self.btn_aceptar = QPushButton("Aceptar")
        self.btn_cancelar = QPushButton("Cancelar")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_aceptar)
        btn_layout.addWidget(self.btn_cancelar)
        self.layout.addLayout(btn_layout)

        self.setLayout(self.layout)

        self.btn_aceptar.clicked.connect(self.accept)
        self.btn_cancelar.clicked.connect(self.reject)

    def get_data(self):
        """Obtiene los datos ingresados."""
        return (self.nombre.text(), self.apellido.text(), self.email.text(), self.telefono.text(), self.estatus.text(), self.fecha.text())

    def set_data(self, nombre, apellido, email, telefono, estatus, fecha):
        """Establece los datos en los campos."""
        self.nombre.setText(nombre)
        self.apellido.setText(apellido)
        self.email.setText(email)
        self.telefono.setText(telefono)
        self.estatus.setText(estatus)
        self.fecha.setText(fecha)

if __name__ == "__main__":
    inicializar_base_datos()
    app = QApplication(sys.argv)
    window = CRUDClientes()
    window.show()
    sys.exit(app.exec_())

