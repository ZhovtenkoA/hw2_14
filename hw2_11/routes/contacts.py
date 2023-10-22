from typing import List

from fastapi_limiter.depends import RateLimiter
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from hw2_11.db.db import get_db
from hw2_11.db.models import User
from hw2_11.schemas import ResponseContact
from hw2_11.repository import contacts as repository_contacts
from hw2_11.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.post("/", response_model=ResponseContact, status_code=status.HTTP_201_CREATED,
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])

async def create_new_contact(body: ResponseContact, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, current_user, db)


@router.get("/all", response_model=List[ResponseContact], status_code=status.HTTP_200_OK,
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])

async def read_all_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ResponseContact, 
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])

async def read_contact_by_id(contact_id: int, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ResponseContact, 
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])

async def update_contact(body: ResponseContact, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/remove/{contact_id}", response_model=ResponseContact,
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])

async def remove_user(contact_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/find/{query}", response_model=List[ResponseContact], 
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])

async def find_contacts(query: str, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.search_contacts(query, current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts


@router.get("/birthday/{days}", response_model=List[ResponseContact],
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])

async def contacts_birthday(days: int, db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_upcoming_birthdays(days, current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts