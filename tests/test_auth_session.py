"""Tests for authentication session state transitions."""

from src.core.auth_session import (
    AUTH_USER_KEY,
    AUTH_USERS_KEY,
    RECOVERY_EMAIL_KEY,
    current_user,
    initialize_auth_state,
    sign_in,
    sign_out,
)


def test_initialize_auth_state_preserves_existing_values():
    state = {AUTH_USERS_KEY: {"existing": {}}, AUTH_USER_KEY: {"name": "A", "email": "a@b.c"}}

    initialize_auth_state(state)

    assert "existing" in state[AUTH_USERS_KEY]
    assert current_user(state) == {"name": "A", "email": "a@b.c"}
    assert state[RECOVERY_EMAIL_KEY] is None


def test_sign_in_and_sign_out_transitions():
    state = {}
    user = {"name": "Marcos", "email": "marcos@example.com"}

    sign_in(state, user)
    assert current_user(state) == user

    state[RECOVERY_EMAIL_KEY] = "marcos@example.com"
    sign_out(state)
    assert current_user(state) is None
    assert state[RECOVERY_EMAIL_KEY] is None
    assert AUTH_USERS_KEY in state
