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
import logging
from typing import Optional, Dict, Any, Tuple, List
import requests

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

    @property
    def url(self) -> str:
        """Returns the configured Supabase project URL."""
        if self._custom_url:
            return self._custom_url.rstrip("/")
        raw = _get_config_val("SUPABASE_URL", ("NEXT_PUBLIC_SUPABASE_URL", "VITE_SUPABASE_URL"))
        return raw.rstrip("/")

    @property
    def anon_key(self) -> str:
        """Returns the configured Supabase anonymous public key."""
        if self._custom_key:
            return self._custom_key
        return _get_config_val(
            "SUPABASE_KEY",
            ("SUPABASE_ANON_KEY", "NEXT_PUBLIC_SUPABASE_ANON_KEY", "VITE_SUPABASE_ANON_KEY")
        )

    @property
    def service_role_key(self) -> str:
        """Returns optional Supabase service role key for administrative tasks."""
        if self._custom_service_key:
            return self._custom_service_key
        return _get_config_val("SUPABASE_SERVICE_ROLE_KEY", ("SUPABASE_SERVICE_KEY",))

    def is_configured(self) -> bool:
        """Checks if Supabase URL and Key are configured with non-empty values."""
        u = self.url
        k = self.anon_key
        return bool(u and k and u.startswith("http") and len(k) > 10)

    def _headers(self, token: Optional[str] = None) -> Dict[str, str]:
        """Constructs headers for Supabase API requests."""
        headers = {
            "apikey": self.anon_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        elif self.anon_key:
            headers["Authorization"] = f"Bearer {self.anon_key}"
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
            resp = requests.post(
                url,
                headers=self._headers(),
                json=payload,
                timeout=DEFAULT_TIMEOUT
            )
            data = resp.json() if resp.content else {}

            if resp.status_code in (200, 201):
                user = data.get("user") or data
                return True, "Registration successful.", user
            else:
                err_msg = data.get("msg") or data.get("error_description") or data.get("message") or f"HTTP {resp.status_code}"
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
            resp = requests.post(
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
            resp = requests.get(
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
            resp = requests.post(
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
            resp = requests.post(
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
            resp = requests.post(
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
        url = f"{self.url}/rest/v1/"
        try:
            resp = requests.get(url, headers=self._headers(), timeout=5.0)
            latency_ms = round((time.time() - start) * 1000, 1)
            if resp.status_code in (200, 204):
                return True, f"Connected to Supabase ({latency_ms}ms).", {
                    "url": self.url,
                    "latency_ms": latency_ms,
                    "status_code": resp.status_code
                }
            return False, f"Supabase responded with HTTP {resp.status_code}.", {"status_code": resp.status_code}
        except Exception as e:
            return False, f"Supabase connection test failed: {e}", {"error": str(e)}

    def select_table(
        self,
        table_name: str,
        params: Optional[Dict[str, Any]] = None,
        access_token: Optional[str] = None
    ) -> Tuple[bool, List[Dict[str, Any]], str]:
        """Queries records from a Supabase table via PostgREST."""
        if not self.is_configured():
            return False, [], "Supabase credentials are not configured."

        url = f"{self.url}/rest/v1/{table_name}"
        try:
            resp = requests.get(
                url,
                headers=self._headers(token=access_token),
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
        access_token: Optional[str] = None
    ) -> Tuple[bool, int, str]:
        """Upserts records into a Supabase table with merge-duplicates."""
        if not self.is_configured():
            return False, 0, "Supabase credentials are not configured."

        url = f"{self.url}/rest/v1/{table_name}"
        headers = self._headers(token=access_token)
        headers["Prefer"] = "resolution=merge-duplicates,return=minimal"

        try:
            resp = requests.post(url, headers=headers, json=records, timeout=DEFAULT_TIMEOUT)
            if resp.status_code in (200, 201, 204):
                return True, len(records), "Success"
            return False, 0, f"HTTP {resp.status_code}: {resp.text[:200]}"
        except Exception as e:
            return False, 0, str(e)

    def get_profile(self, user_id: str, access_token: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Retrieves user profile and preferences from public.profiles."""
        ok, rows, _ = self.select_table("profiles", {"id": f"eq.{user_id}", "limit": 1}, access_token)
        if ok and rows:
            return rows[0]
        return None

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
            resp = requests.patch(
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
            resp = requests.post(
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
            resp = requests.post(
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
        access_token: Optional[str] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Invokes check_and_consume_ai_quota stored procedure atomically.
        Returns (is_allowed, details_dict).
        """
        ok, res = self.call_rpc(
            "check_and_consume_ai_quota",
            {
                "p_user_id": user_id,
                "p_question_text": question_text,
                "p_question_hash": question_hash,
                "p_model": model_used,
                "p_max_questions": max_questions,
                "p_window_hours": window_hours
            },
            access_token=access_token
        )
        if ok and isinstance(res, dict):
            return res.get("allowed", False), res
        return False, {"allowed": False, "message": str(res)}


# Global singleton instance
supabase_auth_client = SupabaseAuthClient()

