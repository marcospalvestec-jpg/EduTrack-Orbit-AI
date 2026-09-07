"""Configurações centrais do EduTrack Orbit AI.

Gerencia o carregamento de variáveis de ambiente com resolução hierárquica:
1. Streamlit Secrets (st.secrets)
2. Variáveis de ambiente (.env via python-dotenv / os.environ)
3. Valores padrão de desenvolvimento
"""

import os
from dataclasses import dataclass
from functools import lru_cache

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


@dataclass(frozen=True)
class Settings:
    """Configurações da aplicação com validação de tipo."""

    app_name: str = "EduTrack Orbit AI"
    app_slogan: str = "Organize, acompanhe e evolua"
    app_version: str = "0.1.0"
    environment: str = "development"
    xano_api_base_url: str = ""
    xano_api_key: str = ""
    default_language: str = "pt-BR"
    is_development: bool = True


def _read_secret(key: str, default: str = "") -> str:
    """Lê um segredo/variável com fallback seguro entre st.secrets e os.environ.

    Args:
        key: Nome da variável a ser consultada.
        default: Valor padrão caso a chave não seja encontrada.

    Returns:
        Valor da configuração resolvida.
    """
    # 1. Tentar ler do streamlit secrets se o módulo streamlit estiver disponível
    try:
        import streamlit as st

        # Procura formato snake_case ou minúsculo
        lower_key = key.lower()
        if hasattr(st, "secrets") and lower_key in st.secrets:
            return str(st.secrets[lower_key])
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass

    # 2. Tentar ler de os.environ
    return os.environ.get(key, os.environ.get(key.upper(), default))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Retorna a instância singleton de configurações da aplicação.

    Returns:
        Settings: Objeto com as configurações carregadas.
    """
    env = _read_secret("ENVIRONMENT", "development").lower()
    return Settings(
        app_name=_read_secret("APP_NAME", "EduTrack Orbit AI"),
        app_slogan=_read_secret("APP_SLOGAN", "Organize, acompanhe e evolua"),
        app_version=_read_secret("APP_VERSION", "0.1.0"),
        environment=env,
        xano_api_base_url=_read_secret("XANO_API_BASE_URL", ""),
        xano_api_key=_read_secret("XANO_API_KEY", ""),
        default_language=_read_secret("DEFAULT_LANGUAGE", "pt-BR"),
        is_development=(env == "development"),
    )
