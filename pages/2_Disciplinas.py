"""Disciplinas management page view."""

import streamlit as st
from src.core.auth_session import render_session_sidebar, require_authenticated
from src.core.metrics import calculate_subject_progress
from src.models.subject import Subject
from src.services.simulated_data import SimulatedDataService
from src.ui.components import render_header
from src.ui.theme import inject_custom_css

# Page Configuration & Style Injection
st.set_page_config(page_title="Disciplinas - EduTrack Orbit AI", page_icon="📚", layout="wide")
inject_custom_css()
user = require_authenticated()
render_session_sidebar(user)

service = SimulatedDataService()
subjects = service.get_subjects()
tasks = service.get_tasks()

render_header(
    title="Gerenciamento de Disciplinas",
    description="Visualize suas matérias ativas, professores, carga horária e progresso por disciplina.",
    icon="📚",
)

# Sidebar form to create a new subject
with st.sidebar:
    st.markdown("### ➕ Nova Disciplina")
    with st.form("form_add_subject", clear_on_submit=True):
        new_name = st.text_input("Nome da Disciplina", placeholder="Ex: Física II")
        new_code = st.text_input("Código", placeholder="Ex: FIS102")
        new_prof = st.text_input("Professor(a)", placeholder="Ex: Prof. Roberto")
        new_workload = st.number_input("Carga Horária (h)", min_value=10, max_value=200, value=60)
        new_color = st.color_picker("Cor da Disciplina", value="#1A3644")

        submitted = st.form_submit_button("Cadastrar Disciplina", width="stretch")
        if submitted:
            if new_name and new_code:
                sub = Subject(
                    name=new_name,
                    code=new_code,
                    professor=new_prof or "Não informado",
                    workload_hours=int(new_workload),
                    color_hex=new_color,
                )
                service.add_subject(sub)
                st.success(f"Disciplina '{new_name}' adicionada com sucesso!")
                st.rerun()
            else:
                st.error("Preencha o Nome e o Código da disciplina.")

# Display Subject Cards
if not subjects:
    st.info("Nenhuma disciplina cadastrada.")
else:
    cols = st.columns(2)
    for index, subj in enumerate(subjects):
        col = cols[index % 2]
        prog = calculate_subject_progress(tasks, subj.id)

        with col:
            with st.container():
                st.markdown(
                    f"""
                    <div style="border-left: 6px solid {subj.color_hex}; padding-left: 12px; margin-bottom: 8px;">
                        <h3 style="margin: 0; color: #1A3644;">{subj.name} ({subj.code})</h3>
                        <p style="margin: 4px 0; color: #64748B;">👨‍🏫 {subj.professor} • ⏱️ {subj.workload_hours}h de Carga Horária</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"**Progresso na Matéria:** {prog['completion_rate']}% ({prog['completed_tasks']}/{prog['total_tasks']} tarefas)"
                )
                st.progress(float(prog["completion_rate"]) / 100.0)

                c_p1, c_p2, c_p3 = st.columns(3)
                c_p1.metric("Total", prog["total_tasks"])
                c_p2.metric("Pendentes", prog["pending_tasks"])
                c_p3.metric("Atrasadas", prog["overdue_tasks"])
                st.divider()
