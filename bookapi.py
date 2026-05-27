from google import genai
import os
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas

# Creates books table in books.db automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# Reads your key securely from environment variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "PASTE_YOUR_GEMINI_KEY_HERE")
ai_client = genai.Client(api_key=GEMINI_API_KEY)


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

# ─── AI Book Summarizer EndPoint ────────────────────────────
@app.get("/books/{book_id}/summarize")
def summarize_book(book_id: int, db: Session = Depends(get_db)):
    # 1. Fetch the book from SQLite database
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # 2. Check if it has a long enough description to summarize
    if not book.description or len(book.description) < 20:
        raise HTTPException(
            status_code=400, 
            detail="The book description is too short to generate an accurate summary."
        )

    try:
        # 3. Create a strict instruction prompt for Gemini
        prompt = f"""
        You are a professional literary assistant.
        Provide a crisp, 3-sentence summary of the following book content.
        Do not include introductory words like "Here is your summary". Go straight to the points.

        Book Title: {book.title}
        Book Content: {book.description}
        """

        # 4. Generate the content using Gemini 1.5 Flash
        response = ai_client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
        )

        return {
            "book_id": book.id,
            "title": book.title,
            "summary": response.text.strip()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini LLM Error: {str(e)}")
