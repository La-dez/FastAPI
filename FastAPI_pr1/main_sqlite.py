from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from typing import Optional, List, Dict, Annotated
from itertools import count
from sqlalchemy.orm import Session

from models import Base, UserDTO, PostDTO
from database import engine, session_local
from schemas import UserCreate, PostCreate, User, Post

app = FastAPI()

Base.metadata.create_all(bind = engine)

def get_db(): #функция, выполняющая подключение к БД
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=User)                                    #response_model - указывает, что мы ожидаем получить в ответе
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserDTO: #Depends - позволяет использовать функцию get_db в качестве зависимости
    db_user = UserDTO(name = user.name, age = user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/posts/", response_model=Post)                                    #response_model - указывает, что мы ожидаем получить в ответе
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> PostDTO: #Depends - позволяет использовать функцию get_db в качестве зависимости
    db_user = db.query(UserDTO).filter(UserDTO.id == post.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_post = PostDTO(title = post.title, body = post.body, author_id = post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/", response_model=List[Post])
async def posts(db: Session = Depends(get_db)):
    return db.query(PostDTO).all()