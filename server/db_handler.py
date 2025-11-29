import json, os
from server.models import Task

DATA_FILE = 'data/task.json'

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        try:
            tasks_data = json.load(f)
        except json.JSONDecodeError:
            tasks_data = []
    return [Task(**task) for task in tasks_data]

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump([task.dict() for task in tasks], f, indent=4)