import asyncio
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn

from models.users import *
from utility.exceptions import *
from schema.db import *

app = FastAPI()


class Token(BaseModel):
    access_token: str
    token_type: str


class Oauth2Password(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not isinstance(value, Annotated[OAuth2PasswordRequestForm, Depends()]):
            raise ValueError("Invalid OAuth2PasswordRequestForm")
        return value

class ActiveUsers(BaseModel):
    form_data: Oauth2Password
    current_user: Annotated[User, Depends(get_current_active_user)]

    class Config:
        arbitrary_types_allowed = True
        response_model_exclude_none = True
        

@app.post("/token", response_model=Token)
async def login_for_access_token(user: ActiveUsers):
    """Create a timedelta with the expiration time of the token.
        Create a real JWT access token and return it
    """

    auth_user = authenticate_user(db, user.username, user.password)
    if not auth_user:
        raise credentials_invalid
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": auth_user.username},
                                       expires_delta=access_token_expires
                                       )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/", response_model=User)
async def get_users(user: User):
    return user


@app.get("/users/items/")
async def get_user_items(user: User):
    return [{"item_id": "Foo", "owner": user.username}]


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1",
                port=8080, log_level="info", reload=True,)
