from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_data: str = None



class ContactResponse(ContactBase):
    id: int = 1
    first_name: str = "John"
    last_name: str = "Snow"
    email: EmailStr = "example@mail.com"
    phone_number: str = "0635555555"
    birthday: date = date(year=1999, month=10, day=5)
    additional_data: str = "Cats lover"

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
