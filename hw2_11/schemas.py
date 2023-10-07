from datetime import datetime, date
from pydantic import BaseModel


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    additional_data: str = None


class ContactResponse(ContactBase):
    id: int = 1
    first_name: str = "John"
    last_name: str = "Snow"
    email: str = "example@mail.com"
    phone_number: str = "0635555555"
    birthday: date = date(year=1999, month=10, day=5)
    additional_data: str = "Cats lover"

    class Config:
        orm_mode = True
