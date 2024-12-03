from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QPushButton, QHBoxLayout, QWidget, QMessageBox
from PyQt6 import uic
from src.controllers.user_controller import UserController
from src.views.admin.create_user import Create_User
from src.views.admin.update_user import Update_User

class UserTable(QDialog):
    def __init__(self, previous_window):
        super().__init__()
        uic.loadUi("src/views/admin/table_users.ui", self)  # Cargar la interfaz

        self.previous_window = previous_window

        self.tableUsers.horizontalHeader().setVisible(True)
        self.tableUsers.verticalHeader().setVisible(False)

        self.tableUsers.setColumnWidth(0, 50)   # ID
        self.tableUsers.setColumnWidth(1, 120)  # Nombre
        self.tableUsers.setColumnWidth(2, 120)  # Apellido
        self.tableUsers.setColumnWidth(3, 180)  # Email
        self.tableUsers.setColumnWidth(4, 120)  # Usuario
        self.tableUsers.setColumnWidth(5, 150)  # Rol
        self.tableUsers.setColumnWidth(6, 250)  # Acciones

        self.btnCerrar.clicked.connect(self.salir)
        self.btnAgregarUsuario.clicked.connect(self.agregar_usuario)

        self.llenar_tabla()

    def llenar_tabla(self):
        userCont = UserController()

        users = userCont.get_all_users()

        # Configurar la tabla para mostrar los usuarios, sin incluir el campo contraseña
        self.tableUsers.setRowCount(len(users))
        for row, user in enumerate(users):
            # Excluir la contraseña (índice 5) al llenar la tabla
            for col, value in enumerate(user):
                if col == 5:  # Saltar la columna de la contraseña
                    continue
                adjusted_col = col if col < 5 else col - 1  # Ajustar índice de columna después de excluir
                self.tableUsers.setItem(row, adjusted_col, QTableWidgetItem(str(value)))

            # Añadir botones de "Actualizar" y "Eliminar" en la columna de acciones
            btnActualizar = QPushButton('Actualizar')
            btnEliminar = QPushButton('Eliminar')

            # Estilo y tamaño de los botones
            btnActualizar.setStyleSheet("background-color: rgb(85, 170, 255); color: white; font: bold 12px;")
            btnEliminar.setStyleSheet("background-color: rgb(255, 85, 85); color: white; font: bold 12px;")
            btnActualizar.setFixedSize(90, 30)
            btnEliminar.setFixedSize(90, 30)

            # Conectar los botones a sus respectivas funciones
            btnActualizar.clicked.connect(lambda ch, user_id=user[0]: self.actualizar_usuario(user_id))
            btnEliminar.clicked.connect(lambda ch, user_id=user[0]: self.confirmar_eliminacion(user_id))

            # Crear un layout horizontal para los botones
            layout = QHBoxLayout()
            layout.addWidget(btnActualizar)
            layout.addWidget(btnEliminar)
            layout.setSpacing(10)  # Espacio entre los botones
            layout.setContentsMargins(0, 0, 0, 0)  # Sin margen para ajustar el contenido

            # Añadir el layout a un widget para colocarlo en la celda
            widget = QWidget()
            widget.setLayout(layout)

            self.tableUsers.setCellWidget(row, 6, widget)  # Columna de "Acciones" es la última (índice 6 después de excluir la contraseña)

    def agregar_usuario(self):
        self.create_user = Create_User(self)
        self.create_user.show()
        self.close()

    def actualizar_usuario(self, user_id):
        self.update_user = Update_User(user_id=user_id, previous_window=self)
        self.update_user.show()
        self.close()

    def confirmar_eliminacion(self, user_id):
        confirmacion = QMessageBox()
        confirmacion.setIcon(QMessageBox.Icon.Warning)
        confirmacion.setWindowTitle("Confirmar Eliminación")
        confirmacion.setText("¿Estás seguro de que deseas eliminar este usuario?")
        confirmacion.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        confirmacion.setDefaultButton(QMessageBox.StandardButton.No)

        respuesta = confirmacion.exec()

        if respuesta == QMessageBox.StandardButton.Yes:
            self.eliminar_usuario(user_id)
            self.llenar_tabla()

    def eliminar_usuario(self, user_id):
        userCont = UserController()
        response = userCont.delete_user(user_id)

        if response.get("message") == 'Usuario eliminado correctamente':
            QMessageBox.information(self, "Eliminación Exitosa", f"Usuario con ID {user_id} eliminado correctamente.")
            self.llenar_tabla()  # Actualizar la tabla después de eliminar
        else:
            QMessageBox.critical(self, "Error", response["message"])

    def salir(self):
        self.close()
        self.previous_window.show()
