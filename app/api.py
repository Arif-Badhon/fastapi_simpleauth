# app/api.py
from fastapi import FastAPI
from app.model import PostSchema

posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]

users = []

app = FastAPI()

@app.get("/", tags=["root"])
def read_root() -> dict:
    return {"message": "Welcome to this app"}

@app.get("/posts", tags=["posts"])
def get_posts() -> dict:
    return {"data": posts}


@app.get("/posts/{id}", tags=["posts"])
def single_post(id: int) -> dict:
    if id > len(posts):
        return {
            "error": "no such post"
        }
    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }

@app.post("/posts", tags=["posts"])
def add_post(post:PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())
    return{
        "data" : "post added"
    }