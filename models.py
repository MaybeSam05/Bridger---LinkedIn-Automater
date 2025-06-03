from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "bridger"}

    email = Column(String, primary_key=True, index=True)
    linkedin_cookies = Column(JSON)
    gmail_token = Column(JSON)
    gmail_token_expiry = Column(DateTime)
    gmail_refresh_token = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)

    profiles = relationship("Profile", back_populates="user")
    emails = relationship("Email", back_populates="user")
    sessions = relationship("Session", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"
    __table_args__ = {"schema": "bridger"}

    profile_id = Column(Integer, primary_key=True, index=True)
    linkedin_url = Column(String, index=True)
    raw_ocr_text = Column(Text)
    cleaned_text = Column(Text)
    last_scraped = Column(DateTime, server_default=func.now())
    is_user_profile = Column(Boolean, default=False)
    user_email = Column(String, ForeignKey("bridger.users.email", ondelete="CASCADE"))

    user = relationship("User", back_populates="profiles")
    emails = relationship("Email", back_populates="target_profile")

class Email(Base):
    __tablename__ = "emails"
    __table_args__ = {"schema": "bridger"}

    email_id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, ForeignKey("bridger.users.email", ondelete="CASCADE"))
    target_profile_id = Column(Integer, ForeignKey("bridger.profiles.profile_id", ondelete="SET NULL"))
    email_address = Column(String)
    subject = Column(String)
    body = Column(Text)
    sent_at = Column(DateTime, server_default=func.now())
    status = Column(String)

    user = relationship("User", back_populates="emails")
    target_profile = relationship("Profile", back_populates="emails")

class Session(Base):
    __tablename__ = "sessions"
    __table_args__ = {"schema": "bridger"}

    session_id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, ForeignKey("bridger.users.email", ondelete="CASCADE"))
    started_at = Column(DateTime, server_default=func.now())
    last_active = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="sessions") 