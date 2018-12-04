import multiprocessing

workers = int(multiprocessing.cpu_count() / 2)
worker_class = 'uvicorn.workers.UvicornWorker'
