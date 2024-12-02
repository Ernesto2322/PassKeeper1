import tkinter as tk
import re
from tkinter import messagebox, simpledialog
from tkinter import ttk
from src.logica.database import Database
from src.logica.Passkeeper import Passkeeper

class LoginApp:
    def __init__(self, root):
        self.db = Database()  # Conexión a la base de datos
        self.root = root
        self.root.title("Login - Passkeeper")
        self.root.geometry("400x300")
        self.root.configure(bg="#f7f7f7")  # Fondo claro

        # Encabezado
        self.header = tk.Label(
            root, text="Passkeeper - Inicio de Sesión", font=("Arial", 18, "bold"), bg="#007acc", fg="white"
        )
        self.header.pack(fill=tk.X, pady=10)

        # Formulario de inicio de sesión
        self.email_label = tk.Label(root, text="Correo Electrónico:", font=("Arial", 12), bg="#f7f7f7")
        self.email_label.pack(pady=(20, 5))
        self.email_entry = tk.Entry(root, width=30, font=("Arial", 12))
        self.email_entry.pack()

        self.password_label = tk.Label(root, text="Contraseña:", font=("Arial", 12), bg="#f7f7f7")
        self.password_label.pack(pady=(10, 5))
        self.password_entry = tk.Entry(root, show="*", width=30, font=("Arial", 12))
        self.password_entry.pack()

        # Botones
        self.login_button = tk.Button(
            root, text="Iniciar Sesión", font=("Arial", 12), bg="#007acc", fg="white", command=self.login
        )
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(
            root, text="Registrarse", font=("Arial", 12), bg="#28a745", fg="white", command=self.register
        )
        self.register_button.pack()

    def login(self):
        """Verifica las credenciales y accede a la aplicación principal."""
        email = self.email_entry.get()
        password = self.password_entry.get()

        user = self.db.verify_user(email, password)
        if user:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
            self.open_main_app(user[0])  # user[0] es el ID del usuario
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos.")

    def register(self):
        """Registra un nuevo usuario."""
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showwarning("Error", "Por favor, completa todos los campos.")
            return

        if self.db.add_user(email, password):
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente. Ahora puedes iniciar sesión.")
        else:
            messagebox.showerror("Error", "El correo ya está registrado. Usa otro correo.")

    def open_main_app(self, user_id):
        """Abre la aplicación principal pasando el ID del usuario."""
        self.root.destroy()  # Cierra la ventana actual
        main_root = tk.Tk()
        app = PasskeeperApp(main_root, user_id=user_id)
        main_root.mainloop()


