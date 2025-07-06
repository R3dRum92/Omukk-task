import datetime
import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class BaseResponse(BaseModel):
    message: str


# Auth schemas
class RegistrationRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    token: str
    verified: bool


class UserUnverified(BaseModel):
    id: uuid.UUID
    name: str


class User(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class VerificationCodeResponse(BaseModel):
    message: str
    verification_code: str
    expires_in: int


# Post schemas
class PostView(BaseModel):
    id: uuid.UUID
    content: str
    author: User
    likes: int
    liked: bool
    time: datetime.datetime


class PostCreate(BaseModel):
    content: str


class PostEdit(BaseModel):
    content: str


class PostAction(BaseModel):
    id: uuid.UUID
