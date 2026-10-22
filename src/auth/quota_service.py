"""
Authoritative Unified Quota Service for Global FuelPulse AI.
Single Source of Truth for:
- Rolling 24-hour question quota enforcement (3 free questions per user).
- Clear separation between Questions Used (0/3 -> 3/3) and Questions Remaining (3 -> 0).
- Immediate synchronization across Top Header, AI Modal, Page 9, and Account Dashboard.
- Server-side atomic quota verification before any AI provider calls.
"""

import time
import logging
import threading
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, Tuple

from config.settings import settings

logger = logging.getLogger(__name__)

MAX_QUESTIONS_PER_24H = 3
ROLLING_WINDOW_HOURS = 24


def utc_now() -> datetime:
    """Returns timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


class QuotaService:
    """
    Centralized, authoritative service for calculating and enforcing user AI quotas.
    Integrates with Supabase PostgreSQL (RPC & PostgREST) and falls back to local database.
    """

    _cache: Dict[str, tuple[float, Dict[str, Any]]] = {}
    _cache_lock = threading.RLock()
    _CACHE_TTL = 3.0  # seconds

    @classmethod
    def format_countdown(cls, target_dt: Optional[datetime]) -> str:
        """Formats remaining time into human-readable hours and minutes."""
        if not target_dt:
            return f"{ROLLING_WINDOW_HOURS} hours"
        now = utc_now()
        if target_dt <= now:
            return "less than a minute"
        diff = target_dt - now
        total_seconds = int(diff.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{max(1, minutes)}m"

    @classmethod
    def invalidate_cache(cls, user_id: Optional[str] = None) -> None:
        """Clears memory cache for immediate reactive UI updates."""
        with cls._cache_lock:
            if user_id:
                cls._cache.pop(str(user_id), None)
            else:
                cls._cache.clear()

    @classmethod
    def get_quota_summary(
        cls,
        user_id: Optional[str],
        max_questions: int = MAX_QUESTIONS_PER_24H,
        window_hours: int = ROLLING_WINDOW_HOURS,
        bypass_cache: bool = False
    ) -> Dict[str, Any]:
        """
        Retrieves the definitive quota summary for a user.
        Always returns a consistent schema:
        - user_id: str
        - used: int (0 to 3)
        - limit: int (3)
        - remaining: int (3 to 0)
        - window_started_at: Optional[str] (ISO)
        - resets_at: Optional[str] (ISO)
        - reset_time_str: str (e.g. "14h 50m")
        - quota_exhausted: bool (True when remaining == 0)
        - total_historical: int
        - is_authenticated: bool
        - badge_text: str (cleanly distinguishes used from remaining)
        """
        clean_uid = str(user_id).strip() if user_id else None

        if not clean_uid:
            return {
                "user_id": None,
                "used": 0,
                "limit": max_questions,
                "remaining": 0,
                "window_started_at": None,
                "resets_at": None,
                "reset_time_str": "Sign in required",
                "quota_exhausted": True,
                "total_historical": 0,
                "is_authenticated": False,
                "status_label": "Sign In Required",
                "badge_text": "Sign In"
            }

        now_ts = time.time()
        with cls._cache_lock:
            if not bypass_cache and clean_uid in cls._cache:
                entry_ts, cached_val = cls._cache[clean_uid]
                if (now_ts - entry_ts) < cls._CACHE_TTL:
                    return cached_val.copy()

        # 1. Supabase Authoritative Lookup (Cloud)
        try:
            from src.auth.supabase_client import supabase_auth_client
            if supabase_auth_client.is_configured() and ("-" in clean_uid and len(clean_uid) >= 32):
                cutoff_dt = utc_now() - timedelta(hours=window_hours)
                cutoff_iso = cutoff_dt.isoformat()

                # Query Supabase ai_question_usages with service role key for authoritative consistency
                ok, rows, _ = supabase_auth_client.select_table(
                    "ai_question_usages",
                    {
                        "user_id": f"eq.{clean_uid}",
                        "status": "eq.completed",
                        "created_at": f"gte.{cutoff_iso}",
                        "select": "usage_id,created_at,quota_unit_consumed",
                        "order": "created_at.asc"
                    },
                    use_service_key=True
                )

                if ok and isinstance(rows, list):
                    # Only count rows that actually consumed a quota unit
                    counted_rows = [r for r in rows if r.get("quota_unit_consumed") is not False]
                    used_count = len(counted_rows)
                    remaining = max(0, max_questions - used_count)
                    is_exhausted = (used_count >= max_questions)

                    resets_at_iso = None
                    reset_time_str = f"{window_hours} hours"
                    window_started_iso = None

                    if counted_rows:
                        raw_earliest = counted_rows[0].get("created_at")
                        if raw_earliest:
                            try:
                                window_started_iso = str(raw_earliest)
                                earliest_dt = datetime.fromisoformat(window_started_iso.replace("Z", "+00:00"))
                                reset_dt = earliest_dt + timedelta(hours=window_hours)
                                resets_at_iso = reset_dt.isoformat()
                                reset_time_str = cls.format_countdown(reset_dt)
                            except Exception as parse_e:
                                logger.debug(f"Date parse error: {parse_e}")

                    # Total historical count
                    ok_hist, hist_rows, _ = supabase_auth_client.select_table(
                        "ai_question_usages",
                        {"user_id": f"eq.{clean_uid}", "select": "usage_id"},
                        use_service_key=True
                    )
                    total_hist = len(hist_rows) if (ok_hist and isinstance(hist_rows, list)) else used_count

                    summary = {
                        "user_id": clean_uid,
                        "used": used_count,
                        "limit": max_questions,
                        "remaining": remaining,
                        "window_started_at": window_started_iso,
                        "resets_at": resets_at_iso,
                        "reset_time_str": reset_time_str,
                        "quota_exhausted": is_exhausted,
                        "total_historical": total_hist,
                        "is_authenticated": True,
                        "status_label": "Quota Exhausted" if is_exhausted else "Available",
                        "badge_text": f"{used_count}/{max_questions} used · {remaining} remaining"
                    }

                    with cls._cache_lock:
                        cls._cache[clean_uid] = (now_ts, summary)
                    return summary
        except Exception as e:
            logger.debug(f"Supabase quota check bypass: {e}")

        # 2. Local SQLite Database Fallback
        try:
            from src.database.connection import db_manager
            from src.database.models import AIQuestionUsage

            cutoff_naive = (datetime.now(timezone.utc) - timedelta(hours=window_hours)).replace(tzinfo=None)

            with db_manager.get_session() as session:
                rows = session.query(AIQuestionUsage).filter(
                    AIQuestionUsage.user_id == clean_uid,
                    AIQuestionUsage.created_at >= cutoff_naive,
                    AIQuestionUsage.status == "completed"
                ).order_by(AIQuestionUsage.created_at.asc()).all()

                # Filter out rejected or non-consuming attempts
                counted = [r for r in rows if getattr(r, "quota_unit_consumed", True) is not False]
                used_count = len(counted)
                remaining = max(0, max_questions - used_count)
                is_exhausted = (used_count >= max_questions)

                resets_at_iso = None
                window_started_iso = None
                reset_time_str = f"{window_hours} hours"

                if counted:
                    earliest_naive = counted[0].created_at
                    earliest_aware = earliest_naive.replace(tzinfo=timezone.utc)
                    window_started_iso = earliest_aware.isoformat()
                    reset_aware = earliest_aware + timedelta(hours=window_hours)
                    resets_at_iso = reset_aware.isoformat()
                    reset_time_str = cls.format_countdown(reset_aware)

                total_hist = session.query(AIQuestionUsage).filter(
                    AIQuestionUsage.user_id == clean_uid
                ).count()

                summary = {
                    "user_id": clean_uid,
                    "used": used_count,
                    "limit": max_questions,
                    "remaining": remaining,
                    "window_started_at": window_started_iso,
                    "resets_at": resets_at_iso,
                    "reset_time_str": reset_time_str,
                    "quota_exhausted": is_exhausted,
                    "total_historical": total_hist,
                    "is_authenticated": True,
                    "status_label": "Quota Exhausted" if is_exhausted else "Available",
                    "badge_text": f"{used_count}/{max_questions} used · {remaining} remaining"
                }

                with cls._cache_lock:
                    cls._cache[clean_uid] = (now_ts, summary)
                return summary
        except Exception as e:
            logger.error(f"Local quota check error: {e}")

        # Default fallback if database error
        return {
            "user_id": clean_uid,
            "used": 0,
            "limit": max_questions,
            "remaining": max_questions,
            "window_started_at": None,
            "resets_at": None,
            "reset_time_str": f"{window_hours} hours",
            "quota_exhausted": False,
            "total_historical": 0,
            "is_authenticated": True,
            "status_label": "Available",
            "badge_text": f"0/{max_questions} Used • {max_questions} Left"
        }

    @classmethod
    def consume_quota(cls, user_id: str, question: str) -> Tuple[bool, str]:
        """Atomically checks and consumes a single question unit for the authenticated user."""
        with cls._cache_lock:
            import hashlib
            from src.auth.supabase_client import supabase_auth_client
            q_hash = hashlib.sha256(question.encode("utf-8")).hexdigest()[:16]
            ok, res = supabase_auth_client.check_and_consume_quota(user_id, question, q_hash)
            cls.invalidate_cache(user_id)
            msg = res.get("message", "Quota accepted" if ok else "Daily quota reached (3/3 questions used in rolling 24 hours)") if isinstance(res, dict) else str(res)
            return ok, msg

    @classmethod
    def refund_quota(cls, user_id: str, reason: str = "") -> bool:
        """Atomically restores a previously consumed quota unit in case of provider or network error."""
        from src.auth.supabase_client import supabase_auth_client
        res = supabase_auth_client.refund_quota(user_id, reason)
        cls.invalidate_cache(user_id)
        return res


quota_service = QuotaService()
