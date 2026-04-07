FROM python:3.10

WORKDIR /app
<<<<<<< HEAD
COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "7860"]
=======

COPY . /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> d4d54a4fbfdb771cbe88107dcf9cd40ac0e2efc2
