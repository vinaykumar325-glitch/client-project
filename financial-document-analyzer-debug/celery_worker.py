# celery_worker.py
from celery import Celery
from main import run_crew

app = Celery('worker', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@app.task
def analyze_async(query: str, file_path: str = None):
    return run_crew(query=query, file_path=file_path)
