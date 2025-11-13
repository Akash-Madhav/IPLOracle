FROM python:3.12-slim-bullseye

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1 --limit-concurrency 50 --timeout-keep-alive 5"]

HEALTHCHECK CMD curl --fail http://localhost:$PORT/health || exit 1