# EduTrack AI — Agent Guide

## Project

EduTrack AI is a responsive educational web application for students to manage subjects, academic tasks, deadlines and study progress.

The application language is Brazilian Portuguese.

## Official architecture

- Frontend: Python and Streamlit
- Backend: Xano REST API
- Backend schemas: XanoScript
- Data processing: Pandas
- PDF reports: ReportLab
- Tests: Pytest
- Lint and formatting: Ruff
- Specifications: OpenSpec
- Version control: Git and GitHub
- Deployment: Streamlit Community Cloud

FlutterFlow is not part of the current architecture.

## Source of truth

Before implementing a change, read:

1. `docs/especificacao-de-negocio.md`
2. The active proposal inside `openspec/changes/`
3. This `AGENTS.md`

The files in `docs/` describe the course and business requirements. OpenSpec defines the approved implementation scope.

## Initial product scope

The MVP is intended for students and must provide:

- authentication;
- subject management;
- academic task management;
- dashboard metrics;
- filters by subject, status and deadline;
- progress calculation;
- weekly PDF reports.

The first prototype must use simulated data before integration with Xano.

## Code organization

- `app.py`: application entry point
- `pages/`: Streamlit pages
- `src/core/`: business rules and calculations
- `src/models/`: data models
- `src/services/`: Xano API communication
- `src/ui/`: reusable interface components
- `tests/`: automated tests
- `docs/`: course and business documentation

## Visual identity

- Primary: petroleum blue
- Progress and intelligence: purple
- Completed: green
- Attention: orange
- Overdue: red
- Modern, academic and clean interface
- Light and dark themes
- Rounded cards
- Accessible and easy-to-read charts

## Security

Never expose passwords, tokens, API keys or Xano URLs. Use `.streamlit/secrets.toml` for local secrets. Users must access only their own subjects and tasks.

## Validation

Before completing an implementation:

1. Run `ruff check .`
2. Run `ruff format --check .`
3. Run `pytest`
4. Report the real results
5. Wait for approval before commit, push or deploy