# --- Stage 1: Build Stage ---
FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# --- Stage 2: Running Stage ---
EXPOSE 8000

CMD ["python3", "-m", "hypercorn", "Phat_Django_Badass.asgi:application", "--bind", "0.0.0.0:8000"]
