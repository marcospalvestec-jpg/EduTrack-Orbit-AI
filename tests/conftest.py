"""Configurações e fixtures compartilhadas do pytest."""

import sys
from pathlib import Path
import pytest

# Adiciona a raiz do projeto ao sys.path para garantir imports nos testes
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


@pytest.fixture
def sample_settings_dict() -> dict[str, str]:
    """Fixture com valores padrão de teste para configurações."""
    return {
        "app_name": "EduTrack Orbit AI",
        "app_slogan": "Organize, acompanhe e evolua",
        "environment": "test",
        "default_language": "pt-BR",
    }
