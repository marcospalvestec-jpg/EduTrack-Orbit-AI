"""Tests for the Xano authentication adapter."""

from src.services.xano import XanoAuthService, configured_xano_base_url


def test_configured_xano_base_url_uses_environment(monkeypatch):
    monkeypatch.setenv("XANO_API_BASE_URL", "https://example.xano.io/api:test/")

    assert configured_xano_base_url() == "https://example.xano.io/api:test"


def test_xano_authenticate_validates_token_with_profile(monkeypatch):
    service = XanoAuthService("https://example.xano.io/api:test")
    calls = []

    def fake_request(method, path, *, payload=None, token=None):
        calls.append((method, path, payload, token))
        if path == "auth/login":
            return {"authToken": "private-token"}
        return {
            "id": 4,
            "name": "Marcos Alves",
            "email": "marcos@example.com",
            "role": "member",
        }

    monkeypatch.setattr(service.client, "request", fake_request)

    response = service.authenticate("MARCOS@example.com", "secret123")

    assert response.result.success
    assert response.token == "private-token"
    assert response.result.user == {
        "id": 4,
        "name": "Marcos Alves",
        "email": "marcos@example.com",
        "role": "member",
    }
    assert calls == [
        (
            "POST",
            "auth/login",
            {"email": "marcos@example.com", "password": "secret123"},
            None,
        ),
        ("GET", "auth/me", None, "private-token"),
    ]


def test_xano_register_rejects_mismatched_passwords():
    service = XanoAuthService("https://example.xano.io/api:test")

    response = service.register("Marcos Alves", "marcos@example.com", "secret123", "different123")

    assert not response.result.success
    assert response.token is None
    assert response.result.message == "As senhas não coincidem."
