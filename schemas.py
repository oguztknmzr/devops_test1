from typing import Optional
from pydantic import BaseModel


class AuthorCreate(BaseModel):
    name: str
    country: Optional[str] = None


class Author(AuthorCreate):
    id: int


class BookCreate(BaseModel):
    title: str
    year: Optional[int] = None
    author_id: int


class Book(BookCreate):
    id: int
