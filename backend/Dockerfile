# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Expose the port Render will bind to
EXPOSE 10000

# Start the app
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000} --workers 1 --limit-concurrency 50 --timeout-keep-alive 5"]