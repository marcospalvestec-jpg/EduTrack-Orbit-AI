"""EduTrack Orbit AI - Entry Point & Navigation Layout."""

import streamlit as st
from src.core.auth_session import current_user, initialize_auth_state, render_session_sidebar
from src.services.simulated_data import SimulatedDataService
from src.ui.auth import render_auth_portal
from src.ui.components import render_header
from src.ui.theme import inject_custom_css

# Page Configuration
st.set_page_config(
    page_title="EduTrack Orbit AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Custom Visual Identity CSS
inject_custom_css()
initialize_auth_state(st.session_state)

user = current_user(st.session_state)
if user is None:
    render_header(
        title="EduTrack Orbit AI",
        description="Organize, acompanhe e evolua",
        icon="🎓",
    )
    render_auth_portal()
    st.stop()

# Initialize Simulated Data Service (persisted in st.session_state)
service = SimulatedDataService()
render_session_sidebar(user)

# Sidebar Navigation Header & User Info
with st.sidebar:
    st.title("EduTrack Orbit AI")
    st.caption("Organize, acompanhe e evolua")
    st.divider()

    st.markdown("### Perfil do Estudante")
    st.markdown(f"**Aluno:** {user['name']}")
    st.markdown("**Curso:** Ciência da Computação")
    st.markdown("**Semestre:** 2026.2")
    st.divider()

    st.markdown("### 💡 Dica da Semana")
    st.info("Mantenha suas tarefas de Cálculo I em dia para garantir bom desempenho no simulado!")
    st.divider()

    if st.button("🔄 Restaurar Dados Demonstrativos", width="stretch"):
        service.reset_to_defaults()
        st.success("Dados restaurados!")
        st.rerun()

# Main Entry Landing / Dashboard Overview
subjects = service.get_subjects()
tasks = service.get_tasks()

render_header(
    title="Bem-vindo ao EduTrack Orbit AI",
    description="Seu painel central para acompanhar disciplinas, prazos e métricas de desempenho acadêmico.",
    icon="🚀",
)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📌 Guia Rápido de Navegação")
    st.markdown(
        """
        Utilize o menu lateral para navegar entre as seções:
        - **1. Dashboard**: Visão geral de métricas, gráficos de progresso e tarefas urgentes.
        - **2. Disciplinas**: Gerencie suas matérias, professores e carga horária.
        - **3. Tarefas**: Organize e filtre pendências por matéria, status e data de entrega.
        """
    )

with col2:
    st.markdown("### 📊 Status Rápido")
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.status.value == "Concluída")
    rate = round((completed_tasks / total_tasks * 100.0), 1) if total_tasks > 0 else 0.0

    st.metric("Total de Disciplinas", len(subjects))
    st.metric("Total de Tarefas", total_tasks)
    st.metric("Taxa Global de Conclusão", f"{rate}%")
