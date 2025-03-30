from fastapi import FastAPI, HTTPException, Path, Query, Body
from typing import Optional, List, Dict, Annotated
from pydantic import BaseModel, Field
from itertools import count

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    age: int

class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User

class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int

class UserCreate(BaseModel): #annotation demo
    name: Annotated[
        str, Field(...,
                   title='Имя пользователя',
                   min_length=2,
                   max_length=201
                   )
    ]
    age: Annotated[
        str,
        Field(...,title = 'Возраст пользователя', ge=1, le=121)
    ]

users = [
    {'id': 1, 'name': 'John', 'age': 34},
    {'id': 2, 'name': 'Alex', 'age': 12},
    {'id': 3, 'name': 'Bob', 'age': 45},
]
user_id_generator = count(start=max(user['id'] for user in users) + 1)

posts = [
    {'id': 1, 'title': 'News 1', 'body':'Text 1', 'author': users[0]},
    {'id': 2, 'title': 'News 2', 'body':'Text 2', 'author': users[1]},
    {'id': 3, 'title': 'News 3', 'body':'Text 3', 'author': users[2]},
]
post_id_generator = count(start=max(post['id'] for post in posts) + 1)


print('Hello')
@app.get("/items")
async def get_items() -> List[Post]:
    return [Post(**post) for post in posts] #распаковка. Почитать подробнее #хороший метод, но если хотя бы у одного объекта не совпадет формат, то internal server error

@app.get("/items/{post_id}") #with dynamic parameter
async def get_item(post_id: Annotated[int, Path(...,title='Здесь указывается ID поста',ge=1,lt=1000000)] #ge - greater or equal, ... - required, lt - less than
                   ) -> Post:
    for el in posts:
        if el['id'] == post_id:
            return Post(**el)
    raise HTTPException(status_code = 404, detail = "Post not found")

@app.get("/search")
async def search(post_id: Annotated[
    Optional[int],#не path, т.к. параметр не является динамической частью URL, а передается в query string
    Query(title='Id поста для поиска', le = 50000000, gt = 0)
]) -> Dict[str, Optional[Post]]:
    if post_id:
        for el in posts:
            if el['id'] == post_id:
                return {"data": Post(**el)}
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return {"data": None}

@app.post("/items/add")
async def add_item(post: PostCreate) -> Post:
    author = next((user for user in users if user['id'] == post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail = 'User not found')
    new_post_id = next(post_id_generator)
    new_post = { 'id': new_post_id, 'title': post.title, 'body' : post.body, 'author': author}
    posts.append(new_post)
    return Post(**new_post)

@app.post("/user/add")
async def add_user(user: Annotated[
    UserCreate,
    Body(..., example = { #для описания параметра метода в swagger
        'name': 'UserName',
        'age': 34
    })
]) -> User:
    new_post_id = next(user_id_generator)
    new_user = {'id': new_post_id, 'name': user.name, 'age': user.age}
    users.append(new_user)
    return User(**new_user)