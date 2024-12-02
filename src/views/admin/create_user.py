import re
from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox
from PyQt6 import uic
from src.controllers.user_controller import UserController

class Create_User(QDialog):
    def __init__(self, previous_window):
        super().__init__()
        uic.loadUi("src/views/admin/create_user.ui", self)
        
        self.previous_window = previous_window

        self.btnGuardar.clicked.connect(self.guardar_usuario)
        self.btnSalir.clicked.connect(self.salir)

    def guardar_usuario(self):
        first_name = self.firstNameInput.text().strip()
        last_name = self.lastNameInput.text().strip()
        user = self.userInput.text().strip()
        email = self.emailInput.text().strip()
        password = self.passwordInput.text().strip()
        rol = self.roleComboBox.currentText().strip().upper()

        if not all([first_name, last_name, user, email, password, rol]):
            QMessageBox.warning(self, "Campos incompletos", "Todos los campos son obligatorios.")
            return

        if not self.validar_email(email):
            QMessageBox.warning(self, "Email inválido", "Por favor ingrese un email válido.")
            return

        if len(password) < 8:
            QMessageBox.warning(self, "Contraseña inválida", "La contraseña debe tener al menos 6 caracteres.")
            return

        userCont = UserController()
        response = userCont.create_user(first_name, last_name, user, email, password, rol)

        if response.get("message") == 'Usuario creado correctamente':
            QMessageBox.information(self, "Éxito", "Usuario creado exitosamente.")
            self.limpiar_campos()
        else:
            QMessageBox.warning(self, "Resultado", response["message"])
            self.limpiar_campos()

    def validar_email(self, email):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, email)

    def limpiar_campos(self):

        self.firstNameInput.clear()
        self.lastNameInput.clear()
        self.userInput.clear()
        self.emailInput.clear()
        self.passwordInput.clear()
        self.roleComboBox.setCurrentIndex(0)

    def salir(self):
        self.previous_window.llenar_tabla()
        self.close()
        self.previous_window.show()
