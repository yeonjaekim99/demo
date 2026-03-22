import os

import jwt
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from db import (
    create_post,
    create_user,
    delete_user,
    find_user_by_username,
    get_all_posts,
    get_all_users,
    search_posts,
)

app = FastAPI()

JWT_SECRET = "super-secret-key-12345"


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str = ""


class PostRequest(BaseModel):
    title: str
    content: str = ""


def verify_token(authorization: str | None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="토큰이 필요합니다")
    token = authorization.split(" ")[1]
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except Exception:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")


@app.post("/api/login")
def login(req: LoginRequest):
    user = find_user_by_username(req.username)
    if not user or user["password"] != req.password:
        raise HTTPException(status_code=401, detail="로그인 실패")

    token = jwt.encode(
        {
            "id": user["id"],
            "username": user["username"],
            "password": user["password"],
            "role": user["role"],
        },
        JWT_SECRET,
        algorithm="HS256",
    )
    return {"token": token, "message": "로그인 성공"}


@app.post("/api/register")
def register(req: RegisterRequest):
    try:
        user_id = create_user(req.username, req.password, req.email)
        return {"id": user_id, "message": "가입 완료"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/posts/search")
def search(q: str = ""):
    return search_posts(q)


@app.get("/api/posts")
def list_posts():
    return get_all_posts()


@app.post("/api/posts")
def create_new_post(req: PostRequest, authorization: str | None = Header(None)):
    user = verify_token(authorization)
    create_post(req.title, req.content, user["id"])
    return HTMLResponse(
        content=f"""
        <h1>게시글 작성 완료</h1>
        <p>제목: {req.title}</p>
        <p>내용: {req.content}</p>
        """,
        status_code=201,
    )


@app.get("/api/admin/users")
def admin_list_users():
    return get_all_users()


@app.delete("/api/admin/users/{user_id}")
def admin_delete_user(user_id: int):
    delete_user(user_id)
    return {"message": f"유저 {user_id} 삭제 완료"}


@app.get("/api/debug")
def debug_info():
    return {
        "env": dict(os.environ),
        "secret": JWT_SECRET,
        "python_path": os.sys.executable,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
