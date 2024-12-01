import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.models.user_model import UserModel
from src.controllers.login_controller import LoginController


def test_login():
    # Datos de prueba
    test_user_username = "Eddys912"
    test_user_email = "eddys912sc@gmail.com"
    test_password = "12345678"

    user_with_username = UserModel(
        user=test_user_username, email=None, password=test_password
    )
    user_with_email = UserModel(
        user=None, email=test_user_email, password=test_password
    )

    login_controller = LoginController()

    print("\n******************** PRUEBA CON USUARIO ********************\n")
    print("Intentando iniciar sesión con nombre de usuario...")
    result_username = login_controller.authenticate_user(user_with_username)
    if isinstance(result_username, UserModel):
        print(f"Login exitoso con nombre de usuario: {result_username._user}")
    else:
        print("Credenciales incorrectas con nombre de usuario")

    print("\n******************** PRUEBA CON CORREO ********************\n")
    print("Intentando iniciar sesión con correo electrónico...")
    result_email = login_controller.authenticate_user(user_with_email)
    if isinstance(result_email, UserModel):
        print(f"Login exitoso con correo electrónico: {result_email._user}")
    else:
        print("Credenciales incorrectas con correo electrónico")

    print("\n******************** PRUEBA CON ERROR ********************\n")
    test_user_invalid = UserModel(user="Eddys999", email=None, password="wrongpassword")
    print("Intentando iniciar sesión con credenciales incorrectas...")
    result_invalid = login_controller.authenticate_user(test_user_invalid)
    if isinstance(result_invalid, dict) and "message" in result_invalid:
        print(f"Error: {result_invalid['message']}")
    else:
        print("Login exitoso con credenciales incorrectas (esto no debería ocurrir)")


if __name__ == "__main__":
    test_login()
