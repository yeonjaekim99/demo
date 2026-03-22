from datetime import datetime

_todos: list[dict] = []
_next_id: int = 1


def get_all_todos() -> list[dict]:
    return _todos


def get_todo_by_id(todo_id: int) -> dict | None:
    for todo in _todos:
        if todo["id"] == todo_id:
            return todo
    return None


def create_todo(title: str, description: str = "") -> dict:
    global _next_id
    todo = {
        "id": _next_id,
        "title": title,
        "description": description,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    _next_id += 1
    _todos.append(todo)
    return todo


def update_todo(todo_id: int, updates: dict) -> dict | None:
    for i, todo in enumerate(_todos):
        if todo["id"] == todo_id:
            _todos[i] = {
                **todo,
                **updates,
                "updated_at": datetime.now().isoformat(),
            }
            return _todos[i]
    return None


def delete_todo(todo_id: int) -> bool:
    for i, todo in enumerate(_todos):
        if todo["id"] == todo_id:
            _todos.pop(i)
            return True
    return False


def reset_store():
    global _todos, _next_id
    _todos = []
    _next_id = 1
