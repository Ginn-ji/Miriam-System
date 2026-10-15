from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Union, Literal, Dict, Any
import uuid
from datetime import datetime, timezone

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str 
    password: str
    role: str = "user"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class LoginRequest(BaseModel):
    login_type: str
    identifier: str
    password: str


class RoleUpdateRequest(BaseModel):
    requester_id: str
    new_role: str


class ForgotPasswordRequest(BaseModel):
    email: str 


class VerifyCodeRequest(BaseModel):
    email: str
    code: str


class ResetPasswordRequest(BaseModel):
    email: str
    code: str
    new_password: str


class VerifyRegistrationRequest(BaseModel):
    email: str
    code: str


# ─────────────────────────────────────────────────────────────
# CHAT & FEEDBACK SCHEMAS
# ─────────────────────────────────────────────────────────────

class ChatResponse(BaseModel):
    message_id: str
    response: str
    session_id: str
    translated_query: str
    laws: Optional[List[Dict[str, Any]]] = []
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class FeedbackRequest(BaseModel):
    message_id: str
    feedback: Literal["like", "dislike"]
    user_id: Optional[str] = None


class FeedbackHistoryItem(BaseModel):
    message_id: str
    user_message: str
    translated_query: Optional[str] = None
    feedback: str
    created_at: str


class LatestFeedbackResponse(BaseModel):
    liked: List[FeedbackHistoryItem]
    disliked: List[FeedbackHistoryItem]


# ─────────────────────────────────────────────────────────────
# KNOWLEDGE BASE & SYSTEM SETTINGS
# ─────────────────────────────────────────────────────────────

class LegalKnowledge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    article: Optional[str] = None
    title: str
    category: str = "Book I"
    simplified_text: Optional[str] = None 
    chunks: Optional[Union[List[str], str]] = None
    content: Optional[str] = None 
    tags: Union[List[str], str]
    language: str = "en"
    created_at: Optional[str] = None


class ChatLimitRequest(BaseModel):
    new_limit: int


class SavedTestCase(BaseModel):
    test_id: str
    query: str
    expected_article: str


class BulkDeleteRequest(BaseModel):
    ids: List[str]