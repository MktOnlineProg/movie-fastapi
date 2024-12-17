from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from user_jwt import create_token, validateToken
from bd.database import  engine, Base
from routers.movie import routerMovie
from routers.user import login_user

app1 = FastAPI(
    title="My First FastAPI",
    description="This is my first FastAPI",
    version="0.0.1"
)

app1.include_router(routerMovie)

app1.include_router(login_user)

Base.metadata.create_all(bind=engine)

"""
class User(BaseModel):
    email: str
    password: str
"""


"""
movies = [
    {
        'id': 1,
        'title': 'The Shawshank Redemption',
        'overview': "Framed in the 1940s for the",
        'year': '1994',
        'rating': 9.3,
        'category': 'Drama'
    },
    {
        'id': 2,
        'title': 'The Shawshank Redemption',
        'overview': "Framed in the 1940s for the",
        'year': '1994',
        'rating': 9.3,
        'category': 'Drama'
    },
    {
        'id': 3,
        'title': 'The Shawshank Redemption',
        'overview': "Framed in the 1940s for the",
        'year': '1994',
        'rating': 9.3,
        'category': 'Drama'
    },
]
""" 

"""
@app1.post('/login', tags=["Authentication"])
def login(user: User):
    if user.email == 'ejemplo@mail.com' and user.password == '123456':
        token: str = create_token(user.dict())
        print(token)
        return JSONResponse(content={"message": "User authenticated", "token": token}, status_code=200)
    return JSONResponse(content=(message := {"message": "User not authenticated"}), status_code=401)

"""

@app1.get('/', tags=["Inicio"])
def read_root():
    return HTMLResponse(content="<h1>Welcome to my first FastAPI</h1>", status_code=200)
