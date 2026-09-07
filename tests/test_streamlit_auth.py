"""Integration tests for the demonstration authentication UI."""

from pathlib import Path

from src.services.demo_auth import DEMO_EMAIL, DEMO_PASSWORD
from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_demo_login_opens_authenticated_home():
    app = AppTest.from_file(PROJECT_ROOT / "app.py", default_timeout=15).run()

    assert not app.exception
    app.text_input[0].input(DEMO_EMAIL)
    app.text_input[1].input(DEMO_PASSWORD)
    app.button[0].click().run()

    assert not app.exception
    assert app.session_state["auth_current_user"]["email"] == DEMO_EMAIL
    assert any(item.value == "EduTrack Orbit AI" for item in app.title)


def test_protected_pages_stop_without_login():
    for path in ["pages/1_Dashboard.py", "pages/2_Disciplinas.py", "pages/3_Tarefas.py"]:
        app = AppTest.from_file(PROJECT_ROOT / path, default_timeout=15).run()

        assert not app.exception
        assert any("Faça login" in warning.value for warning in app.warning)


def test_protected_pages_render_with_authenticated_session():
    for path in ["pages/1_Dashboard.py", "pages/2_Disciplinas.py", "pages/3_Tarefas.py"]:
        app = AppTest.from_file(PROJECT_ROOT / path, default_timeout=15)
        app.session_state["auth_current_user"] = {
            "name": "Estudante Demo",
            "email": DEMO_EMAIL,
        }
        app.session_state["auth_demo_users"] = {}
        app.session_state["auth_recovery_email"] = None
        app.run()

        assert not app.exception
        assert any(button.label == "Sair" for button in app.button)
