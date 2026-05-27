from pydantic import BaseModel

# ─── Task Schemas ─────────────────────────────────
# Used when CREATING a task
class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False

# Used when RETURNING a task
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    class Config:
        orm_mode = True

# ─── User Schemas ─────────────────────────────────
# Used when REGISTERING a user
class UserCreate(BaseModel):
    username: str
    password: str

# Used when RETURNING a user
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

# Used when RETURNING a token after login
class Token(BaseModel):
    access_token: str
    token_type: str