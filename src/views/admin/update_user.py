from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from src.controllers.user_controller import UserController
import re

class Update_User(QDialog):
    def __init__(self, user_id, previous_window):
        super().__init__()
        uic.loadUi("src/views/admin/update_user.ui", self)  # Cargar la interfaz
        self.user_id = user_id
        self.previous_window = previous_window

        # Cargar los datos actuales del usuario
        self.load_user_data()

        # Conectar los botones a sus funciones correspondientes
        self.btnGuardar.clicked.connect(self.guardar_usuario)
        self.btnSalir.clicked.connect(self.salir)

    def load_user_data(self):
        userCont = UserController()
        user = userCont.get_user_by_id(self.user_id)

        if user:
            self.firstNameInput.setText(user[1])  # Nombre
            self.lastNameInput.setText(user[2])  # Apellido
            self.emailInput.setText(user[3])  # Email
            self.userInput.setText(user[4])  # Usuario
            self.roleComboBox.setCurrentText(user[6])  # Rol

    def guardar_usuario(self):
        # Recoger datos del formulario
        first_name = self.firstNameInput.text().strip()
        last_name = self.lastNameInput.text().strip()
        user = self.userInput.text().strip()
        email = self.emailInput.text().strip()
        rol = self.roleComboBox.currentText().strip().upper()

        # Validaciones de los campos
        if not first_name:
            QMessageBox.critical(self, "Error", "El campo 'Nombre' es obligatorio.")
            return

        if not last_name:
            QMessageBox.critical(self, "Error", "El campo 'Apellido' es obligatorio.")
            return

        if not user:
            QMessageBox.critical(self, "Error", "El campo 'Usuario' es obligatorio.")
            return

        if not email:
            QMessageBox.critical(self, "Error", "El campo 'Email' es obligatorio.")
            return

        # Validar el formato del email
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            QMessageBox.critical(self, "Error", "El email ingresado no tiene un formato válido.")
            return

        if rol not in ["ADMINISTRADOR", "USUARIO"]:
            QMessageBox.critical(self, "Error", "El campo 'Rol' debe ser 'Administrador' o 'Usuario'.")
            return

        # Si todas las validaciones son exitosas, actualizar el usuario
        userCont = UserController()
        response = userCont.update_user(self.user_id, first_name, last_name, user, email, None, rol)

        if response.get("message") == 'Usuario actualizado correctamente':
            QMessageBox.information(self, "Éxito", "Usuario actualizado exitosamente.")
            self.salir()
        else:
            QMessageBox.critical(self, "Error", response.get("message"))

    def salir(self):
        self.previous_window.llenar_tabla()
        self.close()
        self.previous_window.show()
