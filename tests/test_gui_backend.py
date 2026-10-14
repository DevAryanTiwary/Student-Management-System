import unittest
import tempfile
from pathlib import Path
from managers.auth_manager import AuthManager
from storage.json_storage import JSONStorage
from services.integrity_service import IntegrityService
from config import ROLE_SUPER_ADMIN, ROLE_VIEWER, ROLE_TEACHER
import config

class TestGUIBackendUpgrades(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        config.ADMINS_JSON_FILE = Path(self.temp_dir.name) / "admins.json"
        self.auth = AuthManager()
        self.storage_file = Path(self.temp_dir.name) / "students.json"
        self.storage = JSONStorage(self.storage_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_rbac_roles_and_permissions(self):
        self.auth.login("admin", "AdminPassword@123")
        self.assertEqual(self.auth.current_role, ROLE_SUPER_ADMIN)
        self.assertTrue(self.auth.has_permission([ROLE_TEACHER]))

        self.auth.create_user("viewer_user", "ViewerPass@123", ROLE_VIEWER)
        self.auth.logout()

        self.auth.login("viewer_user", "ViewerPass@123")
        self.assertEqual(self.auth.current_role, ROLE_VIEWER)
        self.assertFalse(self.auth.has_permission([ROLE_SUPER_ADMIN]))

    def test_administrative_account_unlocking(self):
        for _ in range(config.MAX_LOGIN_ATTEMPTS):
            try:
                self.auth.login("admin", "WrongPass@999")
            except Exception:
                pass

        with self.assertRaises(Exception):
            self.auth.login("admin", "AdminPassword@123")

        self.auth.unlock_account("admin")
        self.assertTrue(self.auth.login("admin", "AdminPassword@123"))

    def test_integrity_service_diagnostics(self):
        svc = IntegrityService(self.storage)
        res = svc.perform_system_health_check()
        self.assertIn("status", res)
        self.assertEqual(res["status"], "HEALTHY")