class PasskeeperApp:
    def __init__(self, root, user_id):
        self.user_id = user_id  # ID del usuario autenticado
        self.passkeeper = Passkeeper()
        self.root = root
        self.root.title("Passkeeper")
        self.root.geometry("500x400")
        self.root.configure(bg="#e6f0fa")  # Fondo azul claro

        # Encabezado
        self.header = tk.Frame(root, bg="#007acc", height=60)
        self.header.pack(fill=tk.X)

        self.header_label = tk.Label(
            self.header,
            text="Passkeeper",
            font=("Arial", 24, "bold"),
            bg="#007acc",
            fg="white",
        )
        self.header_label.pack(pady=10)

        # Contenedor principal
        self.main_frame = tk.Frame(root, bg="#e6f0fa", padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Widgets de entrada
        self.service_label = tk.Label(
            self.main_frame, text="Servicio:", font=("Arial", 12), bg="#e6f0fa"
        )
        self.service_label.grid(row=0, column=0, sticky=tk.W, pady=5)

        self.service_entry = tk.Entry(self.main_frame, width=30, font=("Arial", 12))
        self.service_entry.grid(row=0, column=1, pady=5)

        self.password_label = tk.Label(
            self.main_frame, text="Contraseña:", font=("Arial", 12), bg="#e6f0fa"
        )
        self.password_label.grid(row=1, column=0, sticky=tk.W, pady=5)

        self.password_entry = tk.Entry(self.main_frame, width=30, font=("Arial", 12))
        self.password_entry.grid(row=1, column=1, pady=5)

        # Botones con estilo
        self.button_style = ttk.Style()
        self.button_style.configure("TButton", font=("Arial", 10), padding=5)

        self.add_button = ttk.Button(
            self.main_frame, text="Agregar", command=self.add_password
        )
        self.add_button.grid(row=2, column=0, padx=5, pady=10, sticky=tk.EW)

        self.edit_button = ttk.Button(
            self.main_frame, text="Editar", command=self.edit_password
        )
        self.edit_button.grid(row=2, column=1, padx=5, pady=10, sticky=tk.EW)

        self.delete_button = ttk.Button(
            self.main_frame, text="Eliminar", command=self.delete_password
        )
        self.delete_button.grid(row=3, column=0, padx=5, pady=10, sticky=tk.EW)

        self.list_button = ttk.Button(
            self.main_frame, text="Listar", command=self.list_passwords
        )
        self.list_button.grid(row=3, column=1, padx=5, pady=10, sticky=tk.EW)

        self.filter_button = ttk.Button(
            self.main_frame, text="Buscar", command=self.filter_passwords
        )
        self.filter_button.grid(row=4, column=0, padx=5, pady=10, sticky=tk.EW)

        self.generate_button = ttk.Button(
            self.main_frame, text="Generar Contraseña", command=self.generate_password
        )
        self.generate_button.grid(row=4, column=1, padx=5, pady=10, sticky=tk.EW)

        self.auth_button = ttk.Button(
            self.main_frame, text="Autenticación 2FA", command=self.enable_2fa
        )
        self.auth_button.grid(row=5, column=0, columnspan=2, pady=20, sticky=tk.EW)

    def add_password(self):
        service = self.service_entry.get()
        password = self.password_entry.get()
        if service and password:
            self.passkeeper.add_password(service, password)
            messagebox.showinfo("Éxito", f"Contraseña para {service} agregada.")
            self.clear_entries()
        else:
            messagebox.showwarning("Error", "Por favor ingresa el servicio y la contraseña.")

    def edit_password(self):
        service = self.service_entry.get()
        new_password = self.password_entry.get()
        if service and new_password:
            self.passkeeper.edit_password(service, new_password)
            messagebox.showinfo("Éxito", f"Contraseña para {service} actualizada.")
            self.clear_entries()
        else:
            messagebox.showwarning("Error", "Por favor ingresa el servicio y la nueva contraseña.")

    def delete_password(self):
        service = self.service_entry.get()
        if service:
            self.passkeeper.delete_password(service)
            messagebox.showinfo("Éxito", f"Contraseña para {service} eliminada.")
            self.clear_entries()
        else:
            messagebox.showwarning("Error", "Por favor ingresa el servicio.")

    def list_passwords(self):
        passwords = self.passkeeper.passwords
        if passwords:
            password_list = "\n".join([f"{service}: {pwd}" for service, pwd in passwords.items()])
            messagebox.showinfo("Lista de Contraseñas", password_list)
        else:
            messagebox.showinfo("Lista de Contraseñas", "No hay contraseñas guardadas.")

    def filter_passwords(self):
        query = simpledialog.askstring("Buscar", "Ingresa el texto a buscar:")
        if query:
            filtered = {
                service: pwd
                for service, pwd in self.passkeeper.passwords.items()
                if query.lower() in service.lower()
            }
            if filtered:
                result = "\n".join([f"{service}: {pwd}" for service, pwd in filtered.items()])
                messagebox.showinfo("Resultados de la búsqueda", result)
            else:
                messagebox.showinfo("Resultados de la búsqueda", "No se encontraron coincidencias.")

    def generate_password(self):
        password = self.passkeeper.generate_secure_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        messagebox.showinfo("Contraseña Generada", f"Contraseña segura: {password}")

    def enable_2fa(self):
        self.passkeeper.enable_two_factor_authentication()
        messagebox.showinfo("Autenticación 2FA", "Autenticación en dos pasos habilitada.")

    def clear_entries(self):
        self.service_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def enable_2fa(self):
        """Habilitar la autenticación en dos pasos solicitando un número de celular."""
        # Pedir al usuario que ingrese su número de celular
        phone_number = simpledialog.askstring("Autenticación 2FA",
                                              "Ingresa tu número de celular (9 dígitos, comienza con 0):")

        # Validar el formato del número de celular
        if phone_number and self.is_valid_phone_number(phone_number):
            # Si el número es válido, habilitamos la autenticación en dos pasos
            self.passkeeper.enable_two_factor_authentication()
            messagebox.showinfo("Autenticación 2FA",
                                f"Autenticación en dos pasos habilitada para el número: {phone_number}")
        else:
            # Mostrar un mensaje de error si el formato es incorrecto
            messagebox.showwarning("Error",
                                   "Por favor ingresa un número de celular válido (9 dígitos, comienza con 9).")

    def is_valid_phone_number(self, phone_number):
        """Validar el formato del número de celular."""
        # Verificar que tenga exactamente 9 dígitos y comience con un 0
        pattern = r"^9\d{8}$"  # Ejemplo: 012345678
        return re.match(pattern, phone_number) is not None


# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

