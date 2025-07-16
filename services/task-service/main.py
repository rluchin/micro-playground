from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4
import json, os, asyncio

app = FastAPI(title="Task Service")
DB_FILE = os.getenv("DB_FILE", "tasks.json")
lock = asyncio.Lock()

# ------------------------------------------------------------------
# 1. Pydantic schemas
# ------------------------------------------------------------------
class TaskCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=200)

class Task(TaskCreate):
    id: str
    done: bool = False

# ------------------------------------------------------------------
# 2. Persistence helpers
# ------------------------------------------------------------------
def _read() -> list[Task]:
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE) as f:
        data = json.load(f)
    return [Task(**item) for item in data]

def _write(tasks: list[Task]) -> None:
    with open(DB_FILE, "w") as f:
        json.dump([t.dict() for t in tasks], f, indent=2)

# ------------------------------------------------------------------
# 3. API routes
# ------------------------------------------------------------------
@app.get("/tasks", response_model=list[Task])
async def list_tasks():
    return _read()

@app.post("/tasks", response_model=Task, status_code=201)
async def add_task(payload: TaskCreate):
    async with lock:
        tasks = _read()
        new_task = Task(id=str(uuid4()), text=payload.text, done=False)
        _write(tasks + [new_task])
    return new_task

@app.patch("/tasks/{task_id}", status_code=204)
async def update_task(task_id: str, done: bool):
    async with lock:
        tasks = _read()
        updated = False
        for t in tasks:
            if t.id == task_id:
                t.done = done
                updated = True
        if not updated:
            raise HTTPException(404, "task not found")
        _write(tasks)