FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install uv
RUN uv sync

CMD ["python", "-m", "server.app"]