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
from typing import Optional, Dict, Any, Tuple
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


# Global singleton instance
supabase_auth_client = SupabaseAuthClient()
