from pydantic import BaseModel
from typing import Optional

# Used when CREATING a book (client sends this)
class BookCreate(BaseModel):
    title: str
    author: str
    price: float
    # ─── ADD THIS LINE ────────────────────────────────
    description: Optional[str] = None

# Used when RETURNING a book (server sends this)
class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    price: float
    # ─── ADD THIS LINE ────────────────────────────────
    description: Optional[str] = None
    
    class Config:
        # FastAPI uses this to convert SQLAlchemy models to JSON automatically
        orm_mode = True
