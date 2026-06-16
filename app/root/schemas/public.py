from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class TenantBase(BaseModel):
    company_name: str
    company_size: Optional[int] = None
    company_description: Optional[str] = None
    address: Optional[str] = None
    schema_name: str

class TenantCreate(TenantBase):
    pass

class Tenant(TenantBase):
    id: UUID
    subscription_status: str
    created_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
