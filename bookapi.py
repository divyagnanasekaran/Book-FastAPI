from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas

# Creates books table in books.db automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ─── Database Session ─────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ─── GET all books ────────────────────────────────
@app.get("/books", response_model=list[schemas.BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

# ─── GET one book ─────────────────────────────────
@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# ─── POST add a book ──────────────────────────────
@app.post("/books", status_code=201, response_model=schemas.BookResponse)
def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# ─── PUT update a book ────────────────────────────
@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Book not found")
    existing.title  = book.title
    existing.author = book.author
    existing.price  = book.price
    db.commit()
    db.refresh(existing)
    return existing

# ─── DELETE a book ────────────────────────────────
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted!"}