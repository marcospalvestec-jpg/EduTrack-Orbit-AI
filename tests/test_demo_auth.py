"""Tests for the in-memory demonstration authentication service."""

from src.services.demo_auth import DEMO_EMAIL, DEMO_PASSWORD, DemoAuthService


def test_demo_account_authenticates_without_storing_plain_password():
    users = {}
    service = DemoAuthService(users)

    result = service.authenticate(DEMO_EMAIL, DEMO_PASSWORD)

    assert result.success is True
    assert result.user == {"name": "Estudante Demo", "email": DEMO_EMAIL}
    assert "password" not in users[DEMO_EMAIL]
    assert users[DEMO_EMAIL]["password_hash"] != DEMO_PASSWORD


def test_registration_normalizes_email_and_authenticates():
    users = {}
    service = DemoAuthService(users)

    registered = service.register("Marcos Alves", "  MARCOS@example.com ", "Senha@123", "Senha@123")
    authenticated = service.authenticate("marcos@example.com", "Senha@123")

    assert registered.success is True
    assert authenticated.success is True
    assert authenticated.user == {"name": "Marcos Alves", "email": "marcos@example.com"}


def test_registration_rejects_invalid_and_duplicate_data():
    service = DemoAuthService({})

    assert service.register("", "invalido", "curta", "outra").message == "Informe seu nome."
    assert (
        service.register("Nome", "invalido", "Senha@123", "Senha@123").message
        == "Informe um e-mail válido."
    )
    assert (
        service.register("Nome", "nome@example.com", "curta", "curta").message
        == "A senha deve possuir pelo menos 8 caracteres."
    )
    assert (
        service.register("Nome", "nome@example.com", "Senha@123", "Senha@456").message
        == "As senhas não coincidem."
    )
    assert service.register("Nome", "nome@example.com", "Senha@123", "Senha@123").success
    assert not service.register("Nome", "nome@example.com", "Senha@123", "Senha@123").success


def test_invalid_login_uses_generic_message():
    service = DemoAuthService({})

    missing = service.authenticate("unknown@example.com", "Senha@123")
    wrong = service.authenticate(DEMO_EMAIL, "SenhaErrada")

    assert missing.message == "E-mail ou senha inválidos."
    assert wrong.message == missing.message


def test_password_reset_updates_existing_account():
    service = DemoAuthService({})

    assert service.has_user(DEMO_EMAIL)
    assert not service.has_user("unknown@example.com")
    reset = service.reset_password(DEMO_EMAIL, "NovaSenha@123", "NovaSenha@123")

    assert reset.success is True
    assert not service.authenticate(DEMO_EMAIL, DEMO_PASSWORD).success
    assert service.authenticate(DEMO_EMAIL, "NovaSenha@123").success


def test_password_reset_validates_password_and_account():
    service = DemoAuthService({})

    assert not service.reset_password(
        "unknown@example.com", "NovaSenha@123", "NovaSenha@123"
    ).success
    assert not service.reset_password(DEMO_EMAIL, "curta", "curta").success
    assert not service.reset_password(DEMO_EMAIL, "NovaSenha@123", "OutraSenha@123").success
