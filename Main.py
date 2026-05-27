from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Lesson 1 - Hello
@app.get("/hello")
def say_hello():
    return {"message": "Hello, World!"}

# Lesson 2 - Path params
@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {"id": product_id, "name": "Laptop", "price": 999.99}

@app.get("/greet/{name}")
def greet_user(name: str):
    return {"message": f"Hello, {name}!"}

# Lesson 3 - Query params
@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/search")
def search_items(q: Optional[str] = None):
    if q:
        return {"results": f"You searched for: {q}"}
    return {"results": "Showing everything"}

@app.get("/users/{user_id}/orders")
def get_user_orders(user_id: int, limit: int = 5):
    return {
        "user_id": user_id,
        "limit": limit,
        "orders": ["order1", "order2"]
    }

# Lesson 4 - Request Body
class User(BaseModel):
    name: str
    age: int
    email: str

class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    in_stock: bool = True

@app.post("/users")
def create_user(user: User):
    return {"message": "User created successfully!", "user": user}

@app.post("/products")
def create_product(product: Product):
    return {"message": "Product added!", "data": product}