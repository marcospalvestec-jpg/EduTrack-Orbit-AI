"""Student profile and local account security page."""

import streamlit as st
from src.core.auth_session import (
    AUTH_USERS_KEY,
    render_session_sidebar,
    require_authenticated,
    update_current_user_name,
)
from src.services.demo_auth import DemoAuthService
from src.ui.components import render_header
from src.ui.theme import inject_custom_css

st.set_page_config(page_title="Meu Perfil - EduTrack Orbit AI", page_icon="👤", layout="wide")
inject_custom_css()
user = require_authenticated()
render_session_sidebar(user)

render_header(
    title="Meu Perfil",
    description="Consulte seus dados e mantenha sua conta atualizada.",
    icon="👤",
)

details_tab, edit_tab, security_tab = st.tabs(["Dados da conta", "Editar perfil", "Segurança"])

with details_tab:
    col_name, col_email = st.columns(2)
    col_name.metric("Nome", user["name"])
    col_email.metric("E-mail", user["email"])
    st.info("A senha fica protegida e nunca é exibida. Você pode substituí-la na aba Segurança.")

with edit_tab:
    with st.form("profile_name_form"):
        new_name = st.text_input("Nome completo", value=user["name"])
        save_name = st.form_submit_button("Salvar nome", type="primary", width="stretch")
    if save_name:
        updated = update_current_user_name(st.session_state, new_name)
        if updated:
            st.success("Perfil atualizado.")
            st.rerun()
        else:
            st.error("Informe um nome válido.")

with security_tab:
    st.markdown("### Alterar senha")
    st.caption("A senha atual não é exibida por segurança.")
    with st.form("profile_password_form", clear_on_submit=True):
        new_password = st.text_input("Nova senha", type="password")
        confirm_password = st.text_input("Confirmar nova senha", type="password")
        save_password = st.form_submit_button("Alterar senha", type="primary", width="stretch")
    if save_password:
        service = DemoAuthService(st.session_state[AUTH_USERS_KEY])
        result = service.reset_password(user["email"], new_password, confirm_password)
        if result.success:
            st.success("Senha alterada com sucesso.")
        else:
            st.error(result.message)
