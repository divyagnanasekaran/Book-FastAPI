from pydantic import BaseModel

# Used when CREATING a book (client sends this)
class BookCreate(BaseModel):
    title: str
    author: str
    price: float

# Used when RETURNING a book (server sends this)
class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    price: float

    class Config:
        orm_mode = True