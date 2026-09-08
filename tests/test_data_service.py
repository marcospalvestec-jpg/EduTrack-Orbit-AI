"""Tests for the staged Xano academic-data integration."""

from datetime import date

from src.models.subject import Subject
from src.services.data_service import XanoSubjectDataService


def test_xano_subjects_maps_paginated_response(monkeypatch):
    service = XanoSubjectDataService(
        "https://example.xano.io/api:test",
        "token",
        "student@example.com",
        use_session_state=False,
    )

    monkeypatch.setattr(
        service.client,
        "request",
        lambda *args, **kwargs: {
            "items": [
                {
                    "id": 7,
                    "name": "Banco de Dados",
                    "code": "BD2026",
                    "professor": "Prof. Evandro",
                    "workload_hours": 80,
                    "color_hex": "#7C3AED",
                }
            ]
        },
    )

    subjects = service.get_subjects()

    assert len(subjects) == 1
    assert subjects[0].id == 7
    assert subjects[0].name == "Banco de Dados"


def test_xano_subject_create_sends_authenticated_payload(monkeypatch):
    service = XanoSubjectDataService(
        "https://example.xano.io/api:test",
        "private-token",
        "student@example.com",
        use_session_state=False,
    )
    captured = {}

    def fake_request(method, path, *, payload=None, token=None):
        captured.update(method=method, path=path, payload=payload, token=token)
        return {"id": 8, **payload}

    monkeypatch.setattr(service.client, "request", fake_request)
    created = service.add_subject(
        Subject(
            "Algoritmos",
            "AED",
            "Prof. Ana",
            60,
            "#123456",
            "Estruturas de dados",
            date(2026, 8, 3),
            date(2026, 12, 18),
        )
    )

    assert created.id == 8
    assert captured == {
        "method": "POST",
        "path": "subjects",
        "payload": {
            "name": "Algoritmos",
            "code": "AED",
            "professor": "Prof. Ana",
            "workload_hours": 60,
            "description": "Estruturas de dados",
            "start_date": "2026-08-03",
            "end_date": "2026-12-18",
            "color_hex": "#123456",
        },
        "token": "private-token",
    }
