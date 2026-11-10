from fastapi import FastAPI, HTTPException, status
from psycopg2.errors import ForeignKeyViolation
import db
from schemas import Author, AuthorCreate, Book, BookCreate

app = FastAPI()


@app.get("/authors", response_model=list[Author])
def list_authors():
    return db.get_authors()


@app.get("/authors/{author_id}", response_model=Author)
def read_author(author_id: int):
    author = db.get_author(author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors", response_model=Author, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorCreate):
    return db.add_author(author.name, author.country)


@app.put("/authors/{author_id}", response_model=Author)
def edit_author(author_id: int, author: AuthorCreate):
    updated = db.update_author(author_id, author.name, author.country)
    if updated is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return updated


@app.delete("/authors/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_author(author_id: int):
    deleted = db.delete_author(author_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Author not found")


@app.get("/books", response_model=list[Book])
def list_books():
    return db.get_books()


@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int):
    book = db.get_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    try:
        return db.add_book(book.title, book.year, book.author_id)
    except ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Author does not exist")


@app.put("/books/{book_id}", response_model=Book)
def edit_book(book_id: int, book: BookCreate):
    try:
        updated = db.update_book(book_id, book.title, book.year, book.author_id)
    except ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Author does not exist")
    if updated is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_book(book_id: int):
    deleted = db.delete_book(book_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Book not found")
