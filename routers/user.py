from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from user_jwt import create_token

login_user = APIRouter()

class User(BaseModel):
    email: str
    password: str



@login_user.post('/login', tags=["Authentication"])
def login(user: User):
    if user.email == 'ejemplo@mail.com' and user.password == '123456':
        token: str = create_token(user.dict())
        print(token)
        return JSONResponse(content={"message": "User authenticated", "token": token}, status_code=200)
    return JSONResponse(content=(message := {"message": "User not authenticated"}), status_code=401)