from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from config import settings


class Token(BaseModel):
    access_token: str
    refresh_token: str


class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    image: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

    @field_validator("image", mode="before")
    def create_image_url(cls, value: Optional[object]) -> Optional[str]:
        return f"http://{settings.run.host}:{settings.run.port}/static/media/{value}"


class UserShort(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    image: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

    @field_validator("image", mode="before")
    def create_image_url(cls, value: Optional[object]) -> Optional[str]:
        return f"http://{settings.run.host}:{settings.run.port}/static/media/{value}"


class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
