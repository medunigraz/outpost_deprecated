import multiprocessing
import os

workers = int(os.environ.get(
    'OUTPOST_GUNICORN_WORKERS',
    multiprocessing.cpu_count() / 2
))
worker_class = 'uvicorn.workers.UvicornH11Worker'
