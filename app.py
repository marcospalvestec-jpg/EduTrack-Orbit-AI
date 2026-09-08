"""EduTrack Orbit AI - Entry Point & Navigation Layout."""

import streamlit as st
from src.core.auth_session import current_user, initialize_auth_state, render_session_sidebar
from src.services.demo_auth import DEMO_EMAIL
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
service = SimulatedDataService(
    user_id=user["email"],
    seed_demo=user["email"] == DEMO_EMAIL,
)
render_session_sidebar(user)

# Sidebar Navigation Header & User Info
with st.sidebar:
    st.title("EduTrack Orbit AI")
    st.caption("Organize, acompanhe e evolua")
    st.divider()

    if st.button("Carregar dados demonstrativos", width="stretch"):
        service.reset_to_defaults()
        st.success("Dados demonstrativos carregados.")
        st.rerun()

    if subjects := service.get_subjects():
        if st.button("Limpar meus dados", width="stretch"):
            st.session_state["confirm_clear_data"] = True
        if st.session_state.get("confirm_clear_data"):
            st.warning(f"Isso excluirá {len(subjects)} disciplina(s) e todas as tarefas.")
            confirm, cancel = st.columns(2)
            if confirm.button("Confirmar", type="primary", width="stretch"):
                service.clear_all()
                st.session_state["confirm_clear_data"] = False
                st.rerun()
            if cancel.button("Cancelar", width="stretch"):
                st.session_state["confirm_clear_data"] = False
                st.rerun()

# Main Entry Landing / Dashboard Overview
subjects = service.get_subjects()
tasks = service.get_tasks()

render_header(
    title="Bem-vindo ao EduTrack Orbit AI",
    description="Seu painel central para acompanhar disciplinas, prazos e métricas de desempenho acadêmico.",
    icon="🚀",
)

if not subjects:
    st.info(
        "Sua conta está pronta. Cadastre a primeira disciplina ou carregue dados demonstrativos pelo menu lateral."
    )
    action_subject, action_demo = st.columns(2)
    with action_subject:
        if st.button("Cadastrar primeira disciplina", type="primary", width="stretch"):
            st.switch_page("pages/2_Disciplinas.py")
    with action_demo:
        if st.button("Explorar com dados de exemplo", width="stretch"):
            service.reset_to_defaults()
            st.rerun()

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown(f"### Olá, {user['name'].split()[0]} 👋")
    if tasks:
        pending = [task for task in tasks if task.status.value != "Concluída"]
        pending.sort(key=lambda task: task.due_date)
        if pending:
            next_task = pending[0]
            st.markdown(f"**Próxima entrega:** {next_task.title}")
            st.caption(f"{next_task.subject_name} · {next_task.due_date.strftime('%d/%m/%Y')}")
        else:
            st.success("Todas as tarefas cadastradas estão concluídas.")
    else:
        st.caption("Adicione tarefas para visualizar aqui suas próximas entregas.")

    quick_subject, quick_task, quick_dashboard = st.columns(3)
    if quick_subject.button("Nova disciplina", width="stretch"):
        st.switch_page("pages/2_Disciplinas.py")
    if quick_task.button("Nova tarefa", width="stretch", disabled=not subjects):
        st.switch_page("pages/3_Tarefas.py")
    if quick_dashboard.button("Ver dashboard", width="stretch"):
        st.switch_page("pages/1_Dashboard.py")

with col2:
    st.markdown("### 📊 Status Rápido")
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.status.value == "Concluída")
    rate = round((completed_tasks / total_tasks * 100.0), 1) if total_tasks > 0 else 0.0

    st.metric("Total de Disciplinas", len(subjects))
    st.metric("Total de Tarefas", total_tasks)
    st.metric("Taxa Global de Conclusão", f"{rate}%")
