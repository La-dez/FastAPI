from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict
from pydantic import BaseModel
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

users = [
    {'id': 1, 'name': 'John', 'age': 34},
    {'id': 2, 'name': 'Alex', 'age': 12},
    {'id': 3, 'name': 'Bob', 'age': 45},
]

posts = [
    {'id': 1, 'title': 'News 1', 'body':'Text 1', 'author': users[0]},
    {'id': 2, 'title': 'News 2', 'body':'Text 2', 'author': users[1]},
    {'id': 3, 'title': 'News 3', 'body':'Text 3', 'author': users[2]},
]
post_id_generator = count(start=4)
#then
# @app.get("/items")
# async def get_items() -> List[Post]:
#     post_objects = []
#     for post in posts:
#         post_objects.append(Post(id=post['id'], title=post['title'], body=post['body']))
#     return post_objects
#now
print('Hello')
@app.get("/items")
async def get_items() -> List[Post]:
    return [Post(**post) for post in posts] #распаковка. Почитать подробнее #хороший метод, но если хотя бы у одного объекта не совпадет формат, то internal server error

@app.get("/items/{post_id}") #with dynamic parameter
async def get_item(post_id: int) -> Post:
    for el in posts:
        if el['id'] == post_id:
            return Post(**el)
    raise HTTPException(status_code = 404, detail = "Post not found")

@app.get("/search")
async def search(post_id: Optional[int] = None) -> Dict[str, Optional[Post]]:
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