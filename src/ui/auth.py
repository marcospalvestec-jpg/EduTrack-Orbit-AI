"""Streamlit components for the local demonstration authentication flow."""

from __future__ import annotations

import streamlit as st

from src.core.auth_session import (
    AUTH_USERS_KEY,
    RECOVERY_EMAIL_KEY,
    initialize_auth_state,
    sign_in,
)
from src.services.demo_auth import DEMO_EMAIL, DEMO_PASSWORD, DemoAuthService
from src.services.xano import XanoAuthService, configured_xano_base_url


def _service() -> DemoAuthService:
    initialize_auth_state(st.session_state)
    return DemoAuthService(st.session_state[AUTH_USERS_KEY])


def _render_login(service: DemoAuthService | XanoAuthService, using_xano: bool) -> None:
    if not using_xano:
        st.info(f"Conta de demonstração: **{DEMO_EMAIL}** · senha: **{DEMO_PASSWORD}**")
    with st.form("auth_login"):
        email = st.text_input("E-mail", placeholder=DEMO_EMAIL)
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar", width="stretch")

    if submitted:
        response = service.authenticate(email, password)
        result = response.result if using_xano else response
        token = response.token if using_xano else None
        if result.success and result.user:
            sign_in(st.session_state, result.user, token)
            st.success(result.message)
            st.rerun()
        st.error(result.message)


def _render_registration(service: DemoAuthService | XanoAuthService, using_xano: bool) -> None:
    with st.form("auth_register", clear_on_submit=True):
        name = st.text_input("Nome completo")
        email = st.text_input("E-mail", key="register_email")
        password = st.text_input("Senha", type="password", key="register_password")
        confirmation = st.text_input(
            "Confirmar senha", type="password", key="register_confirmation"
        )
        submitted = st.form_submit_button("Criar conta", width="stretch")

    if submitted:
        response = service.register(name, email, password, confirmation)
        result = response.result if using_xano else response
        token = response.token if using_xano else None
        if result.success and result.user:
            sign_in(st.session_state, result.user, token)
            st.success(result.message)
            st.rerun()
        st.error(result.message)


def _render_recovery(service: DemoAuthService) -> None:
    st.caption("Nenhum e-mail será enviado. A redefinição acontece apenas nesta sessão.")
    with st.form("auth_recovery"):
        email = st.text_input("E-mail da conta", key="recovery_request_email")
        requested = st.form_submit_button("Continuar", width="stretch")

    if requested:
        normalized = service.normalize_email(email)
        st.session_state[RECOVERY_EMAIL_KEY] = normalized if service.has_user(email) else None
        st.info("Se a conta estiver disponível nesta demonstração, a redefinição será liberada.")

    recovery_email = st.session_state.get(RECOVERY_EMAIL_KEY)
    if recovery_email:
        with st.form("auth_reset_password"):
            st.markdown(f"Redefinição local para **{recovery_email}**")
            password = st.text_input("Nova senha", type="password")
            confirmation = st.text_input("Confirmar nova senha", type="password")
            reset = st.form_submit_button("Redefinir senha", width="stretch")

        if reset:
            result = service.reset_password(recovery_email, password, confirmation)
            if result.success:
                st.session_state[RECOVERY_EMAIL_KEY] = None
                st.success(result.message)
            else:
                st.error(result.message)


def render_auth_portal() -> None:
    """Render login, registration and recovery forms for unauthenticated users."""
    base_url = configured_xano_base_url()
    using_xano = base_url is not None
    service = XanoAuthService(base_url) if base_url else _service()
    if using_xano:
        st.success("Conectado ao backend seguro do EduTrack.")
    else:
        st.warning(
            "Modo demonstrativo: contas e senhas ficam somente nesta sessão e não substituem o Xano."
        )
    login_tab, register_tab, recovery_tab = st.tabs(["Entrar", "Criar conta", "Recuperar senha"])
    with login_tab:
        _render_login(service, using_xano)
    with register_tab:
        _render_registration(service, using_xano)
    with recovery_tab:
        if using_xano:
            st.info(
                "A recuperação pelo Xano será ativada na próxima etapa. "
                "Por enquanto, use Entrar ou Criar conta."
            )
        else:
            _render_recovery(service)
