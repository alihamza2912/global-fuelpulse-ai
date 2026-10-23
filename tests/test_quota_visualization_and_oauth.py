"""
Comprehensive Test Suite covering:
- Test A: AI Quota Visualization (0/3 -> 1/3 -> 2/3 -> 3/3 used · 0 remaining · Quota exceeded)
- Test B: Supabase Google OAuth Flow & Configuration Inspection
- Test C: Supabase GitHub OAuth Flow & Configuration Inspection
- Test D: Complete Removal of Quick 1-Click Demo Login
"""

import uuid
import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock

from config.settings import settings
from src.auth.quota_service import QuotaService, quota_service
from src.auth.supabase_client import supabase_auth_client, SupabaseAuthClient
from src.auth.auth_service import AuthService
from src.database.connection import db_manager
from src.database.models import User, AIQuestionUsage


@pytest.fixture(autouse=True)
def clean_environment():
    """Ensure clean quota cache between tests."""
    quota_service.invalidate_cache()
    yield
    quota_service.invalidate_cache()


def test_scenario_a_exact_quota_progression_convention():
    """
    Test A — Quota:
    Verify that the badge strictly changes from:
    0/3 used · 3 remaining
    -> 1/3 used · 2 remaining
    -> 2/3 used · 1 remaining
    -> 3/3 used · 0 remaining · Quota exceeded
    and a fourth request is blocked.
    """
    uid = f"user_exact_quota_{uuid.uuid4().hex[:8]}"
    quota_service.invalidate_cache(uid)

    # 1. Before using any questions: 0/3 used · 3 remaining
    s0 = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert s0["used"] == 0
    assert s0["remaining"] == 3
    assert s0["quota_exhausted"] is False
    assert s0["badge_text"] == "0/3 used · 3 remaining"

    # 2. After using one question: 1/3 used · 2 remaining
    ok1, res1 = supabase_auth_client.check_and_consume_quota(
        user_id=uid,
        question_text="Question 1",
        question_hash=f"h1_{uuid.uuid4()}",
        request_id=f"r1_{uuid.uuid4()}"
    )
    assert ok1 is True
    s1 = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert s1["used"] == 1
    assert s1["remaining"] == 2
    assert s1["quota_exhausted"] is False
    assert s1["badge_text"] == "1/3 used · 2 remaining"

    # 3. After using two questions: 2/3 used · 1 remaining
    ok2, res2 = supabase_auth_client.check_and_consume_quota(
        user_id=uid,
        question_text="Question 2",
        question_hash=f"h2_{uuid.uuid4()}",
        request_id=f"r2_{uuid.uuid4()}"
    )
    assert ok2 is True
    s2 = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert s2["used"] == 2
    assert s2["remaining"] == 1
    assert s2["quota_exhausted"] is False
    assert s2["badge_text"] == "2/3 used · 1 remaining"

    # 4. After using three questions: 3/3 used · 0 remaining · Quota exceeded
    ok3, res3 = supabase_auth_client.check_and_consume_quota(
        user_id=uid,
        question_text="Question 3",
        question_hash=f"h3_{uuid.uuid4()}",
        request_id=f"r3_{uuid.uuid4()}"
    )
    assert ok3 is True
    s3 = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert s3["used"] == 3
    assert s3["remaining"] == 0
    assert s3["quota_exhausted"] is True
    assert s3["badge_text"] == "3/3 used · 0 remaining · Quota exceeded"

    # 5. Fourth request must be rejected
    ok4, res4 = supabase_auth_client.check_and_consume_quota(
        user_id=uid,
        question_text="Question 4",
        question_hash=f"h4_{uuid.uuid4()}",
        request_id=f"r4_{uuid.uuid4()}"
    )
    assert ok4 is False
    s4 = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert s4["used"] == 3
    assert s4["remaining"] == 0
    assert s4["quota_exhausted"] is True
    assert s4["badge_text"] == "3/3 used · 0 remaining · Quota exceeded"


def test_scenario_a_persistence_across_refresh_and_logout():
    """Verify that clearing cache (browser refresh/relogin) does not reset quota usage."""
    uid = f"user_persist_{uuid.uuid4().hex[:8]}"

    # Use 2 questions
    for i in range(2):
        supabase_auth_client.check_and_consume_quota(
            user_id=uid,
            question_text=f"Persistence query {i}",
            question_hash=f"h_{i}_{uuid.uuid4()}",
            request_id=f"r_{i}_{uuid.uuid4()}"
        )

    # Invalidate cache simulating restart or new session
    quota_service.invalidate_cache()
    summary = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert summary["used"] == 2
    assert summary["remaining"] == 1
    assert summary["badge_text"] == "2/3 used · 1 remaining"


def test_scenario_a_loading_and_error_states():
    """Verify loading badge and error state representations."""
    loading = QuotaService.get_loading_badge()
    assert loading["is_loading"] is True
    assert "loading quota" in loading["badge_text"]

    # Format helper
    b0, c0 = QuotaService.format_badge_display(0, 3)
    assert b0 == "0/3 used · 3 remaining"
    assert c0 == "#10B981"

    b3, c3 = QuotaService.format_badge_display(3, 0, is_exhausted=True)
    assert b3 == "3/3 used · 0 remaining · Quota exceeded"
    assert c3 == "#F5B942"


