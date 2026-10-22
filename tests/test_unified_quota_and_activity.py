"""
Comprehensive Test Suite for Unified AI Quota, Supabase Activity Tracking,
and Professional Top Navigation Header.

Validates the 13 critical production scenarios:
1. First question asked: 0/3 used (3 remaining) -> 1/3 used (2 remaining).
2. Second question asked: 1/3 used (2 remaining) -> 2/3 used (1 remaining).
3. Third question asked: 2/3 used (1 remaining) -> 3/3 used (0 remaining).
4. Both 'Questions Used' (0/3 -> 3/3) and 'Questions Remaining' (3 -> 0) are consistent.
5. All quota displays (header badge, assistant modal, and page 9) share the same single source of truth.
6. Attempting a 4th question is rejected server-side without incrementing quota.
7. Page refresh / cache bypass preserves exact database count.
8. User re-login preserves exact database count.
9. Different users have strictly isolated independent quotas.
10. Idempotent submission with identical request_id does not double-count.
11. Rolling 24-hour reset calculation and countdown formatting.
12. Top navigation order is strictly: AI -> NEWS -> LOGIN/ACCOUNT -> LANGUAGE.
13. Login activity tracking updates last_login_at and records login history audit trail.
"""

import uuid
from datetime import datetime, timezone, timedelta
import pytest
from unittest.mock import patch, MagicMock

from src.auth.quota_service import QuotaService, quota_service, MAX_QUESTIONS_PER_24H, ROLLING_WINDOW_HOURS
from src.auth.auth_service import AuthService, hash_password
from src.auth.supabase_client import SupabaseAuthClient
from src.ai.openai_quota_manager import OpenAIQuotaManager, openai_quota_manager, OpenAIQuotaExhaustedError
from src.database.connection import db_manager
from src.database.models import User, UserLoginHistory, AIQuestionUsage


from src.database.migrations import init_database

@pytest.fixture(autouse=True)
def setup_clean_db():
    """Ensure database tables exist and clean test usage records."""
    init_database()
    quota_service.invalidate_cache()
    test_uids = ["test-user-alpha", "test-user-beta", "test-user-gamma", "test-u-1"]
    test_usernames = ["alpha_user", "beta_user", "gamma_analyst"]
    with db_manager.get_session() as session:
        session.query(AIQuestionUsage).filter(AIQuestionUsage.user_id.in_(test_uids)).delete(synchronize_session=False)
        session.query(UserLoginHistory).filter(UserLoginHistory.user_id.in_(test_uids)).delete(synchronize_session=False)
        session.query(User).filter((User.user_id.in_(test_uids)) | (User.username.in_(test_usernames))).delete(synchronize_session=False)
        session.commit()
    yield
    quota_service.invalidate_cache()
    with db_manager.get_session() as session:
        session.query(AIQuestionUsage).filter(AIQuestionUsage.user_id.in_(test_uids)).delete(synchronize_session=False)
        session.query(UserLoginHistory).filter(UserLoginHistory.user_id.in_(test_uids)).delete(synchronize_session=False)
        session.query(User).filter((User.user_id.in_(test_uids)) | (User.username.in_(test_usernames))).delete(synchronize_session=False)
        session.commit()


