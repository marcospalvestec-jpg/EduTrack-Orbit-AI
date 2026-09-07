# Proposal: Initial Streamlit Prototype for EduTrack AI

## Executive Summary
This proposal establishes the foundational project structure and initial interactive web prototype for **EduTrack AI**, an educational application built using Python and Streamlit. The prototype will use simulated academic data (subjects, tasks, deadlines, and status) to provide a rich student experience across Dashboard, Subject (Disciplinas), and Task (Tarefas) management pages prior to backend integration with Xano.

## Why
EduTrack AI aims to help Brazilian students manage multiple academic subjects, organize tasks and deadlines, and track performance visually. Creating a fully modular Streamlit prototype with simulated data allows immediate user interface feedback, verification of design tokens, and validation of business calculations before connecting live REST APIs.

## Scope of Changes

### Included
1. **Project Configuration & Dependencies**:
   - `pyproject.toml`: Modern Python project configuration specifying Python >= 3.12, Ruff, Pytest, Pandas, Streamlit, and ReportLab dependencies.
   - `requirements.txt`: Pinning project dependencies.
   - `.streamlit/config.toml`: Base Streamlit theme configuration adhering to EduTrack visual identity.

2. **Modular Architecture Structure**:
   - `app.py`: Application entry point with navigation sidebar and global theme styling initialization.
   - `pages/`: Multi-page layout:
     - `pages/1_Dashboard.py`: Academic overview metrics, progress indicators, upcoming deadlines, status distribution chart, and subject workload breakdown.
     - `pages/2_Disciplinas.py`: Subject management interface (list, filter, details, creation form simulation).
     - `pages/3_Tarefas.py`: Academic task management (status updates, filters by subject/status/deadline, interactive task lists).
   - `src/models/`: Domain dataclasses (`Subject`, `Task`, `TaskStatus`, `TaskPriority`).
   - `src/services/`: `SimulatedDataService` providing mock data for subjects and tasks with initial state management.
   - `src/core/`: Business calculation logic (`metrics.py` for completion %, workload, overdue counts, `filters.py` for dynamic multi-criteria filtering using Pandas).
   - `src/ui/`: Reusable UI modules (`theme.py` for petroleum blue visual identity & light/dark CSS tokens, `components.py` for rounded cards & badge chips, `charts.py` for Plotly/Altair/Streamlit accessible charts).

3. **Visual Identity & Theme Support**:
   - **Primary Color**: Petroleum Blue (`#1A3644` / `#0F2537`)
   - **Progress & Intelligence**: Purple (`#7C3AED`)
   - **Completed**: Green (`#10B981`)
   - **Attention / Pending**: Orange (`#F59E0B`)
   - **Overdue**: Red (`#EF4444`)
   - Clean, academic design with rounded cards, readable typography, responsive layouts, and dual light/dark mode styling.

4. **Automated Testing & Linting**:
   - Initial unit tests under `tests/` (`test_models.py`, `test_metrics.py`, `test_filters.py`, `test_simulated_data.py`).
   - Ruff configuration in `pyproject.toml` and validation commands (`ruff check .`, `ruff format --check .`, `pytest`).

### Non-Goals
- Integration with Xano REST API or XanoScript schemas (deferred to subsequent changes).
- Real authentication/JWT handling (Simulated user session only).
- Generating downloadable PDF reports (deferred to future feature task).
- Deploying to Streamlit Community Cloud or committing/pushing git commits (no external actions allowed).

## Capabilities Affected
- `streamlit-prototype`: Initial prototype capability covering navigation, multi-page layout, simulated data service, progress metrics, task filters, responsive CSS theme injection, and unit test suite.

## Risks and Dependencies
- **Streamlit Session State**: Simulated data updates (e.g., toggling task completion) rely on `st.session_state` persistence across page navigation.
- **Color Contrast Accessibility**: Ensure petroleum blue, green, purple, orange, and red palette colors maintain strong contrast against both light and dark backgrounds.
