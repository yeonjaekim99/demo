from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from store import (
    create_todo,
    delete_todo,
    get_all_todos,
    get_todo_by_id,
    update_todo,
)

app = FastAPI()


class CreateTodoRequest(BaseModel):
    title: str
    description: str = ""


class UpdateTodoRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


@app.get("/api/todos")
def list_todos():
    return get_all_todos()


@app.get("/api/todos/{todo_id}")
def get_todo(todo_id: int):
    if todo_id < 1:
        raise HTTPException(status_code=400, detail="유효하지 않은 ID입니다")

    todo = get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo를 찾을 수 없습니다")
    return todo


@app.post("/api/todos", status_code=201)
def create(req: CreateTodoRequest):
    if not req.title:
        raise HTTPException(status_code=400, detail="제목은 필수입니다")
    if not isinstance(req.title, str):
        raise HTTPException(status_code=400, detail="제목은 문자열이어야 합니다")
    if req.title.strip() == "":
        raise HTTPException(status_code=400, detail="제목은 빈 문자열일 수 없습니다")
    if len(req.title) > 200:
        raise HTTPException(status_code=400, detail="제목은 200자 이하여야 합니다")

    return create_todo(req.title.strip(), req.description)


@app.put("/api/todos/{todo_id}")
def update(todo_id: int, req: UpdateTodoRequest):
    if todo_id < 1:
        raise HTTPException(status_code=400, detail="유효하지 않은 ID입니다")

    if req.title is not None:
        if not isinstance(req.title, str):
            raise HTTPException(status_code=400, detail="제목은 문자열이어야 합니다")
        if req.title.strip() == "":
            raise HTTPException(
                status_code=400, detail="제목은 빈 문자열일 수 없습니다"
            )
        if len(req.title) > 200:
            raise HTTPException(
                status_code=400, detail="제목은 200자 이하여야 합니다"
            )

    if req.completed is not None and not isinstance(req.completed, bool):
        raise HTTPException(
            status_code=400, detail="completed는 boolean이어야 합니다"
        )

    updates = req.model_dump(exclude_none=True)
    updated = update_todo(todo_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo를 찾을 수 없습니다")
    return updated


@app.delete("/api/todos/{todo_id}", status_code=204)
def delete(todo_id: int):
    if todo_id < 1:
        raise HTTPException(status_code=400, detail="유효하지 않은 ID입니다")

    if not delete_todo(todo_id):
        raise HTTPException(status_code=404, detail="Todo를 찾을 수 없습니다")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3001)
