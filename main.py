from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import os

# --- Database connection ---
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://todo:todo_password@db:5432/todo",
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# --- The database table, described as a Python class ---
class TodoDB(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    done = Column(Boolean, default=False)


# Create the table if it doesn't exist yet.
Base.metadata.create_all(bind=engine)


# --- What the API accepts and returns ---
class TodoIn(BaseModel):
    title: str
    done: bool = False


class Todo(TodoIn):
    id: int
    model_config = {"from_attributes": True}


app = FastAPI(title="DevOps Todo API")


# Give each request its own database session, then close it.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/todos", response_model=list[Todo])
def list_todos(db: Session = Depends(get_db)):
    return db.query(TodoDB).all()


@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: TodoIn, db: Session = Depends(get_db)):
    item = TodoDB(title=todo.title, done=todo.done)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    item = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return item


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    item = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(item)
    db.commit()
    return None
