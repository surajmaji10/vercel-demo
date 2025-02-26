"""
@author: Akash Maji
@email: akashmaji@iisc.ac.in
"""

import os
# for setting and getting env variables for db params
from dotenv import load_dotenv
loaded = load_dotenv()
from urllib.parse import quote_plus

from sqlalchemy import create_engine, MetaData

# print(os.getenv("FOO"))
# print(os.getenv("BAR"))
# print(os.getenv("AKASH"))

# DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASS = os.getenv("DATABASE_PASS")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

DATABASE_URL = "mysql+pymysql://root:%s@localhost:3306/testdb"%quote_plus(DATABASE_PASS)
print(DATABASE_URL)

# create engine
engine = create_engine(DATABASE_URL)

# create metadata
metadata = MetaData()

# create session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# create base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from models import TodoModel

# create tables
TodoModel.metadata.create_all(engine)

# create a new todo

from pydantic import BaseModel
from typing import Optional

from fastapi import FastAPI
app = FastAPI()

class ToDoRequest(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    done: bool = False

class ToDoResponse(ToDoRequest):
    class Config:
        orm_mode = True


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/todos")
async def get_todos():
    todos = session.query(TodoModel).all()
    return todos

@app.get("/todos/{todo_id}")
async def get_todo_by_id(todo_id: int):
    todo = session.query(TodoModel).filter(TodoModel.id == todo_id).first()
    return todo

@app.post("/todos/{todo_id}", response_model=ToDoResponse)
async def create_todo(todo_id: int, todo: ToDoRequest):
    new_todo = TodoModel(id=todo_id, title=todo.title, description=todo.description, done=todo.done)
    session.add(new_todo)
    session.commit()
    return new_todo

@app.put("/todos/{todo_id}", response_model=ToDoResponse)
async def update_todo_by_id(todo_id: int, todo: ToDoRequest):
    todo_to_update = session.query(TodoModel).filter(TodoModel.id == todo_id).first()
    todo_to_update.title = todo.title
    todo_to_update.description = todo.description
    todo_to_update.done = todo.done
    session.commit()
    return todo_to_update

@app.delete("/todos/{todo_id}")
async def delete_todo_by_id(todo_id: int):
    todo_to_delete = session.query(TodoModel).filter(TodoModel.id == todo_id).first()
    session.delete(todo_to_delete)
    session.commit()
    return {"message": "Todo deleted successfully"}


# curl -X 'POST' \
#   'http://localhost:8000/todos/3' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#     "id": 3,
#     "title": "Buy Milk",
#     "description": "Buy 2 litres of milk",
#     "done": false
#     }'

# curl -X 'PUT' \
#   'http://localhost:8000/todos/3' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#     "id": 3,
#     "title": "Buy Milk",
#     "description": "Buy 100 litres of milk",
#     "done": true
#     }'

# curl -X 'DELETE' \
#   'http://localhost:8000/todos/3'


# @app.post("/todos")
# async def create_todo(todo: ToDo):
#     new_todo = TodoModel(title=todo.title, description=todo.description, done=todo.done)
#     session.add(new_todo)
#     session.commit()
#     return new_todo








