from PyQt6 import uic
from src.models.user_model import UserModel
from src.controllers.login_controller import LoginController
from src.views.pprincipal import Principal


class Login:
    def __init__(self):
        print("Inicio del programa.")
        self.login = uic.loadUi("src/views/login.ui")
        self.login.line_user.setFocus()
        self.login.show()
        self.init()

    def init(self):
        self.login.btn_access.clicked.connect(self.validate_login_form)

    def validate_login_form(self):
        username_or_email = self.login.line_user.text().strip()
        password = self.login.line_password.text().strip()

        if not self.validate_username(username_or_email):
            return
        if not self.validate_password(password):
            return

        self.login.lb_error.setText("")

        # Crear el modelo del usuario según sea email o username
        if "@" in username_or_email:
            user = UserModel(user=None, email=username_or_email, password=password)
        else:
            user = UserModel(user=username_or_email, email=None, password=password)

        user_controller = LoginController()
        res = user_controller.authenticate_user(user)

        if isinstance(res, dict) and "message" in res:
            self.show_error(res["message"])
        elif isinstance(res, UserModel):
            # Validar el rol del usuario y abrir la interfaz correspondiente
            if res._rol == "ADMINISTRADOR":
                self.abrir_pprincipal()
            elif res._rol == "USUARIO":
                self.abrir_pusuario()
            else:
                self.show_error("Acceso denegado. Rol desconocido.")
        else:
            self.show_error("Ha ocurrido un error inesperado. Intente nuevamente.")

    def validate_username(self, username):
        import re

        pattern = r"^[a-zA-Z0-9._@]+$"

        if not username:
            self.show_error("El nombre de usuario no puede estar vacío.")
            self.login.line_user.setFocus()
            return False

        if not re.match(pattern, username):
            self.show_error("El nombre de usuario contiene caracteres no permitidos.")
            self.login.line_user.setFocus()
            return False
        return True

    def validate_password(self, password):
        if len(password) < 8:
            self.show_error("La contraseña debe tener al menos 8 caracteres.")
            self.login.line_password.setFocus()
            return False
        if not password:
            self.show_error("La contraseña no puede estar vacía.")
            self.login.line_password.setFocus()
            return False
        return True

    def show_error(self, message):
        self.login.lb_error.setText(message)

    def abrir_pprincipal(self):
        try:
            print("Cargando pprincipal...")
            from src.views.pprincipal import Principal

            # Cerrar ventana de login antes de abrir pprincipal
            self.login.close()
            # Cargar la ventana principal
            self.principal = Principal()
            self.principal.show()
            print("Ventana principal cargada correctamente.")
        except Exception as e:
            print(f"Error al cargar pprincipal: {e}")



    def abrir_pusuario(self):
        try:
            print("Cargando pprincipal...")
            from src.views.pUsuario import Usuario

            # Cerrar ventana de login antes de abrir pprincipal
            self.login.close()

            # Cargar la ventana principal
            self.usuario = Usuario()
            self.usuario.show()
            print("Ventana principal cargada correctamente.")
        except Exception as e:
            print(f"Error al cargar pprincipal: {e}")

