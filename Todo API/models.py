from sqlalchemy import Column, Integer, String, Boolean
from database import Base

# Task table — same as before
class Task(Base):
    __tablename__ = "tasks"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String)
    description = Column(String)
    completed   = Column(Boolean, default=False)

# User table — new!
class User(Base):
    __tablename__ = "users"

    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)