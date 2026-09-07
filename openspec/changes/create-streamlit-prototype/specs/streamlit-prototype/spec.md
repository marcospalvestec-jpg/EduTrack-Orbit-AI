# Spec Delta: Streamlit Prototype (`streamlit-prototype`)

## ADDED Requirements

### Requirement: Project Configuration and Infrastructure
The project SHALL configure `pyproject.toml`, `requirements.txt`, and `.streamlit/config.toml` to support Python >= 3.12, Streamlit, Pandas, ReportLab, Pytest, and Ruff tooling.

#### Scenario: Verify project configuration files exist
- **GIVEN** the repository root environment
- **WHEN** the project dependencies and configuration files are inspected
- **THEN** `pyproject.toml`, `requirements.txt`, and `.streamlit/config.toml` MUST be present with specified tool options and visual settings.

### Requirement: Multi-Page Navigation and Views
The application SHALL provide `app.py` as the entrypoint with global sidebar navigation routing to 3 distinct page views (`1_Dashboard.py`, `2_Disciplinas.py`, `3_Tarefas.py`).

#### Scenario: Navigate through multi-page application
- **GIVEN** a student launching the Streamlit app
- **WHEN** navigating between Dashboard, Disciplinas, and Tarefas pages
- **THEN** `app.py` SHALL maintain state in `st.session_state` and render the appropriate page view.

### Requirement: Modular Project Structure
The application code SHALL be organized into clean decoupled modules (`src/core/`, `src/models/`, `src/services/`, `src/ui/`, `tests/`).

#### Scenario: Inspect module separation
- **GIVEN** the EduTrack codebase
- **WHEN** inspecting business logic, models, services, and UI components
- **THEN** calculations SHALL reside in `src/core/`, dataclasses in `src/models/`, mock state provider in `src/services/`, and styling/widgets in `src/ui/`.

### Requirement: Visual Identity and Theme Support
The user interface SHALL enforce the official EduTrack visual identity with Petroleum Blue (`#1A3644`), Purple (`#7C3AED`), Green (`#10B981`), Orange (`#F59E0B`), Red (`#EF4444`), rounded cards, and responsive Light/Dark theme support in Brazilian Portuguese.

#### Scenario: Render responsive light and dark themes
- **GIVEN** the user interface rendered in Streamlit
- **WHEN** switching between Light Mode and Dark Mode
- **THEN** custom CSS variables SHALL maintain high-contrast colors, petroleum blue accents, and rounded card styling across all views.

### Requirement: Simulated Data Service
The application SHALL provide a `SimulatedDataService` generating realistic Brazilian academic subjects and tasks with session state persistence.

#### Scenario: Access simulated academic dataset
- **GIVEN** an unauthenticated or test user opening the application
- **WHEN** the simulated data service initializes
- **THEN** it SHALL generate at least 4 realistic subjects and at least 8 realistic tasks with past, present, and future deadlines across multiple statuses.

### Requirement: Core Calculations and Task Filtering
The application SHALL calculate academic metrics (completion percentage, subject progress, pending/overdue counts) in `src/core/metrics.py` and provide dynamic multi-criteria task filtering using Pandas in `src/core/filters.py`.

#### Scenario: Calculate dashboard metrics and filter tasks
- **GIVEN** a dataset of subjects and tasks
- **WHEN** metrics are computed and multi-select filters (subject, status, deadline) are applied
- **THEN** `metrics.py` SHALL return accurate completion percentages and `filters.py` SHALL return matching filtered DataFrames.

### Requirement: Validation and Automated Testing
The project SHALL include unit tests in `tests/` and support clean validation via Ruff (`ruff check .`, `ruff format --check .`) and Pytest (`pytest`).

#### Scenario: Run automated quality checks
- **GIVEN** the EduTrack test suite and source files
- **WHEN** executing Ruff linting/formatting checks and Pytest commands
- **THEN** all lint rules SHALL pass and all unit tests SHALL execute without errors.

