# Design Document: Initial Streamlit Prototype for EduTrack AI

## Technical Architecture Overview

EduTrack AI is designed as a modular Python web application powered by Streamlit. This initial prototype introduces a clean separation of concerns across presentation, business logic, domain models, and data access services.

```
EduTrack/
├── app.py                      # Main entrypoint & multi-page router / header
├── pages/                      # Streamlit navigation pages
│   ├── 1_Dashboard.py          # Dashboard view with metrics and charts
│   ├── 2_Disciplinas.py        # Subjects list & creation view
│   └── 3_Tarefas.py            # Tasks list with interactive filters & checkboxes
├── src/
│   ├── core/                   # Core business rules & computations
│   │   ├── __init__.py
│   │   ├── metrics.py          # Aggregations, completion %, overdue counts
│   │   └── filters.py          # Pandas-backed dynamic task filtering
│   ├── models/                 # Dataclasses & Enums
│   │   ├── __init__.py
│   │   ├── subject.py          # Subject dataclass
│   │   └── task.py             # Task dataclass, TaskStatus & TaskPriority enums
│   ├── services/               # Data access provider abstraction
│   │   ├── __init__.py
│   │   └── simulated_data.py   # Mock data provider & session state sync
│   └── ui/                     # Presentation styling & components
│       ├── __init__.py
│       ├── theme.py            # Visual identity CSS injection & color tokens
│       ├── components.py       # Custom rounded cards, metric badges, UI widgets
│       └── charts.py           # Streamlit native & Plotly accessible charts
├── tests/                      # Automated test suite
│   ├── test_models.py
│   ├── test_metrics.py
│   ├── test_filters.py
│   └── test_simulated_data.py
├── .streamlit/
│   └── config.toml             # Streamlit configuration settings
├── pyproject.toml              # Tooling configuration (Ruff, Pytest)
└── requirements.txt            # Dependency specification
```

## Visual Identity System & Design Tokens

### Color Palette
- **Primary Color**: Petroleum Blue (`#1A3644` / `#0F2537` accent: `#2C4C5E`) - Header, active navigation, primary action buttons.
- **Progress & Intelligence**: Purple (`#7C3AED` / `#8B5CF6`) - Progress bars, AI insights callouts, overall percentage metric.
- **Completed**: Green (`#10B981` / `#059669`) - Completed badges, success indicators, high score metrics.
- **Attention / Pending**: Orange (`#F59E0B` / `#D97706`) - Pending tasks, warning badges, upcoming deadlines within 3 days.
- **Overdue**: Red (`#EF4444` / `#DC2626`) - Overdue alert badges, urgent tasks.

### CSS Injection & Custom Styling (`src/ui/theme.py`)
Streamlit elements are styled via a centralized `inject_custom_css()` function that defines CSS custom properties for both light mode (`@media (prefers-color-scheme: light)`) and dark mode (`@media (prefers-color-scheme: dark)`):

```css
:root {
  --primary-petroleum: #1a3644;
  --color-purple: #7c3aed;
  --color-green: #10b981;
  --color-orange: #f59e0b;
  --color-red: #ef4444;
  --card-bg: #ffffff;
  --card-border: rgba(0, 0, 0, 0.08);
  --card-radius: 14px;
}
```

### Rounded Card Components (`src/ui/components.py`)
- `card(title, value, subtitle, border_color)`: Reusable metric card wrapped in HTML/CSS container.
- `status_chip(status)`: Colored badge chips indicating status (Pendente, Em Andamento, Concluída, Atrasada).

## Data Models (`src/models/`)

### Task Dataclass & Enums (`src/models/task.py`)
```python
from enum import Enum
from dataclasses import dataclass
from datetime import date
from typing import Optional


class TaskStatus(str, Enum):
    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDA = "Concluída"
    ATRASADA = "Atrasada"


class TaskPriority(str, Enum):
    BAIXA = "Baixa"
    MEDIA = "Média"
    ALTA = "Alta"


@dataclass
class Task:
    id: str
    subject_id: str
    subject_name: str
    title: str
    description: str
    due_date: date
    status: TaskStatus
    priority: TaskPriority
    weight: float = 1.0
```

### Subject Dataclass (`src/models/subject.py`)
```python
@dataclass
class Subject:
    id: str
    name: str
    code: str
    professor: str
    workload_hours: int
    color_hex: str
```

## Simulated Data Service (`src/services/simulated_data.py`)
- Initializes subjects and tasks in `st.session_state` if not present.
- Provides CRUD helper methods (`get_subjects()`, `get_tasks()`, `toggle_task_status()`, `add_subject()`, `add_task()`).
- Automatically updates task status to `ATRASADA` if `due_date < date.today()` and status is not `CONCLUIDA`.

## Core Logic & Aggregation (`src/core/`)
- `calculate_dashboard_metrics(tasks, subjects)` returns dict with:
  - `total_subjects`: count of subjects
  - `total_tasks`: count of tasks
  - `completed_tasks`: count of completed tasks
  - `pending_tasks`: count of pending tasks
  - `overdue_tasks`: count of overdue tasks
  - `overall_completion_rate`: float percentage `0.0` to `100.0`
- `filter_tasks(df_tasks, subject_ids, statuses, deadline_filter, search_query)` returns a filtered Pandas DataFrame.

## Testing & Quality Assurance Plan
- `pytest` executes unit tests under `tests/`.
- `ruff check .` validates code quality and PEP 8 standards.
- `ruff format --check .` validates formatting compliance.
