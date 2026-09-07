"""Unit tests for SimulatedDataService state management."""

from src.services.simulated_data import SimulatedDataService


def test_simulated_data_service_initialization():
    """Test service initialization in plain python environment."""
    service = SimulatedDataService(use_session_state=False)
    subjects = service.get_subjects()
    tasks = service.get_tasks()

    assert len(subjects) >= 4
    assert len(tasks) >= 8


def test_simulated_data_service_toggle_task_status():
    """Test toggling task completion state."""
    service = SimulatedDataService(use_session_state=False)
    tasks = service.get_tasks()
    first_task = tasks[0]
    initial_status = first_task.status

    toggled = service.toggle_task_status(first_task.id)
    assert toggled is not None
    assert toggled.status != initial_status
