from bd.database import Base
from sqlalchemy import Column, Integer, String, Date, Float

class Pelicula(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)

