from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import os
from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo Manager", version="2.0.0")

ENVIRONMENT = os.getenv("ENVIRONMENT", "unknown")
APP_VERSION = os.getenv("APP_VERSION", "2.0.0")
SECRET_KEY = os.getenv("SECRET_KEY", "not-set")

@app.get("/")
def root():
    return {
        "message": "Todo Manager API",
        "status": "ok",
        "environment": ENVIRONMENT
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/info")
def info():
    return {
        "app": "todo-manager",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "secret_configured": SECRET_KEY != "not-set"
    }

@app.get("/todos", response_model=list[schemas.TodoResponse])
def get_todos(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    return crud.get_todos(db, skip=skip, limit=limit, completed=completed)

@app.get("/todos/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo non trovato")
    return todo

@app.post("/todos", response_model=schemas.TodoResponse, status_code=201)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

@app.put("/todos/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    updated = crud.update_todo(db, todo_id, todo)
    if updated is None:
        raise HTTPException(status_code=404, detail="Todo non trovato")
    return updated

@app.delete("/todos/{todo_id}", response_model=schemas.TodoResponse)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_todo(db, todo_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Todo non trovato")
    return deleted
