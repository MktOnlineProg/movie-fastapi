from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import create_token, validateToken
from fastapi.security import HTTPBearer
from bd.database import Session, engine, Base
from models.movie import Pelicula
from fastapi.encoders import jsonable_encoder

from fastapi import APIRouter

routerMovie = APIRouter()

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='Titulo de la pelicula',min_length=1, max_length=100)
    overview: str = Field(default='Aqui va la descripcion de la pelicula', min_length=1, max_length=200)
    year: str = Field(default='2021', min_length=1, max_length=4)
    rating: float = Field(default=0.0, ge=0.0, le=10.0)
    category: str = Field(default='Aqui va la categoria', min_length=1, max_length=20)

class Bearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != 'ejemplo@mail.com':
            raise HTTPException(status_code=403, detail="You don't have permission to access")


#Get Movies (todas) Lista
"""
@routerMovie.get('/movies', tags=[" Get Movies"], dependencies=[Depends(Bearer())])
def read_movies():
    return JSONResponse(content=movies, status_code=200)
"""

#Get Movies (todas) BD
@routerMovie.get('/movies', tags=[" Get Movies"], dependencies=[Depends(Bearer())])
def read_movies():
    db = Session()
    data = db.query(Pelicula).all()
    return JSONResponse(content=jsonable_encoder(data), status_code=200)

#Get Movie por ID Lista
"""
@routerMovie.get('/movies/{movie_id}', tags=["Get Movie"])
def read_movie(movie_id: int):
    movie = next((movie for movie in movies if movie['id'] == movie_id), None)
    return movie
"""
#Get Movie por ID Lista
"""
@routerMovie.get('/movies/{movie_id}', tags=["Get Movie"])
def read_movie(movie_id: int = Path(ge=1, le=50)):
    for movie in movies:
        if movie['id'] == movie_id:
            return movie
    return None
"""
#Get Movie por ID BD
@routerMovie.get('/movies/{movie_id}', tags=["Get Movie"])
def read_movie(movie_id: int = Path(ge=1, le=50)):
    db = Session()
    data = db.query(Pelicula).filter(Pelicula.id == movie_id).first()
    if data:
        return JSONResponse(content=jsonable_encoder(data), status_code=200)
    return JSONResponse(content={"message": "Movie not found"}, status_code=404)

#Get Movies por categoria Lista
"""
@routerMovie.get('/movies/', tags=["Movies"])
def get_movies_by_category(category: str = Query(min_length=3, max_length=20)):
    for movie in movies:
        if movie['category'] == category:
            return movie
    return None
"""

#Get Movies por categoria BD
@routerMovie.get('/movies/', tags=["Movies"])
def get_movies_by_category(category: str = Query(min_length=3, max_length=20)):
    db = Session()
    data = db.query(Pelicula).filter(Pelicula.category == category).all()
    return JSONResponse(content=jsonable_encoder(data), status_code=200)


"""
@routerMovie.post('/movies', tags=["Create Movie"])
def create_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(content={"message": "Movie created successfully"}, status_code=201)
"""
#Crear en la base de datos
@routerMovie.post('/movies', tags=["Create Movie"], status_code=201)
def create_movie(movie: Movie):
    db = Session()
    new_movie = Pelicula(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={"message": "Movie created successfully"}, status_code=201)

#Crear en lista
"""
@routerMovie.post('/movies', tags=["Create Movie"])
def create_movie(
    id: int = Body(),
    title: str = Body(),
    overview: str = Body(),
    year: str = Body(),
    rating: float = Body(),
    category: str = Body()
):
    
    movies.append({
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category
    })    
    return title
"""

#Actualizar con una estructura de datos
"""
@routerMovie.put('/movies/{movie_id}', tags=["Update Movie"])
def update_movie(movie_id: int, movie: Movie):
    for item in movies:
        if item["id"] == movie_id:  # Aquí accedes al diccionario
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return movies
    return {"error": "Movie not found"}
"""

#Actualizar en la base de datos
@routerMovie.put('/movies/{movie_id}', tags=["Update Movie"])
def update_movie(movie_id: int, movie: Movie):
    db = Session()
    data = db.query(Pelicula).filter(Pelicula.id == movie_id).first()
    if data:
        data.title = movie.title
        data.overview = movie.overview
        data.year = movie.year
        data.rating = movie.rating
        data.category = movie.category
        db.commit()
        return JSONResponse(content={"message": "Movie updated successfully"}, status_code=200)
    return JSONResponse(content={"message": "Movie not found"}, status_code=404)

#Actualizar con elementos de la lista
"""
@routerMovie.put('/movies/{movie_id}', tags=["Update Movie"])
def update_movie(
    movie_id: int, 
    title: str = Body(...), 
    overview: str = Body(...), 
    year: str = Body(...), 
    rating: float = Body(...), 
    category: str = Body(...),
):
    for movie in movies:
        if movie['id'] == movie_id:
            movie['title'] = title
            movie['overview'] = overview
            movie['year'] = year
            movie['rating'] = rating
            movie['category'] = category
            return movies
    return None
"""

#Eliminar en la lista
"""
@routerMovie.delete('/movies/{movie_id}', tags=["Delete Movie"])
def delete_movie(movie_id: int):
    for movie in movies:
        if movie['id'] == movie_id:
            movies.remove(movie)
            return movies
    return None
"""
    
#Eliminar en la base de datos
@routerMovie.delete('/movies/{movie_id}', tags=["Delete Movie"])
def delete_movie(movie_id: int):
    db = Session()
    data = db.query(Pelicula).filter(Pelicula.id == movie_id).first()
    if data:
        db.delete(data)
        db.commit()
        return JSONResponse(content={"message": "Movie deleted successfully"}, status_code=200)
    return JSONResponse(content={"message": "Movie not found"}, status_code=404)