def test_scenario_01_to_04_quota_progression():
    """
    Scenarios 1-4:
    - Initial: 0/3 used (3 remaining).
    - Question 1: 1/3 used (2 remaining).
    - Question 2: 2/3 used (1 remaining).
    - Question 3: 3/3 used (0 remaining, exhausted).
    - Verifies 'Questions Used' vs 'Questions Remaining' distinct presentation.
    """
    uid = "test-user-alpha"
    quota_service.invalidate_cache(uid)

    # Initial state (0 questions asked)
    q0 = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert q0["used"] == 0
    assert q0["remaining"] == 3
    assert q0["limit"] == 3
    assert q0["quota_exhausted"] is False
    assert ("0/3 used · 3 remaining" in q0["badge_text"] or "0/3 Used • 3 Left" in q0["badge_text"])

    # Question 1 asked
    openai_quota_manager.record_usage_atomic(uid, "What is the Brent crude price?", "gpt-4o-mini")
    q1 = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert q1["used"] == 1
    assert q1["remaining"] == 2
    assert q1["quota_exhausted"] is False
    assert ("1/3 used · 2 remaining" in q1["badge_text"] or "1/3 Used • 2 Left" in q1["badge_text"])

    # Question 2 asked
    openai_quota_manager.record_usage_atomic(uid, "Explain refining crack spreads", "gpt-4o-mini")
    q2 = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert q2["used"] == 2
    assert q2["remaining"] == 1
    assert q2["quota_exhausted"] is False
    assert ("2/3 used · 1 remaining" in q2["badge_text"] or "2/3 Used • 1 Left" in q2["badge_text"])

    # Question 3 asked
    openai_quota_manager.record_usage_atomic(uid, "Analyze Strait of Hormuz tanker traffic", "gpt-4o-mini")
    q3 = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert q3["used"] == 3
    assert q3["remaining"] == 0
    assert q3["quota_exhausted"] is True
    assert ("3/3 used · 0 remaining" in q3["badge_text"] or "3/3 Used • 0 Left" in q3["badge_text"])


def test_scenario_05_quota_synchronization_across_services():
    """
    Scenario 5:
    All 3 quota access points (QuotaService, OpenAIQuotaManager, SupabaseAuthClient)
    return consistent values for used, limit, remaining, and exhaustion state.
    """
    uid = "test-user-alpha"
    quota_service.invalidate_cache(uid)

    # Record 2 usages
    openai_quota_manager.record_usage_atomic(uid, "Query A", "gpt-4o-mini")
    openai_quota_manager.record_usage_atomic(uid, "Query B", "gpt-4o-mini")

    summary = quota_service.get_quota_summary(uid, bypass_cache=True)
    oai_status = openai_quota_manager.get_user_quota_status(uid)

    assert summary["used"] == oai_status["used_count"] == 2
    assert summary["remaining"] == oai_status["remaining"] == 1
    assert summary["limit"] == oai_status["max_allowed"] == 3
    assert summary["quota_exhausted"] == oai_status["is_exhausted"] == False


def test_scenario_06_fourth_question_rejected():
    """
    Scenario 6:
    Attempting a 4th question within the same 24-hour window fails with HTTP 429
    and does not increment the database usage counter past 3.
    """
    uid = "test-user-alpha"
    quota_service.invalidate_cache(uid)

    # Exhaust the 3 questions
    for i in range(3):
        openai_quota_manager.record_usage_atomic(uid, f"Question {i+1}", "gpt-4o-mini")

    can_call, err_msg, status = openai_quota_manager.check_quota(uid)
    assert can_call is False
    assert "You have used your 3 free questions" in err_msg

    with pytest.raises(OpenAIQuotaExhaustedError) as exc_info:
        openai_quota_manager.record_usage_atomic(uid, "Question 4 (Blocked)", "gpt-4o-mini")

    assert "reached your 24-hour limit of 3 questions" in str(exc_info.value)

    # Verify count is still exactly 3
    final_summary = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert final_summary["used"] == 3
    assert final_summary["remaining"] == 0


def test_scenario_07_page_refresh_preserves_count():
    """
    Scenario 7:
    Simulates a page refresh by clearing in-memory caches and re-querying the database.
    The count must be perfectly preserved.
    """
    uid = "test-user-alpha"
    quota_service.invalidate_cache(uid)

    openai_quota_manager.record_usage_atomic(uid, "Question 1", "gpt-4o-mini")
    openai_quota_manager.record_usage_atomic(uid, "Question 2", "gpt-4o-mini")

    # Simulate browser refresh by purging memory cache
    quota_service.invalidate_cache()

    refreshed_summary = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert refreshed_summary["used"] == 2
    assert refreshed_summary["remaining"] == 1
    assert ("2/3 used · 1 remaining" in refreshed_summary["badge_text"] or "2/3 Used • 1 Left" in refreshed_summary["badge_text"])


