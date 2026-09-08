"""Disciplinas management page view."""

from html import escape

import streamlit as st
from src.core.auth_session import render_session_sidebar, require_authenticated
from src.core.metrics import calculate_subject_progress
from src.models.subject import Subject
from src.services.data_service import data_service_for_user, load_academic_data
from src.services.xano import XanoError
from src.ui.components import render_header
from src.ui.theme import inject_custom_css

# Page Configuration & Style Injection
st.set_page_config(page_title="Disciplinas - EduTrack Orbit AI", page_icon="📚", layout="wide")
inject_custom_css()
user = require_authenticated()
render_session_sidebar(user)

service = data_service_for_user(user)
subjects, tasks = load_academic_data(service)

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
                try:
                    service.add_subject(sub)
                except XanoError as error:
                    st.error(f"Não foi possível cadastrar: {error}")
                else:
                    st.success(f"Disciplina '{new_name}' adicionada com sucesso!")
                    st.rerun()
            else:
                st.error("Preencha o Nome e o Código da disciplina.")

# Display Subject Cards
if not subjects:
    st.info("Você ainda não cadastrou disciplinas. Use o formulário no menu lateral para começar.")
else:
    cols = st.columns(2)
    for index, subj in enumerate(subjects):
        col = cols[index % 2]
        prog = calculate_subject_progress(tasks, subj.id)
        safe_name = escape(subj.name)
        safe_code = escape(subj.code)
        safe_professor = escape(subj.professor)
        safe_color = subj.color_hex if subj.color_hex.startswith("#") else "#1A3644"

        with col:
            with st.container():
                st.markdown(
                    f"""
                    <div style="border-left: 6px solid {safe_color}; padding-left: 12px; margin-bottom: 8px;">
                        <h3 style="margin: 0;">{safe_name} ({safe_code})</h3>
                        <p style="margin: 4px 0;">👨‍🏫 {safe_professor} • ⏱️ {subj.workload_hours}h de Carga Horária</p>
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

                details_tab, edit_tab, delete_tab = st.tabs(["Detalhes", "Editar", "Excluir"])
                with details_tab:
                    st.write(f"Código: **{subj.code}**")
                    st.write(f"Professor(a): **{subj.professor}**")
                    st.write(f"Carga horária: **{subj.workload_hours} horas**")

                with edit_tab:
                    with st.form(f"edit_subject_{subj.id}"):
                        edit_name = st.text_input("Nome", value=subj.name)
                        edit_code = st.text_input("Código", value=subj.code)
                        edit_professor = st.text_input("Professor(a)", value=subj.professor)
                        edit_workload = st.number_input(
                            "Carga horária (h)",
                            min_value=10,
                            max_value=200,
                            value=subj.workload_hours,
                        )
                        edit_color = st.color_picker("Cor", value=subj.color_hex)
                        save_subject = st.form_submit_button(
                            "Salvar alterações", type="primary", width="stretch"
                        )
                    if save_subject:
                        if edit_name.strip() and edit_code.strip():
                            try:
                                service.update_subject(
                                    subj.id,
                                    name=edit_name.strip(),
                                    code=edit_code.strip(),
                                    professor=edit_professor.strip() or "Não informado",
                                    workload_hours=int(edit_workload),
                                    color_hex=edit_color,
                                )
                            except XanoError as error:
                                st.error(f"Não foi possível atualizar: {error}")
                            else:
                                st.success("Disciplina atualizada.")
                                st.rerun()
                        else:
                            st.error("Nome e código são obrigatórios.")

                with delete_tab:
                    linked_tasks = prog["total_tasks"]
                    st.warning(f"A exclusão também removerá {linked_tasks} tarefa(s) vinculada(s).")
                    confirm_delete = st.checkbox(
                        "Confirmo a exclusão desta disciplina",
                        key=f"confirm_subject_{subj.id}",
                    )
                    if st.button(
                        "Excluir disciplina",
                        key=f"delete_subject_{subj.id}",
                        disabled=not confirm_delete,
                        width="stretch",
                    ):
                        try:
                            service.delete_subject(subj.id)
                        except XanoError as error:
                            st.error(f"Não foi possível excluir: {error}")
                        else:
                            st.success("Disciplina excluída.")
                            st.rerun()
                st.divider()
