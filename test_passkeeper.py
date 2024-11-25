import unittest
from src.logica.Passkeeper import Passkeeper

class TestPasskeeper(unittest.TestCase):
    def setUp(self):
        self.passkeeper = Passkeeper()

    def test_add_password(self):
        self.passkeeper.add_password("gmail", "123456")
        self.assertIn("gmail", self.passkeeper.passwords)
        self.assertEqual(self.passkeeper.passwords["gmail"], "123456")

    def test_edit_password(self):
        self.passkeeper.add_password("github", "password123")
        self.passkeeper.edit_password("github", "newpassword456")
        self.assertEqual(self.passkeeper.passwords["github"], "newpassword456")

    def test_delete_password(self):
        self.passkeeper.add_password("facebook", "mypassword")
        self.passkeeper.delete_password("facebook")
        self.assertNotIn("facebook", self.passkeeper.passwords)

if __name__ == "__main__":
    unittest.main()

