"""
Supabase Authentication and REST Client Adapter for Global FuelPulse AI.
Provides:
- Native integration with Supabase Auth (/auth/v1/signup, /auth/v1/token, /auth/v1/user, /auth/v1/recover).
- Seamless, zero-config fallback to local database (SQLite/MySQL) when Supabase credentials are not configured.
- Concurrency-safe execution of Supabase RPC functions such as check_and_consume_ai_quota.
- Robust timeout handling, error normalization, and Streamlit secrets support.
"""

import os
import json
import time
import logging
import threading
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, Tuple, List
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10.0


def _get_config_val(name: str, fallback_names: Tuple[str, ...] = ()) -> str:
    """Retrieves configuration variable from environment or Streamlit secrets."""
    val = os.getenv(name)
    if not val:
        for fb in fallback_names:
            val = os.getenv(fb)
            if val:
                break
    if not val:
        try:
            import streamlit as st
            if hasattr(st, "secrets"):
                val = st.secrets.get(name)
                if not val:
                    for fb in fallback_names:
                        val = st.secrets.get(fb)
                        if val:
                            break
        except Exception:
            pass
    return (val or "").strip()


class SupabaseAuthClient:
    """Client adapter for Supabase Auth and Database RPC endpoints."""

    def __init__(
        self,
        supabase_url: Optional[str] = None,
        supabase_key: Optional[str] = None,
        service_role_key: Optional[str] = None
    ):
        self._custom_url = supabase_url
        self._custom_key = supabase_key
        self._custom_service_key = service_role_key
        self._http = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=20, max_retries=2)
        self._http.mount("https://", adapter)
        self._http.mount("http://", adapter)
        self._quota_cache: Dict[str, Tuple[float, Dict[str, Any]]] = {}
        self._quota_lock = threading.RLock()

    @property
    def url(self) -> str:
        """Returns the configured Supabase project URL."""
        if self._custom_url is not None:
            return self._custom_url.rstrip("/")
        raw = _get_config_val("SUPABASE_URL", ("NEXT_PUBLIC_SUPABASE_URL", "VITE_SUPABASE_URL"))
        return raw.rstrip("/")

    @property
    def anon_key(self) -> str:
        """Returns the configured Supabase anonymous public key."""
        if self._custom_key is not None:
            return self._custom_key
        return _get_config_val(
            "SUPABASE_KEY",
            ("SUPABASE_ANON_KEY", "NEXT_PUBLIC_SUPABASE_ANON_KEY", "VITE_SUPABASE_ANON_KEY")
        )

    @property
    def service_role_key(self) -> str:
        """Returns optional Supabase service role key for administrative tasks."""
        if self._custom_service_key is not None:
            return self._custom_service_key
        return _get_config_val("SUPABASE_SERVICE_ROLE_KEY", ("SUPABASE_SERVICE_KEY",))

    def is_configured(self) -> bool:
        """Checks if Supabase URL and Key are configured with non-empty values."""
        u = self.url
        k = self.anon_key
        return bool(u and k and u.startswith("http") and len(k) > 10)

    def _headers(self, token: Optional[str] = None, use_service_key: bool = False) -> Dict[str, str]:
        """Constructs headers for Supabase API requests."""
        key = self.service_role_key if (use_service_key and self.service_role_key) else self.anon_key
        headers = {
            "apikey": key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        elif use_service_key and self.service_role_key:
            headers["Authorization"] = f"Bearer {self.service_role_key}"
        elif key:
            headers["Authorization"] = f"Bearer {key}"
        return headers

    def sign_up(
        self,
        email: str,
        password: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Signs up a user with Supabase Auth (/auth/v1/signup).
        Returns (success, message, user_data_dict).
        """
        if not self.is_configured():
            return False, "Supabase credentials are not configured.", None

        clean_email = (email or "").strip().lower()
        if not clean_email or "@" not in clean_email:
            return False, "Please enter a valid email address.", None
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters.", None

        url = f"{self.url}/auth/v1/signup"
        payload = {
            "email": clean_email,
            "password": password,
            "data": metadata or {}
        }

        try:
            resp = self._http.post(
                url,
                headers=self._headers(),
                json=payload,
                timeout=DEFAULT_TIMEOUT
            )
            data = resp.json() if resp.content else {}

            if resp.status_code in (200, 201):
                user = data.get("user") or data
                user_id = user.get("id")
                # Auto-confirm user via Admin API if service role key is configured so login works immediately
                if user_id and self.service_role_key:
                    try:
                        admin_url = f"{self.url}/auth/v1/admin/users/{user_id}"
                        self._http.put(
                            admin_url,
                            headers=self._headers(use_service_key=True),
                            json={"email_confirm": True},
                            timeout=DEFAULT_TIMEOUT
                        )
                    except Exception as ce:
                        logger.debug(f"Auto-confirm notice: {ce}")

                # Ensure user profile exists in public.profiles table
                if user_id:
                    u_meta = metadata or {}
                    self.ensure_profile_exists(
                        user_id=user_id,
                        email=clean_email,
                        username=u_meta.get("username", clean_email.split("@")[0]),
                        full_name=u_meta.get("full_name")
                    )

                return True, "Registration successful.", user
            else:
                err_msg = data.get("msg") or data.get("error_description") or data.get("message") or f"HTTP {resp.status_code}"
                # If rate limit is encountered, fallback to admin user creation since service role key is present
                if any(k in err_msg.lower() for k in ("rate limit", "over_email_send_rate_limit")) and self.service_role_key:
                    try:
                        admin_create_url = f"{self.url}/auth/v1/admin/users"
                        admin_resp = self._http.post(
                            admin_create_url,
                            headers=self._headers(use_service_key=True),
                            json={
                                "email": clean_email,
                                "password": password,
                                "email_confirm": True,
                                "user_metadata": metadata or {}
                            },
                            timeout=DEFAULT_TIMEOUT
                        )
                        if admin_resp.status_code in (200, 201):
                            admin_data = admin_resp.json()
                            user = admin_data.get("user") or admin_data
                            user_id = user.get("id")
                            if user_id:
                                u_meta = metadata or {}
                                self.ensure_profile_exists(
                                    user_id=user_id,
                                    email=clean_email,
                                    username=u_meta.get("username", clean_email.split("@")[0]),
                                    full_name=u_meta.get("full_name")
                                )
                            return True, "Registration successful via admin.", user
                    except Exception as ae:
                        logger.debug(f"Admin user creation fallback notice: {ae}")

                return False, f"Supabase Registration error: {err_msg}", None
        except Exception as e:
            logger.error(f"Supabase sign_up error: {e}")
            return False, f"Supabase connection error: {str(e)}", None

    def sign_in_with_password(
        self,
        email: str,
        password: str
    ) -> Tuple[bool, str, Optional[str], Optional[Dict[str, Any]]]:
        """
        Authenticates a user via Supabase Auth (/auth/v1/token?grant_type=password).
        Returns (success, message, access_token, user_dict).
        """
        if not self.is_configured():
            return False, "Supabase credentials are not configured.", None, None

        clean_email = (email or "").strip().lower()
        if not clean_email or not password:
            return False, "Please provide both email and password.", None, None

        url = f"{self.url}/auth/v1/token?grant_type=password"
        payload = {
            "email": clean_email,
            "password": password
        }

        try:
            resp = self._http.post(
                url,
                headers=self._headers(),
                json=payload,
                timeout=DEFAULT_TIMEOUT
            )
            data = resp.json() if resp.content else {}

            if resp.status_code == 200:
                access_token = data.get("access_token")
                user = data.get("user") or {}
                user_meta = user.get("user_metadata") or {}
                user_dict = {
                    "user_id": user.get("id"),
                    "email": user.get("email"),
                    "username": user_meta.get("username") or user.get("email", "").split("@")[0],
                    "full_name": user_meta.get("full_name") or user.get("email", "").split("@")[0].capitalize(),
                    "provider": "supabase",
                    "access_token": access_token
                }
                return True, "Login successful.", access_token, user_dict
            else:
                err_msg = data.get("error_description") or data.get("msg") or data.get("message") or f"HTTP {resp.status_code}"
                return False, f"Supabase Login failed: {err_msg}", None, None
        except Exception as e:
            logger.error(f"Supabase sign_in error: {e}")
            return False, f"Supabase connection error: {str(e)}", None, None

    def get_user(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Fetches the authenticated user profile from Supabase Auth (/auth/v1/user).
        """
        if not self.is_configured() or not access_token:
            return None

        url = f"{self.url}/auth/v1/user"
        try:
            resp = self._http.get(
                url,
                headers=self._headers(token=access_token),
                timeout=DEFAULT_TIMEOUT
            )
            if resp.status_code == 200:
                user = resp.json()
                user_meta = user.get("user_metadata") or {}
                return {
                    "user_id": user.get("id"),
                    "email": user.get("email"),
                    "username": user_meta.get("username") or user.get("email", "").split("@")[0],
                    "full_name": user_meta.get("full_name") or user.get("email", "").split("@")[0].capitalize(),
                    "provider": "supabase",
                    "access_token": access_token
                }
            return None
        except Exception as e:
            logger.error(f"Supabase get_user error: {e}")
            return None

    def sign_out(self, access_token: Optional[str]) -> bool:
        """
        Logs out user and invalidates session token via Supabase Auth (/auth/v1/logout).
        """
        if not self.is_configured() or not access_token:
            return True

        url = f"{self.url}/auth/v1/logout"
        try:
            resp = self._http.post(
                url,
                headers=self._headers(token=access_token),
                timeout=DEFAULT_TIMEOUT
            )
            return resp.status_code in (200, 204)
        except Exception as e:
            logger.error(f"Supabase sign_out error: {e}")
            return False

    def reset_password_for_email(self, email: str) -> Tuple[bool, str]:
        """
        Sends a password recovery email via Supabase Auth (/auth/v1/recover).
        """
        if not self.is_configured():
            return False, "Supabase credentials are not configured."

        clean_email = (email or "").strip().lower()
        if not clean_email or "@" not in clean_email:
            return False, "Please provide a valid email address."

        url = f"{self.url}/auth/v1/recover"
        try:
            resp = self._http.post(
                url,
                headers=self._headers(),
                json={"email": clean_email},
                timeout=DEFAULT_TIMEOUT
            )
            if resp.status_code in (200, 204):
                return True, "Password reset email sent successfully."
            data = resp.json() if resp.content else {}
            err_msg = data.get("msg") or data.get("message") or f"HTTP {resp.status_code}"
            return False, f"Password reset failed: {err_msg}"
        except Exception as e:
            return False, f"Supabase recover error: {str(e)}"

    def call_rpc(
        self,
        function_name: str,
        params: Dict[str, Any],
        access_token: Optional[str] = None
    ) -> Tuple[bool, Any]:
        """
        Calls a PostgreSQL RPC function exposed via Supabase PostgREST (/rest/v1/rpc/{function_name}).
        """
        if not self.is_configured():
            return False, "Supabase credentials are not configured."

        url = f"{self.url}/rest/v1/rpc/{function_name}"
        try:
            resp = self._http.post(
                url,
                headers=self._headers(token=access_token),
                json=params,
                timeout=DEFAULT_TIMEOUT
            )
            if resp.status_code in (200, 201):
                return True, resp.json()
            data = resp.json() if resp.content else {}
            return False, data.get("message") or f"HTTP {resp.status_code}"
        except Exception as e:
            logger.error(f"Supabase RPC {function_name} error: {e}")
            return False, str(e)

    def test_connection(self) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Tests the connection to the configured Supabase project.
        Returns (is_connected, message, details_dict).
        """
        if not self.is_configured():
            return False, "Supabase is not configured (missing SUPABASE_URL or SUPABASE_KEY).", {}

        import time
        start = time.time()
        try:
            # First check auth endpoint
            auth_resp = self._http.get(f"{self.url}/auth/v1/health", headers=self._headers(), timeout=5.0)
            latency_ms = round((time.time() - start) * 1000, 1)
            if auth_resp.status_code in (200, 204):
                return True, f"Connected to Supabase ({latency_ms}ms).", {
                    "url": self.url,
                    "latency_ms": latency_ms,
                    "status_code": auth_resp.status_code,
                    "auth_healthy": True
                }

            # Fallback to REST root with service key
            rest_resp = self._http.get(f"{self.url}/rest/v1/", headers=self._headers(use_service_key=True), timeout=5.0)
            latency_ms = round((time.time() - start) * 1000, 1)
            if rest_resp.status_code in (200, 204):
                return True, f"Connected to Supabase ({latency_ms}ms).", {
                    "url": self.url,
                    "latency_ms": latency_ms,
                    "status_code": rest_resp.status_code
                }
            return False, f"Supabase responded with HTTP {auth_resp.status_code}.", {"status_code": auth_resp.status_code}
        except Exception as e:
            return False, f"Supabase connection test failed: {e}", {"error": str(e)}

    def select_table(
        self,
        table_name: str,
        params: Optional[Dict[str, Any]] = None,
        access_token: Optional[str] = None,
        use_service_key: bool = False
    ) -> Tuple[bool, List[Dict[str, Any]], str]:
        """Queries records from a Supabase table via PostgREST."""
        if not self.is_configured():
            return False, [], "Supabase credentials are not configured."

        url = f"{self.url}/rest/v1/{table_name}"
        try:
            resp = self._http.get(
                url,
                headers=self._headers(token=access_token, use_service_key=use_service_key),
                params=params or {},
                timeout=DEFAULT_TIMEOUT
            )
            if resp.status_code == 200:
                return True, resp.json(), "Success"
            return False, [], f"HTTP {resp.status_code}: {resp.text[:200]}"
        except Exception as e:
            return False, [], str(e)

    def upsert_table(
        self,
        table_name: str,
        records: List[Dict[str, Any]],
        access_token: Optional[str] = None,
        use_service_key: bool = False
    ) -> Tuple[bool, int, str]:
        """Upserts records into a Supabase table with merge-duplicates."""
        if not self.is_configured():
            return False, 0, "Supabase credentials are not configured."

        url = f"{self.url}/rest/v1/{table_name}"
        headers = self._headers(token=access_token, use_service_key=use_service_key)
        headers["Prefer"] = "resolution=merge-duplicates,return=representation"

        try:
            resp = self._http.post(url, headers=headers, json=records, timeout=DEFAULT_TIMEOUT)
            if resp.status_code in (200, 201, 204):
                return True, len(records), "Success"
            return False, 0, f"HTTP {resp.status_code}: {resp.text[:200]}"
        except Exception as e:
            return False, 0, str(e)

    def get_profile(self, user_id: str, access_token: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Retrieves user profile and preferences from public.profiles."""
        ok, rows, _ = self.select_table("profiles", {"id": f"eq.{user_id}", "limit": 1}, access_token=access_token, use_service_key=True)
        if ok and rows:
            return rows[0]
        return None

    def ensure_profile_exists(
        self,
        user_id: str,
        email: str,
        username: str,
        full_name: Optional[str] = None
    ) -> bool:
        """Guarantees a profile record exists in public.profiles for the user."""
        if not self.is_configured() or not user_id:
            return False
        clean_user = (username or email.split("@")[0]).strip().lower()
        clean_name = (full_name or clean_user.capitalize()).strip()
        rec = [{
            "id": user_id,
            "email": email.strip().lower(),
            "username": clean_user,
            "full_name": clean_name,
            "role": "analyst",
            "preferences": {"theme": "dark", "default_fuel": "petrol", "notifications": True}
        }]
        ok, _, msg = self.upsert_table("profiles", rec, use_service_key=True)
        return ok

    def update_profile_preferences(
        self,
        user_id: str,
        preferences: Dict[str, Any],
        access_token: Optional[str] = None
    ) -> bool:
        """Updates user preferences in public.profiles."""
        if not self.is_configured():
            return False

        url = f"{self.url}/rest/v1/profiles?id=eq.{user_id}"
        headers = self._headers(token=access_token)
        headers["Prefer"] = "return=minimal"
        try:
            resp = self._http.patch(
                url,
                headers=headers,
                json={"preferences": preferences, "updated_at": "now()"},
                timeout=DEFAULT_TIMEOUT
            )
            return resp.status_code in (200, 204)
        except Exception as e:
            logger.error(f"Update preferences error: {e}")
            return False

    def create_conversation(
        self,
        user_id: str,
        title: str = "New Energy Consultation",
        access_token: Optional[str] = None
    ) -> Optional[str]:
        """Creates a new conversation record in public.chat_conversations."""
        if not self.is_configured():
            return None

        url = f"{self.url}/rest/v1/chat_conversations"
        headers = self._headers(token=access_token)
        headers["Prefer"] = "return=representation"
        try:
            resp = self._http.post(
                url,
                headers=headers,
                json={"user_id": user_id, "title": title},
                timeout=DEFAULT_TIMEOUT
            )
            if resp.status_code in (200, 201):
                data = resp.json()
                if isinstance(data, list) and data:
                    return data[0].get("conversation_id")
            return None
        except Exception as e:
            logger.error(f"Create conversation error: {e}")
            return None

    def save_chat_message(
        self,
        conversation_id: str,
        user_id: str,
        role: str,
        content: str,
        sources_cited: Optional[List[str]] = None,
        tokens_used: int = 0,
        access_token: Optional[str] = None
    ) -> bool:
        """Persists a chat message in public.chat_messages."""
        if not self.is_configured():
            return False

        url = f"{self.url}/rest/v1/chat_messages"
        headers = self._headers(token=access_token)
        headers["Prefer"] = "return=minimal"
        try:
            resp = self._http.post(
                url,
                headers=headers,
                json={
                    "conversation_id": conversation_id,
                    "user_id": user_id,
                    "role": role,
                    "content": content,
                    "sources_cited": sources_cited or [],
                    "tokens_used": tokens_used
                },
                timeout=DEFAULT_TIMEOUT
            )
            return resp.status_code in (200, 201, 204)
        except Exception as e:
            logger.error(f"Save chat message error: {e}")
            return False

    def check_and_consume_quota(
        self,
        user_id: str,
        question_text: str,
        question_hash: str,
        model_used: str = "gemini-2.0-flash",
        max_questions: int = 3,
        window_hours: int = 24,
        request_id: Optional[str] = None,
        access_token: Optional[str] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Atomically checks and consumes 1 question quota unit.
        Attempts Supabase RPC first; falls back cleanly to authoritative table-level
        accounting if the RPC function is not present in the database.
        Returns (is_allowed, details_dict).
        """
        import uuid

        with self._quota_lock:
            # 1. Attempt PostgreSQL RPC
            ok, res = self.call_rpc(
                "check_and_consume_ai_quota",
                {
                    "p_user_id": user_id,
                    "p_question_text": question_text,
                    "p_question_hash": question_hash,
                    "p_request_id": request_id,
                    "p_model": model_used,
                    "p_max_questions": max_questions,
                    "p_window_hours": window_hours
                },
                access_token=access_token
            )
            if ok and isinstance(res, dict) and "allowed" in res:
                try:
                    from src.auth.quota_service import quota_service
                    quota_service.invalidate_cache(user_id)
                except Exception:
                    pass
                self._quota_cache.pop(user_id, None)
                return res.get("allowed", False), res

            # 2. Authoritative Table & Local Fallback
            from src.auth.quota_service import quota_service
            summary = quota_service.get_quota_summary(user_id, max_questions=max_questions, window_hours=window_hours, bypass_cache=True)
            used = summary.get("used", 0)
            rem = summary.get("remaining", max_questions)

            if rem <= 0 or summary.get("quota_exhausted"):
                return False, {
                    "allowed": False,
                    "reason": "quota_exhausted",
                    "questions_used": used,
                    "questions_remaining": 0,
                    "reset_timestamp": summary.get("resets_at"),
                    "reset_time_str": summary.get("reset_time_str", "24 hours")
                }

            # User is allowed: record usage row in Supabase and SQLite
            new_usage_id = str(uuid.uuid4())
            rec = {
                "usage_id": new_usage_id,
                "user_id": user_id,
                "question_text": question_text[:500],
                "question_hash": question_hash,
                "status": "completed",
                "model_used": model_used,
                "tokens_used": 0
            }
            if self.is_configured():
                self.upsert_table("ai_question_usages", [rec], use_service_key=True)

            # Also mirror in local SQLite
            try:
                from src.database.connection import db_manager
                from src.database.models import AIQuestionUsage
                with db_manager.get_session() as session:
                    local_u = AIQuestionUsage(
                        user_id=user_id,
                        question_text=question_text[:500],
                        question_hash=question_hash,
                        status="completed",
                        model_used=model_used,
                        tokens_used=0,
                        request_id=request_id,
                        quota_unit_consumed=True
                    )
                    session.add(local_u)
                    session.commit()
            except Exception as e:
                logger.debug(f"Local usage record notice: {e}")

            quota_service.invalidate_cache(user_id)
            new_summary = quota_service.get_quota_summary(user_id, max_questions=max_questions, window_hours=window_hours, bypass_cache=True)
            return True, {
                "allowed": True,
                "usage_id": new_usage_id,
                "questions_used": new_summary.get("used", used + 1),
                "questions_remaining": new_summary.get("remaining", max(0, rem - 1)),
                "reset_timestamp": new_summary.get("resets_at"),
                "reset_time_str": new_summary.get("reset_time_str", "24 hours")
            }

    def refund_quota(
        self,
        user_id: str,
        usage_id: Optional[str] = None,
        request_id: Optional[str] = None
    ) -> bool:
        """
        Safely refunds a reserved quota slot if provider/network fails before answer delivery.
        Marks status='failed' so it is excluded from rolling 24-hour quota calculation.
        """
        if not user_id:
            return False
        # Update Supabase ai_question_usages
        if self.is_configured() and usage_id:
            try:
                url = f"{self.url}/rest/v1/ai_question_usages"
                headers = self._headers(use_service_key=True)
                params = {"usage_id": f"eq.{usage_id}"}
                self._http.patch(url, headers=headers, params=params, json={"status": "failed"}, timeout=DEFAULT_TIMEOUT)
            except Exception as e:
                logger.debug(f"Supabase refund patch error: {e}")

        # Update local SQLite
        try:
            from src.database.connection import db_manager
            from src.database.models import AIQuestionUsage
            with db_manager.get_session() as session:
                q = session.query(AIQuestionUsage).filter(AIQuestionUsage.user_id == user_id)
                if request_id:
                    q = q.filter(AIQuestionUsage.request_id == request_id)
                row = q.order_by(AIQuestionUsage.created_at.desc()).first()
                if row:
                    row.status = "failed"
                    row.quota_unit_consumed = False
                    session.commit()
        except Exception as e:
            logger.debug(f"SQLite refund error: {e}")

        try:
            from src.auth.quota_service import quota_service
            quota_service.invalidate_cache(user_id)
        except Exception:
            pass
        return True

    def record_login(
        self,
        user_id: str,
        event_type: str = "login",
        result: str = "success",
        session_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        access_token: Optional[str] = None
    ) -> bool:
        """
        Records an authentication event in public.user_login_history and updates profile.last_login_at.
        """
        if not self.is_configured() or not user_id:
            return False

        # Attempt RPC first
        ok, res = self.call_rpc(
            "record_user_login",
            {
                "p_user_id": user_id,
                "p_event_type": event_type,
                "p_result": result,
                "p_session_id": session_id,
                "p_ip_address": ip_address,
                "p_user_agent": user_agent
            },
            access_token=access_token
        )
        if ok:
            return True

        # Fallback to direct PostgREST insert and patch
        try:
            self.upsert_table(
                "user_login_history",
                [{
                    "user_id": user_id,
                    "event_type": event_type,
                    "result": result,
                    "session_id": session_id,
                    "ip_address": ip_address,
                    "user_agent": user_agent
                }],
                use_service_key=True
            )
            if result == "success" and event_type == "login":
                self.update_profile_preferences(user_id, {}, access_token=access_token)
            return True
        except Exception as e:
            logger.debug(f"Direct login history logging error: {e}")
            return False

    def get_user_login_history(
        self,
        user_id: str,
        limit: int = 5,
        access_token: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieves recent login events for an authenticated user from Supabase."""
        if not self.is_configured() or not user_id:
            return []
        ok, rows, _ = self.select_table(
            "user_login_history",
            {
                "user_id": f"eq.{user_id}",
                "order": "login_timestamp.desc",
                "limit": str(limit)
            },
            access_token=access_token,
            use_service_key=True
        )
        return rows if (ok and isinstance(rows, list)) else []

    def get_user_question_history(
        self,
        user_id: str,
        limit: int = 10,
        access_token: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieves private AI question history for an authenticated user."""
        if not self.is_configured() or not user_id:
            return []
        ok, rows, _ = self.select_table(
            "ai_question_usages",
            {
                "user_id": f"eq.{user_id}",
                "order": "created_at.desc",
                "limit": str(limit),
                "select": "usage_id,question_text,created_at,status,model_used,quota_unit_consumed"
            },
            access_token=access_token,
            use_service_key=True
        )
        return rows if (ok and isinstance(rows, list)) else []

    def resolve_email_from_username(self, username: str) -> Optional[str]:
        """Resolves an email address for a given username from public.profiles."""
        if not self.is_configured() or not username:
            return None
        clean_user = username.strip().lower()
        ok, rows, _ = self.select_table(
            "profiles",
            {"username": f"eq.{clean_user}", "select": "email", "limit": 1},
            use_service_key=True
        )
        if ok and rows and isinstance(rows, list) and len(rows) > 0 and rows[0].get("email"):
            return str(rows[0]["email"]).strip().lower()
        return None

    def get_user_quota_status(
        self,
        user_id: str,
        access_token: Optional[str] = None,
        max_questions: int = 3,
        window_hours: int = 24
    ) -> Dict[str, Any]:
        """
        Retrieves the authoritative 24-hour AI question quota status for a user.
        Delegates to the unified QuotaService while supporting direct client mocks.
        """
        if self.is_configured() and user_id:
            try:
                ok, rows, _ = self.select_table(
                    "ai_question_usages",
                    {
                        "user_id": f"eq.{user_id}",
                        "status": "eq.completed",
                        "select": "usage_id,created_at,quota_unit_consumed"
                    },
                    access_token=access_token,
                    use_service_key=True
                )
                if ok and isinstance(rows, list) and len(rows) > 0:
                    used = len([r for r in rows if r.get("quota_unit_consumed") is not False])
                    rem = max(0, max_questions - used)
                    is_ex = (rem <= 0)
                    return {
                        "allowed": not is_ex,
                        "used": used,
                        "limit": max_questions,
                        "remaining": rem,
                        "window_started_at": rows[0].get("created_at"),
                        "resets_at": None,
                        "reset_timestamp": None,
                        "reset_time_str": f"{window_hours} hours",
                        "quota_exhausted": is_ex,
                        "is_exhausted": is_ex,
                        "questions_used": used,
                        "questions_remaining": rem,
                        "daily_questions_used": used,
                        "daily_questions_remaining": rem,
                        "used_count": used,
                        "max_questions": max_questions,
                        "total_historical": len(rows),
                        "badge_text": f"{used}/{max_questions} Used • {rem} Left"
                    }
            except Exception:
                pass

        from src.auth.quota_service import quota_service
        summary = quota_service.get_quota_summary(user_id, max_questions=max_questions, window_hours=window_hours)

        # Return backward-compatible mapping containing all requested keys
        return {
            "allowed": not summary["quota_exhausted"],
            "used": summary["used"],
            "limit": summary["limit"],
            "remaining": summary["remaining"],
            "window_started_at": summary["window_started_at"],
            "resets_at": summary["resets_at"],
            "reset_timestamp": summary["resets_at"],
            "reset_time_str": summary["reset_time_str"],
            "quota_exhausted": summary["quota_exhausted"],
            "is_exhausted": summary["quota_exhausted"],
            "questions_used": summary["used"],
            "questions_remaining": summary["remaining"],
            "daily_questions_used": summary["used"],
            "daily_questions_remaining": summary["remaining"],
            "used_count": summary["used"],
            "max_questions": summary["limit"],
            "total_historical": summary["total_historical"],
            "badge_text": summary["badge_text"]
        }

    def mark_quota_usage_failed(
        self,
        usage_id: int,
        reason: str = "provider_error",
        access_token: Optional[str] = None
    ) -> bool:
        """Marks an existing usage record as failed so it does not penalize user's quota."""
        if not self.is_configured() or not usage_id:
            return False

        url = f"{self.url}/rest/v1/ai_question_usages?usage_id=eq.{usage_id}"
        headers = self._headers(token=access_token)
        headers["Prefer"] = "return=minimal"
        try:
            resp = self._http.patch(
                url,
                headers=headers,
                json={"status": "failed", "model_used": f"failed_{reason[:30]}"},
                timeout=DEFAULT_TIMEOUT
            )
            return resp.status_code in (200, 204)
        except Exception as e:
            logger.error(f"Failed to mark usage failed: {e}")
    def get_oauth_sign_in_url(
        self,
        provider: str,
        redirect_to: Optional[str] = None,
        scopes: Optional[str] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Initiates OAuth authentication through Supabase Auth (GoTrue).
        Returns (success, message_or_status, authorization_url).
        When the provider is properly enabled in Supabase, returns (True, "Ready", oauth_url).
        When the provider is not enabled, returns (False, error_explanation, None).
        """
        if not self.is_configured():
            return False, "Supabase client is not configured.", None

        provider_clean = (provider or "").strip().lower()
        if provider_clean not in ("google", "github"):
            return False, f"Provider '{provider}' is not supported. Use 'google' or 'github'.", None

        redirect = redirect_to or "http://localhost:8501"
        import urllib.parse
        params = {
            "provider": provider_clean,
            "redirect_to": redirect
        }
        if scopes:
            params["scopes"] = scopes

        url = f"{self.url}/auth/v1/authorize?{urllib.parse.urlencode(params)}"
        headers = self._headers()

        try:
            # Query the authorize endpoint with allow_redirects=False to verify provider readiness
            resp = self._http.get(url, headers=headers, allow_redirects=False, timeout=DEFAULT_TIMEOUT)

            # A 302, 303, or 307 redirect indicates Supabase recognized the provider and returned the consent URL
            if resp.status_code in (301, 302, 303, 307, 308) and "Location" in resp.headers:
                auth_url = resp.headers["Location"]
                return True, "Redirect URL generated successfully.", auth_url

            # If Supabase returns HTTP 400 with "provider is not enabled"
            if resp.status_code == 400:
                try:
                    err_json = resp.json()
                    msg = err_json.get("msg") or err_json.get("error_description") or "Provider is not enabled."
                except Exception:
                    msg = resp.text
                return False, f"Supabase OAuth Provider Not Enabled: {msg}", None

            # Fallback URL if Supabase returns 200 or unexpected status
            return True, "Using direct Supabase OAuth authorize endpoint.", url

        except Exception as e:
            logger.error(f"Error querying Supabase OAuth authorize: {e}")
            return False, f"Network error contacting Supabase Auth: {e}", None

    def generate_admin_magic_link(
        self,
        email: str,
        redirect_to: Optional[str] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Generates a direct, cryptographically verified Supabase sign-in link via the Admin API.
        Returns (success, message, action_link).
        """
        if not self.is_configured() or not self.service_role_key:
            return False, "Supabase service credentials not configured.", None

        clean_email = (email or "").strip().lower()
        if not clean_email or "@" not in clean_email:
            return False, "Please provide a valid email address.", None

        url = f"{self.url}/auth/v1/admin/generate_link"
        headers = self._headers(use_service_key=True)
        payload = {
            "type": "magiclink",
            "email": clean_email,
            "redirect_to": redirect_to or "http://localhost:8501"
        }
        try:
            resp = self._http.post(url, headers=headers, json=payload, timeout=DEFAULT_TIMEOUT)
            if resp.status_code == 200:
                data = resp.json()
                action_link = data.get("action_link")
                return True, "Supabase verified sign-in link ready.", action_link
            data = resp.json() if resp.content else {}
            err_msg = data.get("msg") or data.get("message") or f"HTTP {resp.status_code}"
            return False, f"Supabase admin link error: {err_msg}", None
        except Exception as e:
            logger.error(f"Error generating Supabase admin link: {e}")
            return False, f"Connection error: {e}", None

    def exchange_code_for_session(
        self,
        code: str
    ) -> Tuple[bool, str, Optional[str], Optional[Dict[str, Any]]]:
        """
        Exchanges an OAuth authorization code or PKCE auth_code for a valid Supabase JWT session.
        Returns (success, message, access_token, user_dict).
        """
        if not self.is_configured():
            return False, "Supabase client is not configured.", None, None

        if not code or not code.strip():
            return False, "Missing authorization code.", None, None

        clean_code = code.strip()
        url = f"{self.url}/auth/v1/token?grant_type=pkce"
        headers = self._headers()
        payload = {"auth_code": clean_code}

        try:
            resp = self._http.post(url, headers=headers, json=payload, timeout=DEFAULT_TIMEOUT)
            # If PKCE fails, try standard authorization_code grant
            if resp.status_code not in (200, 201):
                url_auth = f"{self.url}/auth/v1/token?grant_type=authorization_code"
                resp = self._http.post(url_auth, headers=headers, json={"code": clean_code}, timeout=DEFAULT_TIMEOUT)

            if resp.status_code in (200, 201):
                data = resp.json()
                token = data.get("access_token")
                raw_user = data.get("user") or {}
                meta = raw_user.get("user_metadata") or {}
                email = raw_user.get("email") or meta.get("email") or ""
                username = meta.get("username") or meta.get("user_name") or (email.split("@")[0] if email else "oauth_user")
                full_name = meta.get("full_name") or meta.get("name") or username.capitalize()

                user_dict = {
                    "user_id": raw_user.get("id"),
                    "email": email,
                    "username": username,
                    "full_name": full_name,
                    "avatar_url": meta.get("avatar_url") or meta.get("picture"),
                    "provider": raw_user.get("app_metadata", {}).get("provider") or "oauth",
                    "created_at": raw_user.get("created_at")
                }
                return True, "OAuth session established.", token, user_dict
            else:
                try:
                    err_data = resp.json()
                    err_msg = err_data.get("msg") or err_data.get("error_description") or resp.text
                except Exception:
                    err_msg = resp.text
                return False, f"Code exchange failed: {err_msg}", None, None

        except Exception as e:
            logger.error(f"Failed to exchange OAuth code: {e}")
            return False, f"Network error during OAuth token exchange: {e}", None, None


# Global singleton instance
supabase_auth_client = SupabaseAuthClient()

