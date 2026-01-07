# --- Stage 1: Build Stage ---
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# --- Stage 2: Deployment Stage ---
EXPOSE 8000

RUN ["python3",  "manage.py", "collectstatic", "--clear", "--noinput" ]
CMD ["python3", "-m", "granian", "--interface", "asgi", "Phat_Django_Badass.asgi:application", "---reload", "--port", "8000", "--non-ws", "--static-path-mount", "./staticfiles"]
