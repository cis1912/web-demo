from typing import Annotated

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks = []


@app.get("/tasks")
def get_tasks():
    return tasks


@app.post("/tasks")
def create_task(task: Annotated[str, Body(embed=True)]):
    tasks.append({
        "id": len(tasks),
        "task": task,
        "completed": False,
    })
    return tasks


@app.delete("/tasks/{id}")
def delete_task(id: int):
    matches = [i for i, t in enumerate(tasks) if t["id"] == id]
    if len(matches) == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    idx = matches[0]
    tasks.remove(tasks[idx])
    return tasks


@app.put("/tasks/{id}")
def update_task(id: int,
                task: Annotated[str, Body(embed=True)],
                completed: Annotated[bool, Body(embed=True)]):
    matches = [i for i, t in enumerate(tasks) if t["id"] == id]
    if len(matches) == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    idx = matches[0]
    tasks[idx] = {
        "id": id,
        "task": task,
        "completed": completed,
    }
    return tasks
