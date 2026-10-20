"""
Unit tests for Supabase Authentication and Client Adapter in Global FuelPulse AI.
Tests:
- SupabaseAuthClient configuration detection.
- Sign up, sign in, get_user, and sign out requests.
- RPC function calls.
- AuthService fallback and integration with Supabase client.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.auth.supabase_client import SupabaseAuthClient
from src.auth.auth_service import AuthService, DEFAULT_DEMO_USERNAME, DEFAULT_DEMO_PASSWORD


def test_supabase_client_unconfigured():
    client = SupabaseAuthClient(supabase_url="", supabase_key="")
    assert not client.is_configured()

    ok, msg, user = client.sign_up("test@example.com", "Password123!")
    assert not ok
    assert "not configured" in msg

    ok, msg, token, user_dict = client.sign_in_with_password("test@example.com", "Password123!")
    assert not ok
    assert "not configured" in msg


def test_supabase_client_configured_properties():
    client = SupabaseAuthClient(
        supabase_url="https://xyzcompany.supabase.co",
        supabase_key="anon-key-1234567890abcdef",
        service_role_key="service-role-secret-999"
    )
    assert client.is_configured()
    assert client.url == "https://xyzcompany.supabase.co"
    assert client.anon_key == "anon-key-1234567890abcdef"
    assert client.service_role_key == "service-role-secret-999"


def test_supabase_sign_up_mocked():
    client = SupabaseAuthClient(
        supabase_url="https://xyzcompany.supabase.co",
        supabase_key="anon-key-1234567890abcdef"
    )

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.content = b'{"user": {"id": "supabase-uuid-1", "email": "test@energy.org"}}'
    mock_resp.json.return_value = {
        "user": {
            "id": "supabase-uuid-1",
            "email": "test@energy.org"
        }
    }

    with patch("requests.post", return_value=mock_resp) as mock_post:
        ok, msg, user = client.sign_up("test@energy.org", "SecurePass123!")
        assert ok
        assert user["id"] == "supabase-uuid-1"
        assert mock_post.called
        assert mock_post.call_args[0][0] == "https://xyzcompany.supabase.co/auth/v1/signup"


def test_supabase_sign_in_mocked():
    client = SupabaseAuthClient(
        supabase_url="https://xyzcompany.supabase.co",
        supabase_key="anon-key-1234567890abcdef"
    )

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.content = b'{"access_token": "mock-sb-token-xyz"}'
    mock_resp.json.return_value = {
        "access_token": "mock-sb-token-xyz",
        "user": {
            "id": "supabase-uuid-2",
            "email": "trader@fuelpulse.ai",
            "user_metadata": {
                "username": "supertrader",
                "full_name": "Senior Energy Trader"
            }
        }
    }

    with patch("requests.post", return_value=mock_resp):
        ok, msg, token, user_dict = client.sign_in_with_password("trader@fuelpulse.ai", "SecretPass2026!")
        assert ok
        assert token == "mock-sb-token-xyz"
        assert user_dict["user_id"] == "supabase-uuid-2"
        assert user_dict["username"] == "supertrader"
        assert user_dict["full_name"] == "Senior Energy Trader"


def test_supabase_rpc_call_mocked():
    client = SupabaseAuthClient(
        supabase_url="https://xyzcompany.supabase.co",
        supabase_key="anon-key-1234567890abcdef"
    )

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.content = b'{"allowed": true, "remaining": 2, "used_count": 1}'
    mock_resp.json.return_value = {"allowed": True, "remaining": 2, "used_count": 1}

    with patch("requests.post", return_value=mock_resp) as mock_post:
        ok, result = client.call_rpc(
            "check_and_consume_ai_quota",
            {"p_user_id": "supabase-uuid-1", "p_question_text": "Brent crude price?"}
        )
        assert ok
        assert result["allowed"] is True
        assert result["remaining"] == 2


def test_auth_service_demo_login_always_works_locally():
    # Ensures demo account bypasses cloud even if Supabase is active
    AuthService.ensure_default_demo_user()
    ok, msg, token, user_dict = AuthService.login_user(DEFAULT_DEMO_USERNAME, DEFAULT_DEMO_PASSWORD)
    assert ok
    assert user_dict["email"] == "analyst@fuelpulse.ai"
    assert token is not None

    # Validate session
    sess_user = AuthService.validate_session(token)
    assert sess_user is not None
    assert sess_user["email"] == "analyst@fuelpulse.ai"