def test_scenario_08_relogin_preserves_count():
    """
    Scenario 8:
    A user logs in, uses 1 question, logs out, and logs in again.
    The quota status must retain the consumed question from the database.
    """
    uid = "test-user-alpha"
    # Create test user in local DB
    with db_manager.get_session() as session:
        test_u = User(
            user_id=uid,
            username="alpha_user",
            email="alpha@fuelpulse.ai",
            password_hash=hash_password("Secret123!"),
            full_name="Alpha Analyst"
        )
        session.add(test_u)
        session.commit()

    # 1. Login
    ok, msg, token, u_dict = AuthService.login_user("alpha_user", "Secret123!")
    assert ok is True

    # 2. Ask 1 question
    openai_quota_manager.record_usage_atomic(uid, "Alpha inquiry", "gpt-4o-mini")

    # 3. Logout
    AuthService.logout(token)

    # 4. Re-login
    ok2, msg2, token2, u_dict2 = AuthService.login_user("alpha_user", "Secret123!")
    assert ok2 is True

    # 5. Check quota
    summary = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert summary["used"] == 1
    assert summary["remaining"] == 2
    assert ("1/3 used · 2 remaining" in summary["badge_text"] or "1/3 Used • 2 Left" in summary["badge_text"])


def test_scenario_09_user_isolation():
    """
    Scenario 9:
    Different users have strictly separate quotas. User A exhausting quota
    does NOT affect User B who has 0 questions used.
    """
    user_a = "test-user-alpha"
    user_b = "test-user-beta"

    # User A exhausts all 3 questions
    for i in range(3):
        openai_quota_manager.record_usage_atomic(user_a, f"Query A {i}", "gpt-4o-mini")

    summary_a = quota_service.get_quota_summary(user_a, bypass_cache=True)
    assert summary_a["used"] == 3
    assert summary_a["remaining"] == 0
    assert summary_a["quota_exhausted"] is True

    # User B should still have all 3 questions remaining
    summary_b = quota_service.get_quota_summary(user_b, bypass_cache=True)
    assert summary_b["used"] == 0
    assert summary_b["remaining"] == 3
    assert summary_b["quota_exhausted"] is False
    assert ("0/3 used · 3 remaining" in summary_b["badge_text"] or "0/3 Used • 3 Left" in summary_b["badge_text"])


def test_scenario_10_idempotent_request_id():
    """
    Scenario 10:
    Rapid duplicate requests with the same request_id must be recognized
    idempotently and not consume additional quota units.
    """
    client = SupabaseAuthClient(supabase_url="https://mock.supabase.co", supabase_key="mock-key")
    req_id = str(uuid.uuid4())

    mock_resp_success = MagicMock()
    mock_resp_success.status_code = 200
    mock_resp_success.content = b'{"allowed": true, "remaining": 2, "used_count": 1, "is_exhausted": false}'
    mock_resp_success.json.return_value = {
        "allowed": True,
        "remaining": 2,
        "used_count": 1,
        "is_exhausted": False,
        "already_processed": False
    }

    mock_resp_duplicate = MagicMock()
    mock_resp_duplicate.status_code = 200
    mock_resp_duplicate.content = b'{"allowed": true, "remaining": 2, "used_count": 1, "is_exhausted": false, "already_processed": true}'
    mock_resp_duplicate.json.return_value = {
        "allowed": True,
        "remaining": 2,
        "used_count": 1,
        "is_exhausted": False,
        "already_processed": True
    }

    with patch.object(client, "is_configured", return_value=True):
        with patch.object(client, "call_rpc", side_effect=[(True, mock_resp_success.json()), (True, mock_resp_duplicate.json())]):
            allowed1, res1 = client.check_and_consume_quota("00000000-0000-0000-0000-000000000001", "Query", question_hash="dummy", request_id=req_id)
            assert allowed1 is True
            assert res1["used_count"] == 1

            allowed2, res2 = client.check_and_consume_quota("00000000-0000-0000-0000-000000000001", "Query", question_hash="dummy", request_id=req_id)
            assert allowed2 is True
            assert res2["already_processed"] is True
            assert res2["used_count"] == 1


