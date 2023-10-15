from pydantic import BaseModel, EmailStr, validator
import re
import datetime

import fast_todo.utils.password as password_utils

class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str
    password: str

    @validator('name')
    def name_alphanumeric(cls, v: str):
        if v.isalpha() == False or len(v) > 15 or len(v) < 4:
            raise ValueError('the name should contain only alphanumeric characters and be less than 15 characters and at least 4 characters')
        return v
    
    @validator('password')
    def password_complexity(cls, v):
        if password_utils.is_password_complex(v) == False:
            raise ValueError('the password should be at least 12 characters with lowercase, uppercase and numeric characters')
        return v

class LoginRequest(BaseModel):
    email: str
    password: str

class UserRecord(BaseModel):
    id: int
    email: str
    name: str
    hashed_password: str
    created_at: datetime.datetime

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

class LoginResponse(BaseModel):
    access_token: str