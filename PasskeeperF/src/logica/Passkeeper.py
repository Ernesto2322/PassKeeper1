import random
import string


class Passkeeper:
    def __init__(self):
        self.passwords = {}  # Diccionario para almacenar contraseñas por servicio

    def add_password(self, service, password):
        """Agregar una contraseña para un servicio."""
        self.passwords[service] = password
        print(f"Contraseña para {service} agregada exitosamente.")

    def edit_password(self, service, new_password):
        """Editar una contraseña existente para un servicio."""
        if service in self.passwords:
            self.passwords[service] = new_password
            print(f"Contraseña para {service} actualizada exitosamente.")
        else:
            print(f"No se encontró el servicio {service}.")

    def delete_password(self, service):
        """Eliminar una contraseña de un servicio."""
        if service in self.passwords:
            del self.passwords[service]
            print(f"Contraseña para {service} eliminada exitosamente.")
        else:
            print(f"No se encontró el servicio {service}.")

    def list_passwords(self):
        """Listar todos los servicios y contraseñas."""
        if self.passwords:
            print("Lista de contraseñas:")
            for service, password in self.passwords.items():
                print(f"{service}: {password}")
        else:
            print("No hay contraseñas guardadas.")

    def filter_passwords(self, query):
        """Filtrar servicios por un texto."""
        filtered = {service: pwd for service, pwd in self.passwords.items() if query.lower() in service.lower()}
        if filtered:
            print("Resultados de la búsqueda:")
            for service, password in filtered.items():
                print(f"{service}: {password}")
        else:
            print("No se encontraron servicios que coincidan con la búsqueda.")

    def generate_secure_password(self, length=12):
        """Generar una contraseña segura aleatoria."""
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        print(f"Contraseña segura generada: {password}")
        return password

    def enable_two_factor_authentication(self):
        """Simular la habilitación de autenticación en dos pasos."""
        print("Autenticación en dos pasos habilitada. Se requiere un código adicional para acceder.")


# Ejemplo de uso:
if __name__ == "__main__":
    passkeeper = Passkeeper()
    passkeeper.add_password("email", "mypassword123")
    passkeeper.list_passwords()
    passkeeper.edit_password("email", "newpassword456")
    passkeeper.list_passwords()
    passkeeper.generate_secure_password()
    passkeeper.delete_password("email")
    passkeeper.list_passwords()
    passkeeper.enable_two_factor_authentication()