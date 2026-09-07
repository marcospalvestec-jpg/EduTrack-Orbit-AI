"""In-memory authentication service used only by the demonstration prototype."""

from __future__ import annotations

import hashlib
import hmac
import os
import re
from dataclasses import dataclass
from typing import Any

DEMO_EMAIL = "demo@edutrack.ai"
DEMO_PASSWORD = "Orbit@123"
DEMO_NAME = "Estudante Demo"

_EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_HASH_ITERATIONS = 120_000


@dataclass(frozen=True)
class AuthResult:
    """Result returned by local authentication operations."""

    success: bool
    message: str
    user: dict[str, str] | None = None


def _hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    actual_salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), actual_salt, _HASH_ITERATIONS)
    return actual_salt.hex(), digest.hex()


class DemoAuthService:
    """Manage temporary users without external persistence."""

    def __init__(self, users: dict[str, dict[str, Any]] | None = None) -> None:
        self.users = users if users is not None else {}
        self._ensure_demo_user()

    @staticmethod
    def normalize_email(email: str) -> str:
        """Normalize e-mail addresses used as local identifiers."""
        return email.strip().lower()

    def _ensure_demo_user(self) -> None:
        if DEMO_EMAIL in self.users:
            return
        salt, password_hash = _hash_password(DEMO_PASSWORD)
        self.users[DEMO_EMAIL] = {
            "name": DEMO_NAME,
            "email": DEMO_EMAIL,
            "salt": salt,
            "password_hash": password_hash,
        }

    @staticmethod
    def public_user(record: dict[str, Any]) -> dict[str, str]:
        """Return only fields safe to expose to the interface."""
        return {"name": str(record["name"]), "email": str(record["email"])}

    @staticmethod
    def validate_registration(
        name: str, email: str, password: str, confirmation: str
    ) -> str | None:
        """Return a Portuguese validation error, or None for valid input."""
        if not name.strip():
            return "Informe seu nome."
        if not _EMAIL_PATTERN.fullmatch(email.strip()):
            return "Informe um e-mail válido."
        if len(password) < 8:
            return "A senha deve possuir pelo menos 8 caracteres."
        if password != confirmation:
            return "As senhas não coincidem."
        return None

    def register(self, name: str, email: str, password: str, confirmation: str) -> AuthResult:
        """Create a temporary user for the current application session."""
        error = self.validate_registration(name, email, password, confirmation)
        if error:
            return AuthResult(False, error)

        normalized_email = self.normalize_email(email)
        if normalized_email in self.users:
            return AuthResult(False, "Já existe uma conta com este e-mail.")

        salt, password_hash = _hash_password(password)
        record = {
            "name": name.strip(),
            "email": normalized_email,
            "salt": salt,
            "password_hash": password_hash,
        }
        self.users[normalized_email] = record
        return AuthResult(True, "Cadastro demonstrativo concluído.", self.public_user(record))

    def authenticate(self, email: str, password: str) -> AuthResult:
        """Authenticate an available demonstration user."""
        record = self.users.get(self.normalize_email(email))
        if not record or not password:
            return AuthResult(False, "E-mail ou senha inválidos.")

        salt = bytes.fromhex(str(record["salt"]))
        _, supplied_hash = _hash_password(password, salt)
        if not hmac.compare_digest(supplied_hash, str(record["password_hash"])):
            return AuthResult(False, "E-mail ou senha inválidos.")

        return AuthResult(True, "Login realizado com sucesso.", self.public_user(record))

    def has_user(self, email: str) -> bool:
        """Return whether the normalized e-mail exists locally."""
        return self.normalize_email(email) in self.users

    def reset_password(self, email: str, password: str, confirmation: str) -> AuthResult:
        """Replace a local password after the simulated recovery step."""
        normalized_email = self.normalize_email(email)
        record = self.users.get(normalized_email)
        if record is None:
            return AuthResult(False, "Não foi possível redefinir a senha.")
        if len(password) < 8:
            return AuthResult(False, "A senha deve possuir pelo menos 8 caracteres.")
        if password != confirmation:
            return AuthResult(False, "As senhas não coincidem.")

        salt, password_hash = _hash_password(password)
        record["salt"] = salt
        record["password_hash"] = password_hash
        return AuthResult(True, "Senha demonstrativa redefinida com sucesso.")
