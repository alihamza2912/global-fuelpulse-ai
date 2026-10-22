"""
Atomic Rolling 24-Hour Quota Manager for OpenAI Integration.
Enforces:
- 3 free questions per authenticated user ID per rolling 24-hour window.
- Database-backed persistence (SQLite & MySQL) that survives page reloads, new sessions, and device switches.
- Atomic check-and-record operations preventing concurrent limit circumvention.
- HTTP 429 exception generation with precise remaining question counts and reset countdowns.
- Zero quota consumption on failed API calls or network retries.
"""

import hashlib
import threading
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Tuple, Optional
from sqlalchemy import func

from src.database.connection import db_manager
from src.database.models import AIQuestionUsage

logger = logging.getLogger(__name__)

def utc_now() -> datetime:
    """Returns timezone-naive UTC datetime compatible with database schemas."""
    return datetime.now(timezone.utc).replace(tzinfo=None)

# Constants
MAX_QUESTIONS_PER_24H = 3
ROLLING_WINDOW_HOURS = 24


class OpenAIQuotaExhaustedError(Exception):
    """Raised when an authenticated user has exhausted their 3 questions per rolling 24 hours."""

    def __init__(self, message: str, reset_time_str: str, reset_timestamp: Optional[datetime] = None):
        super().__init__(message)
        self.status_code = 429
        self.message = message
        self.reset_time_str = reset_time_str
        self.reset_timestamp = reset_timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status_code": 429,
            "error": "Quota Exhausted",
            "message": self.message,
            "remaining": 0,
            "reset_time_str": self.reset_time_str,
            "reset_timestamp": self.reset_timestamp.isoformat() if self.reset_timestamp else None
        }


class OpenAIQuotaManager:
    """Manages rolling 24-hour quota per stable authenticated user ID."""

    def __init__(self):
        self._lock = threading.RLock()

    def invalidate_cache(self, user_id: Optional[str] = None) -> None:
        """Invalidates cache in the unified QuotaService."""
        from src.auth.quota_service import quota_service
        quota_service.invalidate_cache(user_id)

    @classmethod
    def format_time_delta(cls, target_dt: datetime) -> str:
        """Formats remaining time into human-friendly hours and minutes."""
        now = utc_now()
        if target_dt <= now:
            return "less than a minute"
        diff = target_dt - now
        total_seconds = int(diff.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{max(1, minutes)} minutes"

    def get_user_quota_status(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieves the authoritative rolling 24-hour quota status for a user.
        Delegates directly to the unified QuotaService.
        """
        from src.auth.quota_service import quota_service
        q = quota_service.get_quota_summary(user_id)
        reset_ts_dt = None
        if q.get("resets_at"):
            try:
                reset_ts_dt = datetime.fromisoformat(str(q["resets_at"]).replace("Z", "+00:00"))
            except Exception:
                pass

        return {
            "user_id": user_id,
            "max_allowed": q["limit"],
            "used_count": q["used"],
            "remaining": q["remaining"],
            "is_exhausted": q["quota_exhausted"],
            "reset_timestamp": reset_ts_dt,
            "reset_time_str": q["reset_time_str"],
            "used": q["used"],
            "limit": q["limit"],
            "window_started_at": q["window_started_at"],
            "resets_at": q["resets_at"],
            "quota_exhausted": q["quota_exhausted"]
        }

    def check_quota(self, user_id: str) -> Tuple[bool, Optional[str], Dict[str, Any]]:
        """
        Verifies if an authenticated user has remaining quota before calling OpenAI.
        Returns (can_call, error_message, status_dict).
        """
        status = self.get_user_quota_status(user_id)
        if status["is_exhausted"]:
            msg = (
                f"You have used your {MAX_QUESTIONS_PER_24H} free questions for the current rolling 24 hours. "
                f"Your next question unlocks in {status['reset_time_str']}."
            )
            return False, msg, status
        return True, None, status

    def record_usage_atomic(
        self,
        user_id: str,
        question: str,
        model_used: str,
        tokens_used: Optional[int] = None
    ) -> AIQuestionUsage:
        """
        Atomically records a successful question usage within a transaction.
        Raises OpenAIQuotaExhaustedError (HTTP 429) if the rolling limit was already reached.
        """
        if not user_id:
            raise OpenAIQuotaExhaustedError("Authentication required.", "immediate")

        cutoff = utc_now() - timedelta(hours=ROLLING_WINDOW_HOURS)
        q_hash = hashlib.sha256((question or "").strip().encode("utf-8")).hexdigest()

        with self._lock:
            with db_manager.get_session() as session:
                # Count current usage inside transaction
                current_usages = session.query(AIQuestionUsage).filter(
                    AIQuestionUsage.user_id == str(user_id),
                    AIQuestionUsage.created_at >= cutoff,
                    AIQuestionUsage.status == "completed"
                ).order_by(AIQuestionUsage.created_at.asc()).all()

                if len(current_usages) >= MAX_QUESTIONS_PER_24H:
                    oldest_in_window = current_usages[0].created_at
                    reset_ts = oldest_in_window + timedelta(hours=ROLLING_WINDOW_HOURS)
                    reset_time_str = self.format_time_delta(reset_ts)
                    msg = (
                        f"You have reached your 24-hour limit of {MAX_QUESTIONS_PER_24H} questions. "
                        f"Your next question unlocks in {reset_time_str}."
                    )
                    raise OpenAIQuotaExhaustedError(msg, reset_time_str, reset_ts)

                usage_record = AIQuestionUsage(
                    user_id=str(user_id),
                    question_text=(question or "").strip()[:500],
                    question_hash=q_hash,
                    created_at=utc_now(),
                    status="completed",
                    model_used=model_used,
                    tokens_used=tokens_used
                )
                session.add(usage_record)
                session.commit()
                try:
                    from src.auth.quota_service import quota_service
                    quota_service.invalidate_cache(user_id)
                except Exception:
                    pass
                logger.info(
                    "Recorded OpenAI usage for user %s. Used: %d/%d",
                    user_id, len(current_usages) + 1, MAX_QUESTIONS_PER_24H
                )
                return usage_record


# Global singleton
openai_quota_manager = OpenAIQuotaManager()
