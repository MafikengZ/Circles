from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

from models.users import *
from utility.exceptions import *


app =FastAPI()


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    '''Create a timedelta with the expiration time of the token.
        Create a real JWT access token and return it'''
        
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise 
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




if __name__ == "__main__":
    # uvicorn.run(app:'main',
    #     host:str="127.0.0.1" ,
    #     port: int=8080 ,
    #     reload:bool=False,
    #     log_level:str="debug", debug:bool=True)
    pass