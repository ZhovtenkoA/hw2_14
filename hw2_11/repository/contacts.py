from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from hw2_11.db.models import Contact
from hw2_11.schemas import ContactBase


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactBase, db: Session) -> Contact:
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday,
        additional_data=body.additional_data,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(
    contact_id: int, body: ContactBase, db: Session
) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = (body.first_name,)
        contact.last_name = (body.last_name,)
        contact.email = (body.email,)
        contact.phone_number = (body.phone_number,)
        contact.birthday = (body.birthday,)
        contact.additional_data = body.additional_data
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(query: str, db: Session) -> List[Contact]:
    response = []
    search_by_first_name = (
        db.query(Contact).filter(Contact.first_name.like(f"%{query}%")).all()
    )
    if search_by_first_name:
        for i in search_by_first_name:
            response.append(i)
    search_by_last_name = (
        db.query(Contact).filter(Contact.last_name.like(f"%{query}%")).all()
    )
    if search_by_last_name:
        for i in search_by_last_name:
            response.append(i)
    search_by_email = db.query(Contact).filter(Contact.email.like(f"%{query}%")).all()
    if search_by_email:
        for i in search_by_email:
            response.append(i)

    return response


async def get_birthday_per_week(days: int, db: Session) -> Contact:
    response = []
    all_contacts = db.query(Contact).all()
    for contact in all_contacts:
        if (
            timedelta(0)
            <= (
                (contact.birthday.replace(year=int((datetime.now()).year)))
                - datetime.now().date()
            )
            <= timedelta(days)
        ):
            response.append(contact)

    return response
