import unittest
from src.logica.Passkeeper import Passkeeper

class TestPasskeeper(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.passkeeper = Passkeeper()

    def test_add_password(self):
        """Test para agregar una contraseña."""
        self.passkeeper.add_password("gmail", "123456")
        self.assertIn("gmail", self.passkeeper.passwords)
        self.assertEqual(self.passkeeper.passwords["gmail"], "123456")

    def test_edit_password(self):
        """Test para editar una contraseña existente."""
        self.passkeeper.add_password("github", "password123")
        self.passkeeper.edit_password("github", "newpassword456")
        self.assertEqual(self.passkeeper.passwords["github"], "newpassword456")

    def test_delete_password(self):
        """Test para eliminar una contraseña."""
        self.passkeeper.add_password("facebook", "mypassword")
        self.passkeeper.delete_password("facebook")
        self.assertNotIn("facebook", self.passkeeper.passwords)

if __name__ == "__main__":
    unittest.main()