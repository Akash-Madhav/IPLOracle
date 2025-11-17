FROM python:3.12-slim-bullseye

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code and startup script
COPY . .
COPY start.sh ./
RUN chmod +x start.sh

EXPOSE 10000

# Run memory cleanup before starting the app
CMD ["./start.sh"]

# Healthcheck for container monitoring
HEALTHCHECK CMD curl --fail http://localhost:$PORT/health || exit 1