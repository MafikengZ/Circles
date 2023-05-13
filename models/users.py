import uuid

from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext

from datetime import datetime, timedelta


UUID = uuid
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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