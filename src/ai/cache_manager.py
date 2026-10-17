"""
Question Cache Manager.
Caches repeated energy market intelligence queries to eliminate redundant API calls
and preserve the daily free quota.
"""

import re
import json
import time
import fcntl
import logging
import threading
from pathlib import Path
from typing import Dict, Any, Optional

from config.settings import settings

logger = logging.getLogger(__name__)


def normalize_query_text(text: str) -> str:
    """Normalizes natural language question for fuzzy deduplication."""
    if not text:
        return ""
    # Lowercase, strip punctuation, collapse multiple whitespaces
    lowered = text.lower()
    cleaned = re.sub(r"[^\w\s]", " ", lowered)
    return " ".join(cleaned.split())


class QuestionCacheManager:
    """Thread-safe persistent cache for AI intelligence queries."""

    def __init__(self, cache_file_path: Optional[Path] = None, ttl_seconds: int = 86400):
        self.cache_file_path = cache_file_path or (settings.base_dir / ".ai_question_cache.json")
        self.ttl_seconds = ttl_seconds
        self._thread_lock = threading.RLock()
        self._memory_cache: Dict[str, Dict[str, Any]] = {}
        self._load_cache()

    def _load_cache(self) -> None:
        if not self.cache_file_path.exists():
            return
        try:
            with open(self.cache_file_path, "r") as f:
                data = json.load(f)
                now = time.time()
                # Filter expired
                loaded = {}
                for k, v in data.items():
                    if (now - v.get("cached_at", 0)) < self.ttl_seconds:
                        entry = v.copy()
                        resp = entry.get("response", {})
                        if "visualization_fig_dict" in resp and resp["visualization_fig_dict"]:
                            try:
                                import plotly.graph_objects as go
                                resp["visualization_fig"] = go.Figure(resp["visualization_fig_dict"])
                            except Exception:
                                pass
                        loaded[k] = entry
                self._memory_cache = loaded
        except Exception as e:
            logger.warning(f"Could not load question cache from disk: {e}")
            self._memory_cache = {}

    def get(self, question: str) -> Optional[Dict[str, Any]]:
        """Retrieves cached response if present and not expired."""
        norm_key = normalize_query_text(question)
        if not norm_key:
            return None

        with self._thread_lock:
            entry = self._memory_cache.get(norm_key)
            if entry:
                if (time.time() - entry.get("cached_at", 0)) < self.ttl_seconds:
                    res = entry.get("response", {}).copy()
                    res["served_from_cache"] = True
                    return res
                else:
                    del self._memory_cache[norm_key]
            return None

    def set(self, question: str, response: Dict[str, Any]) -> None:
        """Stores query response into cache."""
        norm_key = normalize_query_text(question)
        if not norm_key or not response:
            return

        with self._thread_lock:
            # Memory cache stores full response including visualization_fig
            mem_resp = response.copy()
            mem_resp.pop("served_from_cache", None)
            self._memory_cache[norm_key] = {
                "cached_at": time.time(),
                "original_question": question,
                "response": mem_resp,
            }
            # Disk persistence converts visualization_fig to dict for JSON serialization
            disk_cache = {}
            for k, entry in self._memory_cache.items():
                resp_copy = {}
                for rk, rv in entry["response"].items():
                    if rk == "visualization_fig":
                        if rv is not None and hasattr(rv, "to_dict"):
                            try:
                                resp_copy["visualization_fig_dict"] = rv.to_dict()
                            except Exception:
                                pass
                    else:
                        resp_copy[rk] = rv

                disk_cache[k] = {
                    "cached_at": entry["cached_at"],
                    "original_question": entry["original_question"],
                    "response": resp_copy
                }
            try:
                with open(self.cache_file_path, "w") as f:
                    fcntl.flock(f, fcntl.LOCK_EX)
                    try:
                        json.dump(disk_cache, f, indent=2)
                    finally:
                        fcntl.flock(f, fcntl.LOCK_UN)
            except Exception as e:
                logger.warning(f"Failed to persist question cache: {e}")

    def clear(self) -> None:
        """Clears memory and persistent cache."""
        with self._thread_lock:
            self._memory_cache.clear()
            if self.cache_file_path.exists():
                try:
                    self.cache_file_path.unlink()
                except Exception:
                    pass


# Global singleton instance
question_cache = QuestionCacheManager()
