dev:
	uvicorn main:app --reload --port 3000
start:
	gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind localhost:3000