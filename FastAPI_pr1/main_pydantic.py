from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict
from pydantic import BaseModel

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


# @app.get("/items")
# async def get_items() -> List[Post]:
#     post_objects = []
#     for post in posts:
#         post_objects.append(Post(id=post['id'], title=post['title'], body=post['body']))
#     return post_objects

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



#