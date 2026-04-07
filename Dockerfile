FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn

EXPOSE 8000

<<<<<<< HEAD
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
=======
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> 4de9549e9f215b1612d459325fba8eba08bcef4c
