from src.models.user_model import UserModel

class UserController:
    def get_all_users(self):
        try:
            user_model = UserModel()
            users = user_model.get_all_users()
            return users if users else {"message": "No se encontraron usuarios."}
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return {"message": "Error al obtener usuarios."}

    def create_user(self, first_name, last_name, user, email, password):
        try:
            if not all([first_name, last_name, user, email, password]):
                return {"message": "Todos los campos son obligatorios."}
            new_user = UserModel(first_name, last_name, user, email, password)
            return new_user.create_user()
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return {"message": "Error al crear usuario."}

<<<<<<< HEAD
    def update_user(self, id, first_name=None, last_name=None, user=None, email=None, password=None, rol=None):
=======
    def update_user(
        self, id, first_name=None, last_name=None, user=None, email=None, password=None
    ):
>>>>>>> parent of 785fc5b (Merge pull request #1 from contrerasalexa/alexa)
        try:
            if not any([first_name, last_name, user, email, password]):
                return {
                    "message": "Debe proporcionar al menos un campo para actualizar."
                }
            user_model = UserModel()
            existing_user = user_model.get_user_by_id(id)
            if not existing_user:
                return {"message": "El usuario no existe."}
            updated_user = UserModel(
                first_name=first_name or existing_user[1],
                last_name=last_name or existing_user[2],
                user=user or existing_user[3],
                email=email or existing_user[4],
                password=password or existing_user[5],
            )
            return updated_user.update_user(id)
        except Exception as e:
            print(f"Error al actualizar usuario con ID {id}: {e}")
            return {"message": "Error al actualizar usuario."}

    def delete_user(self, id):
        try:
            user_model = UserModel()
            existing_user = user_model.get_user_by_id(id)
            if not existing_user:
                return {"message": "El usuario no existe."}
            return user_model.delete_user(id)
        except Exception as e:
            print(f"Error al eliminar usuario con ID {id}: {e}")
            return {"message": "Error al eliminar usuario."}

    def get_user_by_id(self, id):
        try:
            user_model = UserModel()
            user = user_model.get_user_by_id(id)
            if user:
                return user
            else:
                return {"message": "El usuario no existe."}
        except Exception as e:
            print(f"Error al obtener usuario con ID {id}: {e}")
            return {"message": "Error al obtener usuario."}
