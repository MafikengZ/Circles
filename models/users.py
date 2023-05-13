import uuid

from pydantic import BaseModel
from typing import Optional , Annotated, Required

from jose import JWTError, jwt
from passlib.context import CryptContext

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta

from utility.exceptions import *



UUID = uuid
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "d556c6142436e109b7ca0e6e77414a635cdf52249c14395342ddf683e6eb43f0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

db = {
    "AyraStark": {
        "username": "Ayra",
        "full_name": "Ayra Stark",
        "email": "ayra.stark@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class User(BaseModel):
    employee_id = UUID.uuid1()
    username: str
    password: str 
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    
class UserInDB(User):
    hashed_password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None

async def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
#Hash and verify the passwords
async def get_password_hash(password:str):
    '''Create a utility function to hash a password coming from the user'''
    return pwd_context.hash(password)

async def verify_password(password:str , hash_passport:str):
    '''Verify if a received password matches the hash stored.'''
    return pwd_context.verify(password , hash_passport)

#Get user and authenticate
async def authenticate_user(db , username:str , password:str):
    '''authenticate and return a user.'''
    user = get_user(db , username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    '''Create a utility function to generate a new access token'''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    '''Update get_current_user to receive the same token as before, but this time,using JWT tokens.
        Decode the received token, verify it, and return the current user.
        If the token is invalid, return an HTTP error right away.'''
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user