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
    def get_or_create_streamlit_user(cls) -> Dict[str, Any]:
        """
        Retrieves the authenticated user from Streamlit session_state.
        If no session token is stored, automatically initializes the session
        with the default seeded demo analyst account so immediate functionality is guaranteed.
        """
        try:
            import streamlit as st
            if hasattr(st, "session_state"):
                token = st.session_state.get("auth_session_token")
                user = cls.validate_session(token)
                if user:
                    return user

                # If no valid token, authenticate as default demo analyst
                cls.ensure_default_demo_user()
                ok, msg, new_tok, user_dict = cls.login_user(DEFAULT_DEMO_USERNAME, DEFAULT_DEMO_PASSWORD)
                if ok and new_tok:
                    st.session_state["auth_session_token"] = new_tok
                    st.session_state["auth_user"] = user_dict
                    return user_dict
        except Exception as e:
            logger.debug(f"Streamlit auth resolution notice: {e}")

        # Fallback to direct DB demo user
        demo = cls.ensure_default_demo_user()
        return {
            "user_id": demo.user_id,
            "username": demo.username,
            "email": demo.email,
            "full_name": demo.full_name
        }
