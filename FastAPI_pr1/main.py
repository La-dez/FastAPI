from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()

@app.get("/")
async def home() -> dict[str,str]: #так указывается тип возращаемого значения
    return {"data":"message"}

@app.get("/contacts")
async def contacts() -> int:
    return 34

posts = [
    {'id': 1, 'title': 'News 1', 'body':'Text 1'},
    {'id': 2, 'title': 'News 2', 'body':'Text 2'},
    {'id': 3, 'title': 'News 3', 'body':'Text 3'},
]

@app.get("/items")
async def get_items() -> list:
    return posts

@app.get("/items/{post_id}") #with dynamic parameter
async def get_item(post_id: int) -> dict:
    for el in posts:
        if el['id'] == post_id:
            return el
    raise HTTPException(status_code = 404, detail = "Post not found")

@app.get("/search")
async def search(post_id: Optional[int] = None) -> dict:
    if post_id:
        for el in posts:
            if el['id'] == post_id:
                return el
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return {"data": "No post ID provided"}

#