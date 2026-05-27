from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    title:  str
    author: str
    price:  float

books_db = {
    1: {"title": "Python Crash Course", "author": "Eric Matthes", "price": 29.99},
    2: {"title": "Clean Code",          "author": "Robert Martin", "price": 34.99},
}

@app.get("/books")
def get_all_books():
    return books_db

@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    return books_db[book_id]

@app.post("/books", status_code=201)
def add_book(book: Book):
    new_id = len(books_db) + 1
    books_db[new_id] = book.dict()
    return {"message": "Book added!", "id": new_id, "book": book}

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    books_db[book_id] = book.dict()
    return {"message": "Book updated!", "book": book}

@app.delete("/books/{book_id}", status_code=200)
def delete_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    deleted = books_db.pop(book_id)
    return {"message": "Book deleted!", "deleted": deleted}
