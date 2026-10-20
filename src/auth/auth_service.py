"""
Authentication and Secure Identity Management for Global FuelPulse AI.
Provides:
- PBKDF2-HMAC-SHA256 password hashing with crypto salts.
- Database-backed user registration and session management.
- Stable, authenticated user identity validation.
- Default seeded analyst account for instant zero-config testing.
"""

import os
import hmac
import hashlib
import secrets
import uuid
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.database.connection import db_manager
from src.database.models import User, UserSession
from src.auth.supabase_client import supabase_auth_client

logger = logging.getLogger(__name__)

def utc_now() -> datetime:
    """Returns timezone-naive UTC datetime compatible with database schemas."""
    return datetime.now(timezone.utc).replace(tzinfo=None)

# Constants
DEFAULT_SESSION_DURATION_DAYS = 30
PASSWORD_SALT_BYTES = 16
PBKDF2_ITERATIONS = 120_000

DEFAULT_DEMO_USER_ID = "00000000-0000-0000-0000-000000000001"
DEFAULT_DEMO_EMAIL = "analyst@fuelpulse.ai"
DEFAULT_DEMO_USERNAME = "energy_analyst"
DEFAULT_DEMO_PASSWORD = "FuelPulse2026!"


def hash_password(password: str) -> str:
    """Hashes a plaintext password using PBKDF2-HMAC-SHA256 with a random salt."""
    salt = secrets.token_bytes(PASSWORD_SALT_BYTES)
    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS
    )
    return f"{salt.hex()}:{derived.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    """Verifies a plaintext password against a stored salt:hash string."""
    if not password or not password_hash or ":" not in password_hash:
        return False
    try:
        salt_hex, hash_hex = password_hash.split(":", 1)
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)
        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            PBKDF2_ITERATIONS
        )
        return hmac.compare_digest(actual_hash, expected_hash)
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False


class AuthService:
    """Service handling user registration, authentication, and session tokens."""

    @classmethod
    def ensure_default_demo_user(cls) -> User:
        """Ensures the standard demo analyst account exists in the database."""
        with db_manager.get_session() as session:
            existing = session.query(User).filter(
                (User.user_id == DEFAULT_DEMO_USER_ID) | (User.email == DEFAULT_DEMO_EMAIL)
            ).first()
            if existing:
                session.refresh(existing)
                session.expunge(existing)
                return existing

            demo_user = User(
                user_id=DEFAULT_DEMO_USER_ID,
                username=DEFAULT_DEMO_USERNAME,
                email=DEFAULT_DEMO_EMAIL,
                password_hash=hash_password(DEFAULT_DEMO_PASSWORD),
                full_name="Global FuelPulse Senior Analyst",
                is_active=True,
                created_at=utc_now()
            )
            session.add(demo_user)
            session.commit()
            session.refresh(demo_user)
            session.expunge(demo_user)
            logger.info("Default demo analyst user seeded: %s", DEFAULT_DEMO_EMAIL)
            return demo_user

    @classmethod
    def register_user(
        cls,
        username: str,
        email: str,
        password: str,
        full_name: Optional[str] = None
    ) -> Tuple[bool, str, Optional[User]]:
        """
        Registers a new user in the database.
        Returns (success, message, user_object).
        """
        username_clean = (username or "").strip().lower()
        email_clean = (email or "").strip().lower()
        if not username_clean or len(username_clean) < 3:
            return False, "Username must be at least 3 characters long.", None
        if not email_clean or "@" not in email_clean or "." not in email_clean:
            return False, "Please enter a valid email address.", None
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters long.", None

        # Supabase Integration: attempt cloud registration if configured
        if supabase_auth_client.is_configured():
            meta = {"username": username_clean, "full_name": (full_name or "").strip() or username_clean.capitalize()}
            sb_ok, sb_msg, sb_user = supabase_auth_client.sign_up(email_clean, password, meta)
            if sb_ok and sb_user:
                user_id = (sb_user.get("id") if isinstance(sb_user, dict) else None) or str(uuid.uuid4())
                with db_manager.get_session() as session:
                    existing = session.query(User).filter(
                        (User.username == username_clean) | (User.email == email_clean) | (User.user_id == user_id)
                    ).first()
                    if not existing:
                        new_user = User(
                            user_id=user_id,
                            username=username_clean,
                            email=email_clean,
                            password_hash=hash_password(password),
                            full_name=(full_name or "").strip() or username_clean.capitalize(),
                            is_active=True,
                            created_at=utc_now()
                        )
                        session.add(new_user)
                        session.commit()
                        session.refresh(new_user)
                        session.expunge(new_user)
                        return True, "User registered successfully via Supabase.", new_user
                    session.expunge(existing)
                    return True, "User registered successfully via Supabase.", existing
            elif not sb_ok and "already registered" in sb_msg.lower():
                return False, "An account with this email already exists.", None

        with db_manager.get_session() as session:
            # Check existing username or email
            existing = session.query(User).filter(
                (User.username == username_clean) | (User.email == email_clean)
            ).first()
            if existing:
                if existing.username == username_clean:
                    return False, "Username is already taken.", None
                return False, "An account with this email already exists.", None

            new_user = User(
                user_id=str(uuid.uuid4()),
                username=username_clean,
                email=email_clean,
                password_hash=hash_password(password),
                full_name=(full_name or "").strip() or username_clean.capitalize(),
                is_active=True,
                created_at=utc_now()
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            session.expunge(new_user)
            return True, "User registered successfully.", new_user

    @classmethod
    def login_user(
        cls,
        username_or_email: str,
        password: str
    ) -> Tuple[bool, str, Optional[str], Optional[Dict[str, Any]]]:
        """
        Authenticates a user and creates a secure session token.
        Returns (success, message, session_token, user_dict).
        """
        ident = (username_or_email or "").strip().lower()
        if not ident or not password:
            return False, "Please provide username/email and password.", None, None

        # Supabase Integration: attempt cloud login if configured and email is provided
        if supabase_auth_client.is_configured() and "@" in ident and ident != DEFAULT_DEMO_EMAIL:
            sb_ok, sb_msg, sb_token, sb_user = supabase_auth_client.sign_in_with_password(ident, password)
            if sb_ok and sb_token and sb_user:
                # Mirror user in local database to guarantee foreign-key constraints for local tables
                with db_manager.get_session() as session:
                    local_user = session.query(User).filter(
                        (User.user_id == sb_user["user_id"]) | (User.email == sb_user["email"])
                    ).first()
                    if not local_user:
                        local_user = User(
                            user_id=sb_user["user_id"],
                            username=sb_user["username"],
                            email=sb_user["email"],
                            password_hash=hash_password(password),
                            full_name=sb_user["full_name"],
                            is_active=True,
                            created_at=utc_now()
                        )
                        session.add(local_user)
                        session.commit()
                return True, "Login successful via Supabase.", sb_token, sb_user

        with db_manager.get_session() as session:
            user = session.query(User).filter(
                (User.username == ident) | (User.email == ident)
            ).first()

            if not user or not verify_password(password, user.password_hash):
                return False, "Invalid username/email or password.", None, None

            if not user.is_active:
                return False, "This account is inactive. Please contact support.", None, None

            # Generate crypto-secure session token
            token = secrets.token_urlsafe(32)
            user_session = UserSession(
                session_token=token,
                user_id=user.user_id,
                created_at=utc_now(),
                expires_at=utc_now() + timedelta(days=DEFAULT_SESSION_DURATION_DAYS),
                is_revoked=False
            )
            session.add(user_session)
            session.commit()

            user_dict = {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
            return True, "Login successful.", token, user_dict

    @classmethod
    def validate_session(cls, token: Optional[str]) -> Optional[Dict[str, Any]]:
        """
        Validates a session token and returns the authenticated user info if valid and active.
        """
        if not token or not str(token).strip():
            return None

        clean_token = str(token).strip()

        # Check Supabase session if configured
        if supabase_auth_client.is_configured():
            sb_user = supabase_auth_client.get_user(clean_token)
            if sb_user:
                return sb_user

        with db_manager.get_session() as session:
            user_session = session.query(UserSession).filter(
                UserSession.session_token == clean_token,
                UserSession.is_revoked.is_(False),
                UserSession.expires_at > utc_now()
            ).first()

            if not user_session or not user_session.user or not user_session.user.is_active:
                return None

            user = user_session.user
            return {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "session_token": clean_token
            }

    @classmethod
    def logout(cls, token: Optional[str]) -> bool:
        """Revokes an active session token."""
        if not token:
            return False

        if supabase_auth_client.is_configured():
            supabase_auth_client.sign_out(token)

        with db_manager.get_session() as session:
            sess = session.query(UserSession).filter(
                UserSession.session_token == str(token).strip()
            ).first()
            if sess:
                sess.is_revoked = True
                session.commit()
                return True
        return False

    @classmethod
    def get_active_user(cls) -> Optional[Dict[str, Any]]:
        """
        Retrieves the authenticated user from Streamlit session_state.
        Returns None if the user is an unauthenticated visitor.
        """
        try:
            import streamlit as st
            if hasattr(st, "session_state"):
                u = st.session_state.get("auth_user")
                if u and isinstance(u, dict) and u.get("user_id"):
                    return u

                token = st.session_state.get("auth_token") or st.session_state.get("auth_session_token")
                if token:
                    user = cls.validate_session(token)
                    if user:
                        st.session_state["auth_user"] = user
                        st.session_state["auth_token"] = token
                        return user
        except Exception as e:
            logger.debug(f"Auth resolution check: {e}")
        return None

    @classmethod
    def get_or_create_streamlit_user(cls, allow_demo_fallback: bool = False) -> Optional[Dict[str, Any]]:
        """
        Retrieves the authenticated user.
        If allow_demo_fallback=True (used in automated tests), falls back to seeded demo analyst.
        Otherwise returns None so users must explicitly sign in to unlock 3 daily questions.
        """
        active = cls.get_active_user()
        if active:
            return active

        if allow_demo_fallback:
            cls.ensure_default_demo_user()
            ok, msg, new_tok, user_dict = cls.login_user(DEFAULT_DEMO_USERNAME, DEFAULT_DEMO_PASSWORD)
            if ok and user_dict:
                try:
                    import streamlit as st
                    if hasattr(st, "session_state"):
                        st.session_state["auth_token"] = new_tok
                        st.session_state["auth_user"] = user_dict
                except Exception:
                    pass
                return user_dict

        return None

    @classmethod
    def save_supabase_credentials(
        cls,
        supabase_url: str,
        supabase_key: str,
        service_role_key: str = ""
    ) -> Tuple[bool, str]:
        """
        Saves Supabase project credentials to environment variables and .env file.
        Enables immediate cloud user sync without restarting the server.
        """
        clean_url = (supabase_url or "").strip().rstrip("/")
        clean_key = (supabase_key or "").strip()
        clean_srv = (service_role_key or "").strip()

        if not clean_url or not clean_url.startswith("http"):
            return False, "Please provide a valid Supabase project URL (e.g. https://xxxx.supabase.co)."
        if not clean_key or len(clean_key) < 10:
            return False, "Please provide a valid Supabase anon public API key."

        # Set in-memory environment variables
        os.environ["SUPABASE_URL"] = clean_url
        os.environ["SUPABASE_KEY"] = clean_key
        if clean_srv:
            os.environ["SUPABASE_SERVICE_ROLE_KEY"] = clean_srv

        # Update singleton client
        supabase_auth_client._custom_url = clean_url
        supabase_auth_client._custom_key = clean_key
        if clean_srv:
            supabase_auth_client._custom_service_key = clean_srv

        # Persist to .env file
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        try:
            content = ""
            if os.path.exists(env_file):
                with open(env_file, "r", encoding="utf-8") as f:
                    content = f.read()

            import re
            if "SUPABASE_URL=" in content:
                content = re.sub(r'SUPABASE_URL=.*', f'SUPABASE_URL="{clean_url}"', content)
            else:
                content += f'\nSUPABASE_URL="{clean_url}"'

            if "SUPABASE_KEY=" in content:
                content = re.sub(r'SUPABASE_KEY=.*', f'SUPABASE_KEY="{clean_key}"', content)
            else:
                content += f'\nSUPABASE_KEY="{clean_key}"'

            if clean_srv:
                if "SUPABASE_SERVICE_ROLE_KEY=" in content:
                    content = re.sub(r'SUPABASE_SERVICE_ROLE_KEY=.*', f'SUPABASE_SERVICE_ROLE_KEY="{clean_srv}"', content)
                else:
                    content += f'\nSUPABASE_SERVICE_ROLE_KEY="{clean_srv}"'

            with open(env_file, "w", encoding="utf-8") as f:
                f.write(content.strip() + "\n")

            logger.info("Successfully persisted Supabase credentials to .env")
            return True, "Supabase credentials connected and saved successfully!"
        except Exception as e:
            logger.error(f"Failed to persist Supabase credentials to .env: {e}")
            return True, "Supabase credentials connected for active session (could not write to .env)."
