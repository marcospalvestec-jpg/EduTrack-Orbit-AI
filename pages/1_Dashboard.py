"""Dashboard page view with summary metrics, charts and urgent deadlines."""

import streamlit as st
from src.core.auth_session import render_session_sidebar, require_authenticated
from src.core.metrics import calculate_dashboard_metrics
from src.services.demo_auth import DEMO_EMAIL
from src.services.simulated_data import SimulatedDataService
from src.ui.charts import render_status_pie_chart, render_subject_workload_chart
from src.ui.components import render_header, render_metric_card, render_status_chip
from src.ui.theme import inject_custom_css

# Page Configuration & Style Injection
st.set_page_config(page_title="Dashboard - EduTrack Orbit AI", page_icon="📊", layout="wide")
inject_custom_css()
user = require_authenticated()
render_session_sidebar(user)

# Data Service Layer
service = SimulatedDataService(user_id=user["email"], seed_demo=user["email"] == DEMO_EMAIL)
subjects = service.get_subjects()
tasks = service.get_tasks()

metrics = calculate_dashboard_metrics(tasks, subjects)

render_header(
    title="Dashboard de Desempenho",
    description="Acompanhe suas métricas de estudo, distribuição de tarefas e entregas prioritárias.",
    icon="📊",
)

if not subjects:
    st.info("Seu dashboard será preenchido conforme você cadastrar disciplinas e tarefas.")
    action_subject, action_demo = st.columns(2)
    if action_subject.button("Cadastrar disciplina", type="primary", width="stretch"):
        st.switch_page("pages/2_Disciplinas.py")
    if action_demo.button("Carregar dados demonstrativos", width="stretch"):
        service.reset_to_defaults()
        st.rerun()

# Top KPI Metric Cards
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    render_metric_card("Disciplinas", metrics["total_subjects"], "Ativas no semestre", "#1A3644")

with c2:
    render_metric_card("Total Tarefas", metrics["total_tasks"], "Cadastradas", "#1A3644")

with c3:
    render_metric_card("Concluídas", metrics["completed_tasks"], "Entregas feitas", "#10B981")

with c4:
    render_metric_card(
        "Pendentes",
        metrics["pending_tasks"] + metrics["in_progress_tasks"],
        "A realizar",
        "#F59E0B",
    )

with c5:
    render_metric_card("Atrasadas", metrics["overdue_tasks"], "Atenção necessária", "#EF4444")

st.divider()

# Overall Progress Bar Section
st.markdown(f"### 🎯 Progresso Geral: **{metrics['completion_rate']}%**")
st.progress(float(metrics["completion_rate"]) / 100.0)

st.divider()

# Interactive Charts Row
col_left, col_right = st.columns([1, 1])

with col_left:
    render_status_pie_chart(tasks)

with col_right:
    render_subject_workload_chart(subjects, tasks)

st.divider()

# Urgent Deadlines Table
st.markdown("### ⚠️ Próximas Entregas & Tarefas Urgentes")

urgent_tasks = [t for t in tasks if t.status.value != "Concluída"]
urgent_tasks.sort(key=lambda x: x.due_date)

if not urgent_tasks:
    st.success("🎉 Nenhuma tarefa pendente ou atrasada!")
else:
    for t in urgent_tasks[:5]:
        with st.container():
            col_t1, col_t2, col_t3, col_t4 = st.columns([3, 2, 2, 1])
            with col_t1:
                st.markdown(f"**{t.title}**")
                st.caption(f"📚 {t.subject_name} • {t.description}")
            with col_t2:
                st.markdown(f"📅 **Prazo:** {t.due_date.strftime('%d/%m/%Y')}")
            with col_t3:
                st.markdown(render_status_chip(t.status), unsafe_allow_html=True)
            with col_t4:
                if st.button("Concluir", key=f"dash_done_{t.id}"):
                    service.toggle_task_status(t.id)
                    st.rerun()
            st.divider()
