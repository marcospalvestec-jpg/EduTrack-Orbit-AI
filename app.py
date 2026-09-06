"""EduTrack Orbit AI - Entrypoint Principal da Aplicação Streamlit.

Ponto de entrada do sistema que inicializa a aplicação, configurações
e validação da fundação técnica do projeto.
"""

import sys
from pathlib import Path

# Garantir que a raiz do projeto esteja no sys.path para imports absolutos
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from app.core.config import get_settings


def main() -> None:
    """Função principal de inicialização da aplicação."""
    settings = get_settings()

    st.set_page_config(
        page_title=f"{settings.app_name} | Início",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="auto",
    )

    st.title(f"🎓 {settings.app_name}")
    st.caption(f"_{settings.app_slogan}_ — v{settings.app_version}")

    st.divider()

    st.success(
        "🚀 **Fundação Técnica Estabelecida com Sucesso!**\n\n"
        "A estrutura modular do projeto Python 3.12+ com Streamlit e OpenSpec está pronta para "
        "as próximas fases de integração de autenticação e regras de negócio."
    )

    with st.expander("ℹ️ Detalhes da Fundação", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Ambiente:** `{settings.environment}`")
            st.markdown(f"**Idioma Padrão:** `{settings.default_language}`")
        with col2:
            st.markdown("**Stack:** `Python 3.12+ | Streamlit | Xano`")
            st.markdown("**Governança:** `OpenSpec + Spec-Driven`")


if __name__ == "__main__":
    main()
