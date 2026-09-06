"""Testes automatizados da fundação técnica do EduTrack Orbit AI.

Valida:
1. Integridade de importação de todos os subpacotes do app
2. Resolução de configurações centrais
3. Inicialização limpa do app.py via AppTest do Streamlit
"""

import importlib
from pathlib import Path

from streamlit.testing.v1 import AppTest

from app.core.config import Settings, get_settings


def test_package_imports() -> None:
    """Valida se todos os submódulos da arquitetura modular são importáveis."""
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
        assert mod is not None, f"Falha ao importar o módulo {module_name}"


def test_core_settings() -> None:
    """Valida o carregamento e integridade do modelo de configurações."""
    settings = get_settings()
    assert isinstance(settings, Settings)
    assert settings.app_name == "EduTrack Orbit AI"
    assert settings.app_slogan == "Organize, acompanhe e evolua"
    assert settings.default_language == "pt-BR"
    assert settings.app_version == "0.1.0"


def test_app_initialization_with_apptest() -> None:
    """Valida que o entrypoint app.py inicializa sem exceções via AppTest."""
    app_path = Path(__file__).resolve().parent.parent / "app.py"
    at = AppTest.from_file(str(app_path), default_timeout=10)
    at.run()

    # Verifica que não ocorreram exceções na execução do script
    assert not at.exception, f"Exceção detectada na inicialização do app.py: {at.exception}"
    # Verifica que o título foi renderizado
    assert len(at.title) > 0
    assert "EduTrack Orbit AI" in at.title[0].value