def test_scenario_b_google_oauth_endpoint_and_disabled_provider_detection():
    """
    Test B — Google OAuth:
    Verifies that get_oauth_sign_in_url queries Supabase and safely identifies
    the current status of the Google provider without fabricating a login.
    """
    ok, msg, url = AuthService.get_oauth_url("google", redirect_to="http://localhost:8501")

    # In the live configured Supabase project, Google provider is not yet enabled
    if not ok:
        assert "Provider Not Enabled" in msg or "not enabled" in msg.lower() or "network error" in msg.lower()
        assert url is None
    else:
        assert url is not None
        assert "google" in url.lower() or "accounts.google.com" in url or "supabase.co" in url


def test_scenario_b_google_oauth_callback_handling():
    """
    Test B — Google OAuth Callback Round-Trip:
    Verifies that when returning from Google OAuth with code or token:
    1. Validates the session.
    2. Retrieves/creates profile idempotently.
    3. Loads user quota.
    """
    oauth_uid = str(uuid.uuid4())
    mock_user = {
        "id": oauth_uid,
        "email": "analyst.google@energyintel.org",
        "user_metadata": {
            "full_name": "Google Analyst",
            "name": "Google Analyst",
            "avatar_url": "https://google.com/avatar.png"
        },
        "app_metadata": {"provider": "google"},
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    with patch.object(supabase_auth_client, "exchange_code_for_session") as mock_exchange:
        mock_exchange.return_value = (
            True,
            "OAuth session established.",
            "mock-jwt-token-12345",
            {
                "user_id": oauth_uid,
                "email": "analyst.google@energyintel.org",
                "username": "analyst.google",
                "full_name": "Google Analyst",
                "avatar_url": "https://google.com/avatar.png",
                "provider": "google",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        )

        ok, msg, token, udict = AuthService.handle_oauth_callback(
            code="mock-google-auth-code-777",
            user_agent="PyTest OAuth Agent"
        )
        assert ok is True
        assert token == "mock-jwt-token-12345"
        assert udict["email"] == "analyst.google@energyintel.org"
        assert udict["provider"] == "google"

        # Verify user has independent fresh quota
        summary = quota_service.get_quota_summary(oauth_uid, bypass_cache=True)
        assert summary["used"] == 0
        assert summary["remaining"] == 3
        assert summary["badge_text"] == "0/3 used · 3 remaining"


def test_scenario_c_github_oauth_endpoint_and_disabled_provider_detection():
    """
    Test C — GitHub OAuth:
    Verifies that get_oauth_sign_in_url queries Supabase and safely identifies
    the current status of the GitHub provider without fabricating a login.
    """
    ok, msg, url = AuthService.get_oauth_url("github", redirect_to="http://localhost:8501")

    if not ok:
        assert "Provider Not Enabled" in msg or "not enabled" in msg.lower() or "network error" in msg.lower()
        assert url is None
    else:
        assert url is not None
        assert "github" in url.lower() or "supabase.co" in url


def test_scenario_c_github_oauth_callback_handling():
    """
    Test C — GitHub OAuth Callback Round-Trip:
    Verifies that when returning from GitHub OAuth with an access token:
    1. Validates the session.
    2. Retrieves/creates profile idempotently.
    3. Loads user quota.
    """
    oauth_gh_uid = str(uuid.uuid4())
    mock_gh_user = {
        "id": oauth_gh_uid,
        "email": "dev.github@energyintel.org",
        "user_metadata": {
            "full_name": "GitHub Developer",
            "user_name": "gitdev",
            "avatar_url": "https://github.com/avatar.png"
        },
        "app_metadata": {"provider": "github"},
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    with patch.object(supabase_auth_client, "get_user", return_value=mock_gh_user):
        ok, msg, token, udict = AuthService.handle_oauth_callback(
            access_token="mock-gh-access-token-999",
            user_agent="PyTest GitHub Agent"
        )
        assert ok is True
        assert token == "mock-gh-access-token-999"
        assert udict["email"] == "dev.github@energyintel.org"
        assert udict["provider"] == "github"

        # Verify user has independent fresh quota
        summary = quota_service.get_quota_summary(oauth_gh_uid, bypass_cache=True)
        assert summary["used"] == 0
        assert summary["remaining"] == 3
        assert summary["badge_text"] == "0/3 used · 3 remaining"


def test_scenario_d_demo_login_button_completely_removed():
    """
    Test D — Demo login removal:
    Searches actual frontend files to verify Quick 1-Click Demo Login
    button is completely removed from all active sign-in dialogs and gates.
    """
    files_to_check = [
        "src/ui_components.py",
        "pages/9_AI_Analyst.py",
        "src/views/features.py",
        "app.py"
    ]

    for fpath in files_to_check:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        assert "Quick 1-Click Demo Login" not in content, f"Quick 1-Click Demo Login must not exist in {fpath}"
        assert "auth_quick_demo" not in content, f"auth_quick_demo key must not exist in {fpath}"
        assert "p9_demo_login_btn" not in content, f"p9_demo_login_btn key must not exist in {fpath}"
        assert "[_used_q]" not in content, f"Broken placeholder [_used_q] must not exist in {fpath}"
        assert "[_rem_q]" not in content, f"Broken placeholder [_rem_q] must not exist in {fpath}"
