from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

from models.users import User

app =FastAPI()

class UserRegistration(BaseModel):
    user : User
    
    
    @app()

if __name__ == "__main__":
    uvicorn.run(app:'main',
        host:str="127.0.0.1" ,
        port: int=8080 ,
        reload:bool=False,
        log_level:str="debug", debug:bool=True)
    