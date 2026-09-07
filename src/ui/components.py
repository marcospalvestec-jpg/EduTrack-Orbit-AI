"""Reusable UI widgets and rounded metric cards."""

import streamlit as st

from src.models.task import TaskStatus


def render_header(title: str, description: str, icon: str = "🎓") -> None:
    """Render a styled header banner with EduTrack visual identity."""
    html = f"""
    <div class="edutrack-header-banner">
        <h1 class="edutrack-header-title">{icon} {title}</h1>
        <p class="edutrack-header-desc">{description}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_metric_card(
    title: str,
    value: str | int | float,
    subtitle: str | None = None,
    color_accent: str | None = None,
) -> None:
    """Render a rounded metric card with custom styling."""
    accent_style = f"color: {color_accent};" if color_accent else ""
    subtitle_html = f'<div class="edutrack-card-subtitle">{subtitle}</div>' if subtitle else ""

    html = f"""
    <div class="edutrack-card">
        <div class="edutrack-card-title">{title}</div>
        <div class="edutrack-card-value" style="{accent_style}">{value}</div>
        {subtitle_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_status_chip(status: TaskStatus | str) -> str:
    """Return HTML string for status chip badge."""
    val = status.value if isinstance(status, TaskStatus) else str(status)

    css_class = "chip-pendente"
    if val == TaskStatus.CONCLUIDA.value:
        css_class = "chip-concluid"
    elif val == TaskStatus.EM_ANDAMENTO.value:
        css_class = "chip-andamento"
    elif val == TaskStatus.ATRASADA.value:
        css_class = "chip-atrasada"

    return f'<span class="edutrack-chip {css_class}">{val}</span>'
