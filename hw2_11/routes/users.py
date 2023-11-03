from fastapi import APIRouter, HTTPException, Depends, status, Security, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
import cloudinary
import cloudinary.uploader

from sqlalchemy.orm import Session

from hw2_11.db.db import get_db
from hw2_11.db.models import User
from hw2_11.schemas import UserModel, ResponseUser, TokenModel, UserDb
from hw2_11.repository import users as repository_users
from hw2_11.services.auth import auth_service
from hw2_11.conf.config import settings

router = APIRouter(prefix='/users', tags=['users'])

@router.get("/me", response_model=UserDb)
async def read_user_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    read_user_me returns the currently authenticated user.

    It uses the auth_service.get_current_user dependency to retrieve the 
    User object for the authenticated request. This function can be used
    in other routes to get the current user data.
    """
    return current_user

@router.patch("/me", response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_avatar_user function updates the avatar of a user.
        Args:
            file (UploadFile): The file to be uploaded.
            db (Session, optional): [description]. Defaults to Depends(get_db).
            current_user (User, optional): [description]. Defaults to Depends(auth_service.get_current_user).
        
        Returns:
    
    :param file: UploadFile: Get the file that is being uploaded
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user information
    :return: A user object
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    public_id = f"Contacts_app/{current_user.username}{current_user.id}"
    r = cloudinary.uploader.upload(file.file, public_id=public_id, owerwrite=True)
    avatar_url = cloudinary.CloudinaryImage(public_id).build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, avatar_url, db)
    
    return user