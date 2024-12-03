import sys
import os

# Agrega la raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.models.user_model import UserModel
from src.database.connection import DBConnection


class LoginController:
    def authenticate_user(self, user: UserModel):
        cursor = None
        db = None
        try:
            db = DBConnection().connection()
            cursor = db.cursor()
            if user._user:
                query = "SELECT * FROM users WHERE user=%s AND password=%s"
                values = (user._user, user._password)
            elif user._email:
                query = "SELECT * FROM users WHERE email=%s AND password=%s"
                values = (user._email, user._password)
            cursor.execute(query, values)
            row = cursor.fetchone()
            if row:
                return UserModel(user=row[3], email=row[4], password=row[5])
            return {"message": "Credenciales inválidas."}
        except Exception as e:
            print(f"Error en login: {e}")
            return {"message": "No se puede acceder al sistema, intentarlo más tarde."}
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
