from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()

print("✅ debug_app.py исполняется")
print("👀 Регистрируем /search")

posts = [
    {'id': 1, 'title': 'News 1', 'body': 'Text 1'},
    {'id': 2, 'title': 'News 2', 'body': 'Text 2'},
    {'id': 3, 'title': 'News 3', 'body': 'Text 3'},

]

@app.get("/search")
async def search(post_id: Optional[int] = None) -> dict:
    if post_id:
        for el in posts:
            if el['id'] == post_id:
                return el
        raise HTTPException(status_code=404, detail="Post not found")
    return {"data": "No post ID provided"}