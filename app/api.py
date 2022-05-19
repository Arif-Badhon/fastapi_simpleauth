# app/api.py

from fastapi import FastAPI, Body, Depends

from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

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

@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
def add_post(post:PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())
    return{
        "data" : "post added"
    }

@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema=Body(...)):
    users.append(user)
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return{
        "error": "wrong login details"
    }

