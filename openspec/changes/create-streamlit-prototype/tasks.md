# Tasks: Initial Streamlit Prototype Implementation

## Task List

- [ ] **Phase 1: Environment & Project Configuration Setup**
  - [ ] 1.1 Create `pyproject.toml` with Python 3.12+ configuration, Ruff, Pytest, Pandas, Streamlit, and ReportLab settings.
  - [ ] 1.2 Create `requirements.txt` listing exact runtime and development dependencies.
  - [ ] 1.3 Create `.streamlit/config.toml` for base Streamlit settings (theme configuration, font, client settings).

- [ ] **Phase 2: Data Models & Simulated Data Layer**
  - [ ] 2.1 Create `src/__init__.py`, `src/models/__init__.py`, `src/models/subject.py`, and `src/models/task.py` with dataclasses and enums (`TaskStatus`, `TaskPriority`).
  - [ ] 2.2 Create `src/services/__init__.py` and `src/services/simulated_data.py` with `SimulatedDataService` generating realistic Brazilian academic subjects and tasks synced with `st.session_state`, using deterministic sample data for reproducible tests.

- [ ] **Phase 3: Core Calculations & Business Logic**
  - [ ] 3.1 Create `src/core/__init__.py` and `src/core/metrics.py` for dashboard aggregation calculations (completion %, total subjects, pending/overdue counts).
  - [ ] 3.2 Create `src/core/filters.py` with Pandas DataFrame filtering logic (filtering by subject, status, deadline, and keyword search).

- [ ] **Phase 4: Theme Styling & Reusable UI Components**
  - [ ] 4.1 Create `src/ui/__init__.py` and `src/ui/theme.py` with custom CSS injection for petroleum blue identity, purple progress, green completed, orange attention, red overdue, light/dark responsiveness, and rounded cards.
  - [ ] 4.2 Create `src/ui/components.py` with rounded metric cards, status chips, and header components.
  - [ ] 4.3 Create `src/ui/charts.py` with accessible, high-contrast charts (status distribution, subject task progress).

- [ ] **Phase 5: Entrypoint & Streamlit Pages**
  - [ ] 5.1 Create `app.py` with global CSS initialization, sidebar header, user info, and multi-page routing configuration.
  - [ ] 5.2 Create `pages/1_Dashboard.py` render function displaying overall metrics, progress bar, chart visualizations, and urgent deadlines.
  - [ ] 5.3 Create `pages/2_Disciplinas.py` displaying subject cards, workload overview, and interactive subject creation form modal/sidebar.
  - [ ] 5.4 Create `pages/3_Tarefas.py` displaying task filter controls, interactive task list with status badges, and completion toggle checkboxes.

- [ ] **Phase 6: Automated Testing & Verification**
  - [ ] 6.1 Create `tests/__init__.py`, `tests/test_models.py`, `tests/test_metrics.py`, `tests/test_filters.py`, and `tests/test_simulated_data.py`.
  - [ ] 6.2 Execute validation suite (`ruff check .`, `ruff format --check .`, `pytest`) and report empirical test results.
