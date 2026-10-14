"""
Authentication & RBAC Manager.
Extends existing PBKDF2 authentication with roles, status toggling, and multi-user administration.
"""
import os
import json
import hashlib
import binascii
from datetime import datetime
from typing import Dict, Any, List, Optional
from config import (
    ADMINS_JSON_FILE,
    MAX_LOGIN_ATTEMPTS,
    PASSWORD_SALT_BYTES,
    PBKDF2_ITERATIONS,
    DEFAULT_ADMIN_USERNAME,
    DEFAULT_ADMIN_PASSWORD,
    ROLE_SUPER_ADMIN,
    ROLE_ADMIN,
    ROLE_TEACHER,
    ROLE_VIEWER
)
from utils.exceptions import AuthenticationError, AccountLockedError
from utils.logger import log_activity

class AuthManager:
    def __init__(self):
        self.current_user: Optional[str] = None
        self.current_role: Optional[str] = None
        self.failed_attempts: Dict[str, int] = {}
        self._initialize_admin_store()

    def _hash_password(self, password: str, salt: bytes = None) -> tuple[str, str]:
        if salt is None:
            salt = os.urandom(PASSWORD_SALT_BYTES)
        derived = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            PBKDF2_ITERATIONS
        )
        return binascii.hexlify(salt).decode("ascii"), binascii.hexlify(derived).decode("ascii")

    def _verify_password(self, provided_password: str, hex_salt: str, hex_hash: str) -> bool:
        salt = binascii.unhexlify(hex_salt.encode("ascii"))
        _, check_hash = self._hash_password(provided_password, salt=salt)
        return check_hash == hex_hash

    def _initialize_admin_store(self):
        if not ADMINS_JSON_FILE.exists():
            salt, p_hash = self._hash_password(DEFAULT_ADMIN_PASSWORD)
            initial_data = {
                DEFAULT_ADMIN_USERNAME: {
                    "salt": salt,
                    "hash": p_hash,
                    "role": ROLE_SUPER_ADMIN,
                    "created_at": datetime.now().isoformat(),
                    "is_locked": False,
                    "is_enabled": True
                }
            }
            with open(ADMINS_JSON_FILE, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, indent=4)
        else:
            admins = self._load_admins()
            changed = False
            for user, data in admins.items():
                if "role" not in data:
                    data["role"] = ROLE_SUPER_ADMIN
                    changed = True
                if "is_enabled" not in data:
                    data["is_enabled"] = True
                    changed = True
            if changed:
                self._save_admins(admins)

    def _load_admins(self) -> Dict[str, Any]:
        try:
            with open(ADMINS_JSON_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_admins(self, data: Dict[str, Any]):
        with open(ADMINS_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def login(self, username: str, password: str) -> bool:
        admins = self._load_admins()
        user = username.strip()

        if user not in admins:
            log_activity(user, "LOGIN_FAILED", "User does not exist")
            raise AuthenticationError("Invalid username or password.")

        record = admins[user]

        if not record.get("is_enabled", True):
            log_activity(user, "LOGIN_BLOCKED", "Account disabled by administrator")
            raise AuthenticationError("This account has been disabled. Please contact your Administrator.")

        if record.get("is_locked", False):
            log_activity(user, "LOGIN_BLOCKED", "Account locked")
            raise AccountLockedError("Account is locked due to excessive failed attempts. Please unlock via Administrator.")

        salt = record["salt"]
        stored_hash = record["hash"]

        if self._verify_password(password, salt, stored_hash):
            self.failed_attempts[user] = 0
            self.current_user = user
            self.current_role = record.get("role", ROLE_ADMIN)
            log_activity(user, "LOGIN_SUCCESS", f"Authentication successful (Role: {self.current_role})")
            return True
        else:
            attempts = self.failed_attempts.get(user, 0) + 1
            self.failed_attempts[user] = attempts
            log_activity(user, "LOGIN_FAILED", f"Attempt {attempts} of {MAX_LOGIN_ATTEMPTS}")

            if attempts >= MAX_LOGIN_ATTEMPTS:
                record["is_locked"] = True
                self._save_admins(admins)
                log_activity(user, "ACCOUNT_LOCKED", "Locked out due to repeated failures")
                raise AccountLockedError(f"Account locked! Maximum attempts ({MAX_LOGIN_ATTEMPTS}) exceeded.")

            remaining = MAX_LOGIN_ATTEMPTS - attempts
            raise AuthenticationError(f"Invalid username or password. {remaining} attempts remaining.")

    def logout(self):
        if self.current_user:
            log_activity(self.current_user, "LOGOUT", "User logged out")
            self.current_user = None
            self.current_role = None

    def is_authenticated(self) -> bool:
        return self.current_user is not None

    def has_permission(self, required_roles: List[str]) -> bool:
        if not self.is_authenticated():
            return False
        if self.current_role == ROLE_SUPER_ADMIN:
            return True
        return self.current_role in required_roles

    def change_password(self, old_pass: str, new_pass: str) -> bool:
        if not self.is_authenticated():
            raise AuthenticationError("Must be logged in to change password.")

        if len(new_pass) < 8:
            raise AuthenticationError("New password must be at least 8 characters long.")

        admins = self._load_admins()
        record = admins[self.current_user]

        if not self._verify_password(old_pass, record["salt"], record["hash"]):
            log_activity(self.current_user, "CHANGE_PASSWORD_FAILED", "Incorrect old password")
            raise AuthenticationError("Current password incorrect.")

        salt, p_hash = self._hash_password(new_pass)
        record["salt"] = salt
        record["hash"] = p_hash
        self._save_admins(admins)

        log_activity(self.current_user, "CHANGE_PASSWORD_SUCCESS", "Password updated successfully")
        return True

    def list_users(self) -> List[Dict[str, Any]]:
        admins = self._load_admins()
        users = []
        for uname, info in admins.items():
            users.append({
                "username": uname,
                "role": info.get("role", ROLE_ADMIN),
                "is_locked": info.get("is_locked", False),
                "is_enabled": info.get("is_enabled", True),
                "created_at": info.get("created_at", "N/A")
            })
        return users

    def create_user(self, username: str, password: str, role: str) -> bool:
        u = username.strip()
        if not u or len(password) < 8:
            raise AuthenticationError("Username cannot be empty and password must be >= 8 characters.")

        admins = self._load_admins()
        if u in admins:
            raise AuthenticationError(f"User '{u}' already exists.")

        salt, p_hash = self._hash_password(password)
        admins[u] = {
            "salt": salt,
            "hash": p_hash,
            "role": role,
            "created_at": datetime.now().isoformat(),
            "is_locked": False,
            "is_enabled": True
        }
        self._save_admins(admins)
        log_activity(self.current_user or "SYSTEM", "CREATE_USER", f"Created user {u} with role {role}")
        return True

    def unlock_account(self, username: str) -> bool:
        admins = self._load_admins()
        if username in admins:
            admins[username]["is_locked"] = False
            self.failed_attempts[username] = 0
            self._save_admins(admins)
            log_activity(self.current_user or "SYSTEM", "UNLOCK_ACCOUNT", f"Unlocked account {username}")
            return True
        return False

    def toggle_user_enabled(self, username: str, enabled: bool) -> bool:
        if username == DEFAULT_ADMIN_USERNAME:
            raise AuthenticationError("Cannot disable default root administrator.")
        admins = self._load_admins()
        if username in admins:
            admins[username]["is_enabled"] = enabled
            self._save_admins(admins)
            log_activity(self.current_user or "SYSTEM", "TOGGLE_USER_STATUS", f"User {username} enabled={enabled}")
            return True
        return False