from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas

# Creates tasks table in todo.db automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ─── Database Session ─────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ─── GET all tasks ────────────────────────────────
@app.get("/todo", response_model=list[schemas.TaskResponse])
def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

# ─── GET one task ─────────────────────────────────
@app.get("/todo/{todo_id}", response_model=schemas.TaskResponse)
def get_task(todo_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == todo_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Todo not found")
    return task

# ─── POST add a task ──────────────────────────────
@app.post("/todo", status_code=201, response_model=schemas.TaskResponse)
def add_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# ─── PUT update a task ────────────────────────────
@app.put("/todo/{todo_id}", response_model=schemas.TaskResponse)
def update_task(todo_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Task).filter(models.Task.id == todo_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Todo not found")
    existing.title       = task.title
    existing.description = task.description
    existing.completed   = task.completed
    db.commit()
    db.refresh(existing)
    return existing

# ─── DELETE a task ────────────────────────────────
@app.delete("/todo/{todo_id}")
def delete_task(todo_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == todo_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(task)
    db.commit()
    return {"message": "Todo deleted!"}