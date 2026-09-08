"""Tarefas management page view with filters and status toggle."""

from datetime import date, timedelta

import streamlit as st
from src.core.auth_session import render_session_sidebar, require_authenticated
from src.core.filters import filter_tasks_dataframe, tasks_to_dataframe
from src.models.task import Task, TaskPriority, TaskStatus
from src.services.data_service import data_service_for_user, load_academic_data
from src.ui.components import render_header, render_status_chip
from src.ui.theme import inject_custom_css

# Page Configuration & Style Injection
st.set_page_config(page_title="Tarefas - EduTrack Orbit AI", page_icon="📝", layout="wide")
inject_custom_css()
user = require_authenticated()
render_session_sidebar(user)

service = data_service_for_user(user)
subjects, tasks = load_academic_data(service)

render_header(
    title="Gerenciamento de Tarefas",
    description="Filtre suas entregas por disciplina, status ou data. Marque como concluídas conforme avança.",
    icon="📝",
)

# Sidebar Form to Add New Task
with st.sidebar:
    st.markdown("### ➕ Nova Tarefa")
    with st.form("form_add_task", clear_on_submit=True):
        t_title = st.text_input("Título da Tarefa", placeholder="Ex: Exercícios 1 a 10")
        subject_options = {s.name: s.id for s in subjects}
        t_subj_name = st.selectbox(
            "Disciplina", options=list(subject_options.keys()) if subjects else ["Nenhuma"]
        )
        t_due = st.date_input("Data de Entrega", value=date.today() + timedelta(days=3))
        t_priority = st.selectbox("Prioridade", options=[p.value for p in TaskPriority], index=1)
        t_desc = st.text_area("Descrição", placeholder="Instruções ou observações...")

        task_submitted = st.form_submit_button("Cadastrar Tarefa", width="stretch")
        if task_submitted:
            if t_title and subjects and t_subj_name in subject_options:
                s_id = subject_options[t_subj_name]
                new_t = Task(
                    title=t_title,
                    subject_id=s_id,
                    subject_name=t_subj_name,
                    due_date=t_due,
                    priority=TaskPriority(t_priority),
                    description=t_desc,
                )
                service.add_task(new_t)
                st.success(f"Tarefa '{t_title}' adicionada!")
                st.rerun()
            else:
                st.error("Preencha o título e selecione uma disciplina válida.")

# Interactive Filter Controls
st.markdown("### 🔍 Filtros e Busca")

f_col1, f_col2, f_col3, f_col4 = st.columns([3, 3, 2, 4])

with f_col1:
    selected_subjs = st.multiselect(
        "Filtrar por Disciplina",
        options=[s.name for s in subjects],
        default=[],
        placeholder="Todas as disciplinas",
    )
    subj_id_map = {s.name: s.id for s in subjects}
    selected_subj_ids = [subj_id_map[name] for name in selected_subjs]

with f_col2:
    selected_statuses = st.multiselect(
        "Filtrar por Status",
        options=[st_item.value for st_item in TaskStatus],
        default=[],
        placeholder="Todos os status",
    )

with f_col3:
    deadline_filter = st.selectbox(
        "Prazo",
        options=["Todas", "Atrasadas", "Hoje", "Esta Semana", "Próximos 14 dias"],
        index=0,
    )

with f_col4:
    search_query = st.text_input(
        "🔍 Buscar por palavra-chave", placeholder="Buscar no título ou descrição..."
    )

# Convert to DataFrame & Apply Filters
df_tasks = tasks_to_dataframe(tasks)
df_filtered = filter_tasks_dataframe(
    df=df_tasks,
    subject_ids=selected_subj_ids if selected_subj_ids else None,
    statuses=selected_statuses if selected_statuses else None,
    deadline_filter=deadline_filter,
    search_query=search_query,
)

st.markdown(f"**Tarefas Encontradas:** `{len(df_filtered)}` de `{len(tasks)}` total")
st.divider()