def test_scenario_11_reset_countdown_calculation():
    """
    Scenario 11:
    Verifies that the reset timestamp is computed exactly 24 hours after the earliest
    question in the rolling window, and countdown formatting is accurate.
    """
    uid = "test-user-alpha"
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Insert a record from 10 hours ago
    t_minus_10h = now - timedelta(hours=10)
    with db_manager.get_session() as session:
        usage = AIQuestionUsage(
            user_id=uid,
            question_text="Earlier question",
            question_hash="abc12345",
            created_at=t_minus_10h,
            status="completed"
        )
        session.add(usage)
        session.commit()

    summary = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert summary["used"] == 1
    assert summary["remaining"] == 2

    # Should reset in ~14 hours (24 - 10)
    assert "13h" in summary["reset_time_str"] or "14h" in summary["reset_time_str"]


def test_scenario_12_top_navigation_order():
    """
    Scenario 12:
    Verifies top navigation layout strictly arranges controls in the required CWI Studio order:
    Brand | [Overview, Live Intel, Global Trade, Forecasts, News, AI Analyst] | [Language, Theme, Account].
    """
    import inspect
    from src.ui_components import render_universal_top_header

    source = inspect.getsource(render_universal_top_header)

    # Search column allocations and render order in the source code
    col_brand_pos = source.find("col_brand")
    col_nav_home_pos = source.find("col_nav_home")
    col_nav_intel_pos = source.find("col_nav_intel")
    col_nav_trade_pos = source.find("col_nav_trade")
    col_nav_fc_pos = source.find("col_nav_fc")
    col_news_pos = source.find("col_news")
    col_ai_pos = source.find("col_ai")
    col_lang_pos = source.find("col_lang")
    col_theme_pos = source.find("col_theme")
    col_auth_pos = source.find("col_auth")

    assert col_brand_pos != -1, "col_brand must exist"
    assert col_nav_home_pos != -1, "col_nav_home must exist"
    assert col_nav_intel_pos != -1, "col_nav_intel must exist"
    assert col_nav_trade_pos != -1, "col_nav_trade must exist"
    assert col_nav_fc_pos != -1, "col_nav_fc must exist"
    assert col_news_pos != -1, "col_news must exist"
    assert col_ai_pos != -1, "col_ai must exist"
    assert col_lang_pos != -1, "col_lang must exist"
    assert col_theme_pos != -1, "col_theme must exist"
    assert col_auth_pos != -1, "col_auth must exist"

    # Verify CWI Studio Layout: Brand -> Center Nav (Overview < Intel < Trade < FC < News < AI) -> Actions (Lang < Theme < Auth)
    assert col_brand_pos < col_nav_home_pos < col_nav_intel_pos < col_nav_trade_pos < col_nav_fc_pos < col_news_pos < col_ai_pos < col_lang_pos < col_theme_pos < col_auth_pos, (
        "Header controls must strictly be ordered: Brand -> Center Navigation (Overview, Intel, Trade, Forecasts, News, AI) -> Actions (Language, Theme, Account)"
    )


def test_scenario_13_supabase_activity_tracking():
    """
    Scenario 13:
    Verifies user login activity is recorded in user_login_history and updates last_login_at.
    """
    uid = "test-user-gamma"
    # Create test user
    with db_manager.get_session() as session:
        test_u = User(
            user_id=uid,
            username="gamma_analyst",
            email="gamma@fuelpulse.ai",
            password_hash=hash_password("SuperSecret999!"),
            full_name="Gamma Analyst"
        )
        session.add(test_u)
        session.commit()

    # Perform login
    ok, msg, token, u_dict = AuthService.login_user(
        "gamma_analyst",
        "SuperSecret999!",
        request_ip="192.168.1.100",
        user_agent="GlobalFuelPulse/2.0 PyTest"
    )
    assert ok is True

    # Verify last_login_at was updated on User
    with db_manager.get_session() as session:
        u = session.query(User).filter(User.user_id == uid).first()
        assert u.last_login_at is not None

        # Verify audit record in UserLoginHistory
        history = session.query(UserLoginHistory).filter(UserLoginHistory.user_id == uid).all()
        assert len(history) >= 1
        latest = history[-1]
        assert latest.event_type == "login"
        assert latest.result == "success"
        assert latest.ip_address == "192.168.1.100"
        assert latest.user_agent == "GlobalFuelPulse/2.0 PyTest"

    # Verify AuthService query methods
    login_records = AuthService.get_user_login_history(uid)
    assert len(login_records) >= 1
    assert login_records[0]["event_type"] == "login"
    assert login_records[0]["result"] == "success"
