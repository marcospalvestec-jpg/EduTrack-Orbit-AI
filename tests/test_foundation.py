"""Testes automatizados da fundaÃ§Ã£o tÃ©cnica do EduTrack Orbit AI.

Valida:
1. Integridade de importaÃ§Ã£o de todos os subpacotes do app
2. ResoluÃ§Ã£o de configuraÃ§Ãµes centrais
3. InicializaÃ§Ã£o limpa do app.py via AppTest do Streamlit
"""

import importlib
from pathlib import Path

from app.core.config import Settings, get_settings
from streamlit.testing.v1 import AppTest


def test_package_imports() -> None:
    """Valida se todos os submÃ³dulos da arquitetura modular sÃ£o importÃ¡veis."""
    modules = [
        "app",
        "app.api",
        "app.components",
        "app.core",
        "app.core.config",
        "app.i18n",
        "app.models",
        "app.services",
        "app.styles",
        "app.utils",
        "app.views",
    ]
    for module_name in modules:
        mod = importlib.import_module(module_name)
        assert mod is not None, f"Falha ao importar o mÃ³dulo {module_name}"


def test_core_settings() -> None:
    """Valida o carregamento e integridade do modelo de configuraÃ§Ãµes."""
    settings = get_settings()
    assert isinstance(settings, Settings)
    assert settings.app_name == "EduTrack Orbit AI"
    assert settings.app_slogan == "Organize, acompanhe e evolua"
    assert settings.default_language == "pt-BR"
    assert settings.app_version == "0.1.0"


def test_app_initialization_with_apptest() -> None:
    """Valida que o entrypoint app.py inicializa sem exceÃ§Ãµes via AppTest."""
    app_path = Path(__file__).resolve().parent.parent / "app.py"
    at = AppTest.from_file(str(app_path), default_timeout=10)
    at.run()

    # Verifica que nÃ£o ocorreram exceÃ§Ãµes na execuÃ§Ã£o do script
    assert not at.exception, f"ExceÃ§Ã£o detectada na inicializaÃ§Ã£o do app.py: {at.exception}"
    # Verifica que o tÃ­tulo foi renderizado
    assert len(at.markdown) > 0
    assert any("EduTrack Orbit AI" in item.value for item in at.markdown)
