import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name="passkeeper.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.setup_tables()

    def setup_tables(self):
        """Crea las tablas necesarias si no existen."""
        # Tabla para los usuarios
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)

        # Tabla para las contraseñas
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            password TEXT NOT NULL,
            date_created TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)

        self.connection.commit()

    def add_user(self, email, password):
        """Agregar un nuevo usuario."""
        try:
            self.cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # El correo ya existe

    def verify_user(self, email, password):
        """Verificar si un usuario existe y la contraseña es correcta."""
        self.cursor.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, password))
        return self.cursor.fetchone()

    def add_password(self, service, password, user_id):
        """Agregar una contraseña para un servicio."""
        date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
        INSERT INTO passwords (service, password, date_created, user_id)
        VALUES (?, ?, ?, ?)
        """, (service, password, date_created, user_id))
        self.connection.commit()

    def get_passwords(self, user_id):
        """Obtener todas las contraseñas para un usuario."""
        self.cursor.execute("""
        SELECT service, password, date_created FROM passwords WHERE user_id = ?
        """, (user_id,))
        return self.cursor.fetchall()

    def delete_password(self, service, user_id):
        """Eliminar una contraseña de un servicio."""
        self.cursor.execute("""
        DELETE FROM passwords WHERE service = ? AND user_id = ?
        """, (service, user_id))
        self.connection.commit()
