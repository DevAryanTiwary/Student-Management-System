import unittest
import tempfile
from pathlib import Path
from managers.auth_manager import AuthManager
from utils.exceptions import AuthenticationError, AccountLockedError
import config

class TestAuthManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        config.ADMINS_JSON_FILE = Path(self.temp_dir.name) / "admins.json"
        self.auth = AuthManager()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_default_login_success(self):
        success = self.auth.login("admin", "AdminPassword@123")
        self.assertTrue(success)
        self.assertEqual(self.auth.current_user, "admin")

    def test_login_failure_and_lockout(self):
        with self.assertRaises(AuthenticationError):
            self.auth.login("admin", "WrongPass1")
        with self.assertRaises(AuthenticationError):
            self.auth.login("admin", "WrongPass2")
        with self.assertRaises(AccountLockedError):
            self.auth.login("admin", "WrongPass3")

    def test_password_change(self):
        self.auth.login("admin", "AdminPassword@123")
        self.auth.change_password("AdminPassword@123", "BrandNewPass@999")
        self.auth.logout()

        with self.assertRaises(AuthenticationError):
            self.auth.login("admin", "AdminPassword@123")

        self.assertTrue(self.auth.login("admin", "BrandNewPass@999"))