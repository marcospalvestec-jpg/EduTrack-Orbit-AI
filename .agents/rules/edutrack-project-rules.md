---
trigger: always_on
---

# EduTrack Rules

Stack: Python 3.12+, Streamlit, Xano REST API, XanoScript, Pandas, ReportLab, Pytest, OpenSpec and Git. Do not use FlutterFlow.

Before editing, read AGENTS.md and the active OpenSpec proposal. Present a short plan and change only the approved scope.

Keep Streamlit pages focused on UI. Put business logic in `src/core`, API access in `src/services`, reusable UI in `src/ui` and models in `src/models`.

Follow PEP 8, use type hints and avoid duplicated code. Catch specific exceptions. Never use `eval`, `exec` or bare `except`.

Never hardcode or expose passwords, tokens, API keys or Xano URLs. Use `.streamlit/secrets.toml`, which must never be committed. Each user may access only their own data.

Before completion, run Ruff and Pytest and report the real results. Never claim an unexecuted test passed.

Never delete files, install packages, commit, push or deploy without explicit user approval.