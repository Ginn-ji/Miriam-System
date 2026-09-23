from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Union
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

class ChatResponse(BaseModel):
    response: str
    session_id: str
    laws: Optional[List[dict]] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class LegalKnowledge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    article: Optional[str] = None
    title: str
    category: str = "Labor Law"
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

class VerifyRegistrationRequest(BaseModel):
    email: str
    code: str