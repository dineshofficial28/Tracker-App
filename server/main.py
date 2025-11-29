from fastapi import FastAPI, HTTPException
from server.models import Task
from server.db_handler import load_tasks, save_tasks
from typing import List

app = FastAPI(
    title="Task Tracker API",
    description="API for managing tasks with various frequencies",
)

tasks = load_tasks()

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
def add_task(task: Task):
    tasks.append(task)
    save_tasks(tasks)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks[index] = updated_task
            save_tasks(tasks)
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    save_tasks(tasks)
    return {"detail": "Task deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)