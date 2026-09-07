"""Pandas-backed dynamic filtering module for tasks."""

from datetime import date, timedelta

import pandas as pd

from src.models.task import Task, TaskStatus


def tasks_to_dataframe(tasks: list[Task]) -> pd.DataFrame:
    """Convert list of Task models to a structured Pandas DataFrame."""
    if not tasks:
        return pd.DataFrame(
            columns=[
                "id",
                "title",
                "subject_id",
                "subject_name",
                "due_date",
                "status",
                "priority",
                "description",
                "weight",
            ]
        )

    records = [t.to_dict() for t in tasks]
    df = pd.DataFrame(records)
    if "due_date" in df.columns:
        df["due_date"] = pd.to_datetime(df["due_date"]).dt.date
    return df


def filter_tasks_dataframe(
    df: pd.DataFrame,
    subject_ids: list[str] | None = None,
    statuses: list[str] | None = None,
    deadline_filter: str = "Todas",
    search_query: str = "",
    reference_date: date | None = None,
) -> pd.DataFrame:
    """Filter task DataFrame dynamically by subject, status, deadline window, and search string."""
    if df.empty:
        return df

    filtered = df.copy()
    ref = reference_date or date.today()

    # Filter by subject IDs
    if subject_ids:
        filtered = filtered[filtered["subject_id"].isin(subject_ids)]

    # Filter by statuses
    if statuses:
        filtered = filtered[filtered["status"].isin(statuses)]

    # Filter by search query
    if search_query and search_query.strip():
        q = search_query.strip().lower()
        title_match = filtered["title"].str.lower().str.contains(q, na=False)
        desc_match = filtered["description"].str.lower().str.contains(q, na=False)
        subj_match = filtered["subject_name"].str.lower().str.contains(q, na=False)
        filtered = filtered[title_match | desc_match | subj_match]

    # Filter by deadline criteria
    if deadline_filter == "Atrasadas":
        filtered = filtered[
            (filtered["due_date"] < ref) & (filtered["status"] != TaskStatus.CONCLUIDA.value)
        ]
    elif deadline_filter == "Hoje":
        filtered = filtered[filtered["due_date"] == ref]
    elif deadline_filter == "Esta Semana":
        week_end = ref + timedelta(days=7)
        filtered = filtered[(filtered["due_date"] >= ref) & (filtered["due_date"] <= week_end)]
    elif deadline_filter == "Próximos 14 dias":
        fortnight_end = ref + timedelta(days=14)
        filtered = filtered[(filtered["due_date"] >= ref) & (filtered["due_date"] <= fortnight_end)]

    return filtered
