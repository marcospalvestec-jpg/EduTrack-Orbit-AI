"""Accessible, high-contrast chart visualizers using Plotly / Streamlit."""

import plotly.graph_objects as go
import streamlit as st

from src.models.subject import Subject
from src.models.task import Task, TaskStatus


def render_status_pie_chart(tasks: list[Task]) -> None:
    """Render an accessible donut chart showing task status distribution."""
    if not tasks:
        st.info("Nenhuma tarefa disponível para exibir o gráfico.")
        return

    status_counts = {
        TaskStatus.CONCLUIDA.value: sum(1 for t in tasks if t.status == TaskStatus.CONCLUIDA),
        TaskStatus.EM_ANDAMENTO.value: sum(1 for t in tasks if t.status == TaskStatus.EM_ANDAMENTO),
        TaskStatus.PENDENTE.value: sum(1 for t in tasks if t.status == TaskStatus.PENDENTE),
        TaskStatus.ATRASADA.value: sum(
            1 for t in tasks if t.status == TaskStatus.ATRASADA or t.is_overdue
        ),
    }

    labels = [k for k, v in status_counts.items() if v > 0]
    values = [v for k, v in status_counts.items() if v > 0]

    color_map = {
        TaskStatus.CONCLUIDA.value: "#10B981",  # Green
        TaskStatus.EM_ANDAMENTO.value: "#7C3AED",  # Purple
        TaskStatus.PENDENTE.value: "#F59E0B",  # Orange
        TaskStatus.ATRASADA.value: "#EF4444",  # Red
    }

    colors = [color_map[label] for label in labels]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.5,
                marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
                textinfo="percent+label",
                textposition="inside",
                hoverinfo="label+value+percent",
            )
        ]
    )

    fig.update_layout(
        title="Distribuição de Tarefas por Status",
        margin=dict(t=40, b=10, l=10, r=10),
        height=320,
        autosize=True,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, width="stretch", config={"responsive": True})


def render_subject_workload_chart(subjects: list[Subject], tasks: list[Task]) -> None:
    """Render horizontal bar chart showing workload hours and tasks per subject."""
    if not subjects:
        st.info("Nenhuma disciplina disponível para o gráfico de carga horária.")
        return

    subject_names = [s.name for s in subjects]
    workloads = [s.workload_hours for s in subjects]
    task_counts = [sum(1 for t in tasks if t.subject_id == s.id) for s in subjects]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=subject_names,
            x=workloads,
            name="Carga Horária (h)",
            orientation="h",
            marker=dict(color="#1A3644", cornerradius=4),
        )
    )

    fig.add_trace(
        go.Bar(
            y=subject_names,
            x=task_counts,
            name="Qtd. de Tarefas",
            orientation="h",
            marker=dict(color="#7C3AED", cornerradius=4),
        )
    )

    fig.update_layout(
        title="Carga Horária e Tarefas por Disciplina",
        barmode="group",
        height=340,
        autosize=True,
        margin=dict(t=40, b=10, l=10, r=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, width="stretch", config={"responsive": True})
