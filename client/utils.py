import requests

API_URL = "http://127.0.0.1:8000/tasks"

def get_tasks():
    try:
        resp = requests.get(API_URL)
        if resp.status_code == 200:
            return resp.json()
        return []
    except:
        return []

def add_task(task):
    try:
        resp = requests.post(API_URL, json=task)
        return resp.status_code == 200 or resp.status_code == 201
    except:
        return False

def update_task(task_id, task):
    try:
        resp = requests.put(f"{API_URL}/{task_id}", json=task)
        return resp.status_code == 200
    except:
        return False
