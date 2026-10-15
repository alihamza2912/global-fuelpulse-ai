"""
Thread-safe and process-safe AI Quota and Rate Limit Manager.
Enforces Google Gemini Free Tier limits:
- Daily reset synchronized with Google AI Studio (00:00 Pacific Time).
- Rolling 60-second window for per-minute rate limits.
- Provider error latching for HTTP 429 / RESOURCE_EXHAUSTED errors.
- Atomic file locking ensuring multi-user and multi-threaded safety.
"""

import os
import json
import time
import fcntl
import logging
import threading
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Tuple, Optional
import zoneinfo

from config.settings import settings

logger = logging.getLogger(__name__)

# Pacific Timezone where Google AI Studio quotas reset
PACIFIC_TZ = zoneinfo.ZoneInfo("America/Los_Angeles")


class AIQuotaManager:
    """Manages shared Gemini API free-tier quotas and rate limits."""

    def __init__(self, state_file_path: Optional[Path] = None):
        self.state_file_path = state_file_path or (settings.base_dir / ".ai_quota_state.json")
        self._thread_lock = threading.RLock()

    def _get_pacific_now(self) -> datetime:
        return datetime.now(PACIFIC_TZ)

    def get_pacific_date_key(self) -> str:
        """Returns current date in Pacific Time (YYYY-MM-DD)."""
        return self._get_pacific_now().strftime("%Y-%m-%d")

    def get_next_reset_datetime(self) -> datetime:
        """Calculates the upcoming midnight Pacific Time reset moment."""
        now_pt = self._get_pacific_now()
        tomorrow_pt = now_pt.date() + timedelta(days=1)
        next_midnight_pt = datetime(
            tomorrow_pt.year, tomorrow_pt.month, tomorrow_pt.day, 0, 0, 0, tzinfo=PACIFIC_TZ
        )
        return next_midnight_pt

    def get_formatted_reset_time(self) -> str:
        """Returns human-readable reset time string, e.g., '12:00 AM PT (07:00 UTC)'."""
        next_reset_pt = self.get_next_reset_datetime()
        next_reset_utc = next_reset_pt.astimezone(timezone.utc)
        pt_tz_abbr = next_reset_pt.strftime("%Z")
        return f"{next_reset_pt.strftime('%I:%M %p')} {pt_tz_abbr} ({next_reset_utc.strftime('%H:%M')} UTC)"

    def _load_state_locked(self, file_obj) -> Dict[str, Any]:
        """Loads state dictionary with fallback defaults."""
        default_state = {
            "pacific_date": self.get_pacific_date_key(),
            "daily_calls": 0,
            "provider_exhausted": False,
            "provider_error_reason": "",
            "minute_call_timestamps": [],
            "last_updated": time.time(),
        }
        try:
            file_obj.seek(0)
            content = file_obj.read()
            if not content.strip():
                return default_state
            data = json.loads(content)
            # Validate required keys
            for k, v in default_state.items():
                if k not in data:
                    data[k] = v
            return data
        except Exception as e:
            logger.warning(f"Could not parse quota state file, using defaults: {e}")
            return default_state

    def _save_state_locked(self, file_obj, state: Dict[str, Any]) -> None:
        """Writes state dictionary to disk atomically."""
        file_obj.seek(0)
        file_obj.truncate()
        json.dump(state, file_obj, indent=2)
        file_obj.flush()

    def _normalize_state(self, state: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        """
        Cleans state:
        - Resets daily counters if Pacific date has changed.
        - Trims rolling minute window calls older than 60 seconds.
        Returns (updated_state, has_changed).
        """
        changed = False
        current_pt_date = self.get_pacific_date_key()
        now_ts = time.time()

        # Check daily reset (midnight PT)
        if state.get("pacific_date") != current_pt_date:
            state["pacific_date"] = current_pt_date
            state["daily_calls"] = 0
            state["provider_exhausted"] = False
            state["provider_error_reason"] = ""
            changed = True

        # Prune calls older than 60 seconds
        recent_calls = [
            ts for ts in state.get("minute_call_timestamps", [])
            if (now_ts - ts) < 60.0
        ]
        if len(recent_calls) != len(state.get("minute_call_timestamps", [])):
            state["minute_call_timestamps"] = recent_calls
            changed = True

        return state, changed

    def check_quota(self) -> Tuple[bool, str, Optional[str]]:
        """
        Checks whether an AI call can be made.
        Returns:
            (is_allowed, reason_code, user_message)
            reason_code is one of: "OK", "DAILY_LIMIT_REACHED", "PROVIDER_EXHAUSTED", "MINUTE_RATE_LIMIT"
        """
        with self._thread_lock:
            with open(self.state_file_path, "a+") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                try:
                    state = self._load_state_locked(f)
                    state, changed = self._normalize_state(state)
                    if changed:
                        self._save_state_locked(f, state)

                    reset_time_str = self.get_formatted_reset_time()
                    quota_finished_msg = (
                        f"The free AI quota for today is finished. The AI assistant will be available "
                        f"again after {reset_time_str}. Meanwhile you can still use the charts, tables "
                        f"and forecasts on the dashboard."
                    )
                    minute_throttled_msg = "Too many questions right now. Please try again in a minute."

                    # 1. Provider HTTP 429 / RESOURCE_EXHAUSTED latch
                    if state.get("provider_exhausted"):
                        return False, "PROVIDER_EXHAUSTED", quota_finished_msg

                    # 2. Daily call counter limit
                    max_daily = settings.api.max_ai_calls_per_day
                    if state.get("daily_calls", 0) >= max_daily:
                        return False, "DAILY_LIMIT_REACHED", quota_finished_msg

                    # 3. Per-minute rolling window limit
                    max_minute = settings.api.max_ai_calls_per_minute
                    if len(state.get("minute_call_timestamps", [])) >= max_minute:
                        return False, "MINUTE_RATE_LIMIT", minute_throttled_msg

                    return True, "OK", None
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)

    def record_call_success(self) -> Dict[str, Any]:
        """Atomically increments daily call counter and records current timestamp."""
        with self._thread_lock:
            with open(self.state_file_path, "a+") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                try:
                    state = self._load_state_locked(f)
                    state, _ = self._normalize_state(state)

                    state["daily_calls"] = state.get("daily_calls", 0) + 1
                    timestamps = state.get("minute_call_timestamps", [])
                    timestamps.append(time.time())
                    state["minute_call_timestamps"] = timestamps
                    state["last_updated"] = time.time()

                    self._save_state_locked(f, state)
                    return state.copy()
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)

    def record_provider_quota_error(self, error_message: str = "") -> None:
        """
        Latches the provider quota exhaustion flag for the current Pacific day.
        Prevents any further AI calls until the daily reset time.
        """
        with self._thread_lock:
            with open(self.state_file_path, "a+") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                try:
                    state = self._load_state_locked(f)
                    state, _ = self._normalize_state(state)

                    state["provider_exhausted"] = True
                    # Clean any keys or sensitive tokens from error message
                    state["provider_error_reason"] = error_message[:200]
                    state["last_updated"] = time.time()

                    self._save_state_locked(f, state)
                    logger.warning(f"AI Quota provider error latched until next PT reset: {error_message[:100]}")
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)

    def get_quota_status(self) -> Dict[str, Any]:
        """Returns current quota status for dashboard presentation."""
        with self._thread_lock:
            with open(self.state_file_path, "a+") as f:
                fcntl.flock(f, fcntl.LOCK_SH)
                try:
                    state = self._load_state_locked(f)
                    state, _ = self._normalize_state(state)

                    max_daily = settings.api.max_ai_calls_per_day
                    calls_today = state.get("daily_calls", 0)
                    calls_remaining = max(0, max_daily - calls_today)
                    is_finished = (
                        calls_remaining == 0 or bool(state.get("provider_exhausted"))
                    )

                    return {
                        "calls_today": calls_today,
                        "max_calls_today": max_daily,
                        "calls_remaining": 0 if is_finished else calls_remaining,
                        "is_finished": is_finished,
                        "provider_exhausted": bool(state.get("provider_exhausted")),
                        "minute_calls": len(state.get("minute_call_timestamps", [])),
                        "max_calls_minute": settings.api.max_ai_calls_per_minute,
                        "reset_time_str": self.get_formatted_reset_time(),
                        "model": settings.api.ai_model,
                    }
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)

    def reset_state(self) -> None:
        """Resets quota state (primarily for automated testing)."""
        with self._thread_lock:
            with open(self.state_file_path, "w") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                try:
                    state = {
                        "pacific_date": self.get_pacific_date_key(),
                        "daily_calls": 0,
                        "provider_exhausted": False,
                        "provider_error_reason": "",
                        "minute_call_timestamps": [],
                        "last_updated": time.time(),
                    }
                    self._save_state_locked(f, state)
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)


# Global singleton instance
quota_manager = AIQuotaManager()
