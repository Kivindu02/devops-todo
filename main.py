from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="DevOps Todo API")

# Config comes from the environment, not hardcoded — the start of "12-factor" thinking.
APP_ENV = os.getenv("APP_ENV", "development")

# In-memory store for now. We swap this for a real Postgres database at the container layer.
todos = {}
next_id = 1


class TodoIn(BaseModel):
    title: str
    done: bool = False


class Todo(TodoIn):
    id: int


@app.get("/health")
def health():
    # CI/CD and Kubernetes use this endpoint to ask "is the app alive?"
    return {"status": "ok", "env": APP_ENV}


@app.get("/todos")
def list_todos():
    return list(todos.values())


@app.post("/todos", status_code=201)
def create_todo(todo: TodoIn):
    global next_id
    item = Todo(id=next_id, **todo.model_dump())
    todos[next_id] = item
    next_id += 1
    return item


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
    return None