# Render Task List Container Cards
if not tasks:
    if subjects:
        st.info(
            "Nenhuma tarefa cadastrada. Use o formulário no menu lateral para criar a primeira."
        )
    else:
        st.info("Cadastre uma disciplina antes de adicionar tarefas.")
        if st.button("Ir para Disciplinas", type="primary"):
            st.switch_page("pages/2_Disciplinas.py")
elif df_filtered.empty:
    st.info("Nenhuma tarefa corresponde aos filtros selecionados.")
else:
    for idx, row in df_filtered.iterrows():
        t_id = str(row["id"])
        is_done = row["status"] == TaskStatus.CONCLUIDA.value

        with st.container():
            c1, c2, c3, c4, c5 = st.columns([1, 4, 2, 2, 2])

            with c1:
                checked = st.checkbox(
                    "Concluída",
                    value=is_done,
                    key=f"check_{t_id}",
                    label_visibility="collapsed",
                )
                if checked != is_done:
                    service.toggle_task_status(t_id)
                    st.rerun()

            with c2:
                title_fmt = f"~~{row['title']}~~" if is_done else f"**{row['title']}**"
                st.markdown(title_fmt)
                st.caption(f"📚 {row['subject_name']} • {row['description']}")

            with c3:
                due_val = row["due_date"]
                due_str = (
                    due_val.strftime("%d/%m/%Y") if hasattr(due_val, "strftime") else str(due_val)
                )
                st.markdown(f"📅 **Prazo:** {due_str}")

            with c4:
                st.markdown(f"⚡ **Prioridade:** {row['priority']}")

            with c5:
                st.markdown(render_status_chip(row["status"]), unsafe_allow_html=True)

            with st.expander("Editar ou excluir"):
                edit_tab, delete_tab = st.tabs(["Editar", "Excluir"])
                task = service.get_task_by_id(t_id)
                if task is None:
                    st.error("Tarefa não encontrada.")
                    continue

                with edit_tab:
                    subject_names = [subject.name for subject in subjects]
                    current_subject_index = (
                        subject_names.index(task.subject_name)
                        if task.subject_name in subject_names
                        else 0
                    )
                    with st.form(f"edit_task_{t_id}"):
                        edit_title = st.text_input("Título", value=task.title)
                        edit_subject_name = st.selectbox(
                            "Disciplina", subject_names, index=current_subject_index
                        )
                        edit_due = st.date_input("Prazo", value=task.due_date)
                        status_values = [status.value for status in TaskStatus]
                        priority_values = [priority.value for priority in TaskPriority]
                        edit_status = st.selectbox(
                            "Status",
                            status_values,
                            index=status_values.index(task.status.value),
                        )
                        edit_priority = st.selectbox(
                            "Prioridade",
                            priority_values,
                            index=priority_values.index(task.priority.value),
                        )
                        edit_description = st.text_area("Descrição", value=task.description)
                        save_task = st.form_submit_button(
                            "Salvar alterações", type="primary", width="stretch"
                        )
                    if save_task:
                        if not edit_title.strip():
                            st.error("O título é obrigatório.")
                        else:
                            selected_subject = next(
                                subject for subject in subjects if subject.name == edit_subject_name
                            )
                            service.update_task(
                                t_id,
                                title=edit_title.strip(),
                                subject_id=selected_subject.id,
                                subject_name=selected_subject.name,
                                due_date=edit_due,
                                status=TaskStatus(edit_status),
                                priority=TaskPriority(edit_priority),
                                description=edit_description.strip(),
                            )
                            st.success("Tarefa atualizada.")
                            st.rerun()

                with delete_tab:
                    st.warning("Esta ação não pode ser desfeita.")
                    confirm_delete = st.checkbox(
                        "Confirmo a exclusão desta tarefa",
                        key=f"confirm_task_{t_id}",
                    )
                    if st.button(
                        "Excluir tarefa",
                        key=f"delete_task_{t_id}",
                        disabled=not confirm_delete,
                        width="stretch",
                    ):
                        service.delete_task(t_id)
                        st.success("Tarefa excluída.")
                        st.rerun()

            st.divider()
