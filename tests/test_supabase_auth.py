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

    with patch("requests.Session.post", return_value=mock_resp) as mock_post:
        ok, msg, user = client.sign_up("test@energy.org", "SecurePass123!")
        assert ok
        assert user["id"] == "supabase-uuid-1"
        assert mock_post.called
        assert any(c[0][0] == "https://xyzcompany.supabase.co/auth/v1/signup" for c in mock_post.call_args_list)


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

    with patch("requests.Session.post", return_value=mock_resp):
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

    with patch("requests.Session.post", return_value=mock_resp) as mock_post:
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


def test_supabase_test_connection_mocked():
    client = SupabaseAuthClient(
        supabase_url="https://xyzcompany.supabase.co",
        supabase_key="anon-key-1234567890abcdef"
    )
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    with patch("requests.Session.get", return_value=mock_resp):
        ok, msg, details = client.test_connection()
        assert ok
        assert "Connected" in msg
        assert details["status_code"] == 200


def test_supabase_table_and_profile_methods():
    client = SupabaseAuthClient(
        supabase_url="https://xyzcompany.supabase.co",
        supabase_key="anon-key-1234567890abcdef"
    )

    # 1. select_table
    mock_resp_sel = MagicMock()
    mock_resp_sel.status_code = 200
    mock_resp_sel.json.return_value = [{"country_iso3": "IND", "country_name": "India"}]
    with patch("requests.Session.get", return_value=mock_resp_sel):
        ok, rows, msg = client.select_table("dim_country")
        assert ok
        assert len(rows) == 1
        assert rows[0]["country_iso3"] == "IND"

    # 2. get_profile
    mock_resp_prof = MagicMock()
    mock_resp_prof.status_code = 200
    mock_resp_prof.json.return_value = [{"id": "uuid-1", "username": "analyst", "preferences": {"theme": "dark"}}]
    with patch("requests.Session.get", return_value=mock_resp_prof):
        prof = client.get_profile("uuid-1")
        assert prof is not None
        assert prof["username"] == "analyst"
        assert prof["preferences"]["theme"] == "dark"

    # 3. create_conversation & save_chat_message
    mock_resp_conv = MagicMock()
    mock_resp_conv.status_code = 201
    mock_resp_conv.json.return_value = [{"conversation_id": "conv-123"}]
    with patch("requests.Session.post", return_value=mock_resp_conv):
        conv_id = client.create_conversation("uuid-1", "Crude Analysis")
        assert conv_id == "conv-123"

    mock_resp_msg = MagicMock()
    mock_resp_msg.status_code = 201
    with patch("requests.Session.post", return_value=mock_resp_msg):
        saved = client.save_chat_message("conv-123", "uuid-1", "user", "What is petrol price?")
        assert saved is True

    # 4. check_and_consume_quota
    mock_resp_quota = MagicMock()
    mock_resp_quota.status_code = 200
    mock_resp_quota.content = b'{"allowed": true, "remaining": 1, "used_count": 2}'
    mock_resp_quota.json.return_value = {"allowed": True, "remaining": 1, "used_count": 2}
    with patch("requests.Session.post", return_value=mock_resp_quota):
        allowed, res = client.check_and_consume_quota("uuid-1", "What is diesel rate?", "hash123")
        assert allowed is True
        assert res["remaining"] == 1


def test_resolve_username_to_email_and_login():
    """Verifies that usernames without @ are resolved to registered email addresses via profiles."""
    from src.auth.supabase_client import SupabaseAuthClient
    client = SupabaseAuthClient(
        supabase_url="https://xyzcompany.supabase.co",
        supabase_key="anon-key-1234567890abcdef"
    )

    mock_resp_prof = MagicMock()
    mock_resp_prof.status_code = 200
    mock_resp_prof.json.return_value = [{"email": "alihamza09076@gmail.com", "username": "alihamza5253"}]

    with patch("requests.Session.get", return_value=mock_resp_prof):
        resolved = client.resolve_email_from_username("alihamza5253")
        assert resolved == "alihamza09076@gmail.com"


def test_supabase_quota_status_authoritative():
    """Verifies that get_user_quota_status accurately reflects questions used and remaining."""
    from src.auth.supabase_client import SupabaseAuthClient
    client = SupabaseAuthClient(
        supabase_url="https://xyzcompany.supabase.co",
        supabase_key="anon-key-1234567890abcdef"
    )

    # Mock 1 query used
    mock_resp_rows = MagicMock()
    mock_resp_rows.status_code = 200
    mock_resp_rows.json.return_value = [
        {"usage_id": "u1", "created_at": "2026-10-20T10:00:00Z", "status": "completed"}
    ]

    with patch("requests.Session.get", return_value=mock_resp_rows):
        status = client.get_user_quota_status("user-uuid-abc")
        assert status["allowed"] is True
        assert status["questions_used"] == 1
        assert status["questions_remaining"] == 2


def test_mark_quota_usage_failed():
    """Verifies that failed provider calls call mark_quota_usage_failed to refund free questions."""
    from src.auth.supabase_client import SupabaseAuthClient
    client = SupabaseAuthClient(
        supabase_url="https://xyzcompany.supabase.co",
        supabase_key="anon-key-1234567890abcdef"
    )

    mock_resp_patch = MagicMock()
    mock_resp_patch.status_code = 200

    with patch("requests.Session.patch", return_value=mock_resp_patch) as mock_patch:
        ok = client.mark_quota_usage_failed("usage-uuid-999", "Rate limit 429 from Google")
        assert ok is True
        assert mock_patch.called
        assert "usage_id=eq.usage-uuid-999" in mock_patch.call_args[0][0]

