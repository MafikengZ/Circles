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
    def validate(cls, v):
        if not isinstance(v, Annotated[OAuth2PasswordRequestForm, Depends()]):
            raise ValueError("Not a valid OAuth2PasswordRequestForm")
        return str(v)


class Users(BaseModel):
    form_data: Oauth2Password
    current_user: Annotated[User, Depends(get_current_active_user)]

    class Config:
        arbitrary_types_allowed = True
        response_model_exclude_none = True


@app.post("/token", response_model=Token)
async def login_for_access_token(data: Users):
    """Create a timedelta with the expiration time of the token.
    Create a real JWT access token and return it"""

    user = authenticate_user(db, data.username, data.password)
    if not user:
        raise invalid_credentials
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/", response_model=User)
async def get_users(user: User):
    return user


@app.get("/users/items/")
async def get_user_items(user: User):
    return [{"item_id": "Foo", "owner": user.username}]


async def server():
    config = uvicorn.Config(
        "main:app", host="127.0.0.1", port=5000, log_level="info", reload=True
    )

    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(server())
