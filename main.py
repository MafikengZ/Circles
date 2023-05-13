import asyncio
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

from models.users import *
from utility.exceptions import *


app = FastAPI()


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Create a timedelta with the expiration time of the token.
    Create a real JWT access token and return it"""

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise invalid_credentials
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/", response_model=User)
async def get_users(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@app.get("/users/items/")
async def get_user_items(current_user: Annotated[User, Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]


async def server():
    config = uvicorn.Config("main:app",
                            host="127.0.0.1", 
                            port=5000, 
                            log_level="info",
                            reload=True)
    
    server = uvicorn.Server(config)
    await server.serve()
    
if __name__ == "__main__":
  asyncio.run(server())