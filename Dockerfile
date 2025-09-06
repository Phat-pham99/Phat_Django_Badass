FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .env .

COPY . .

EXPOSE 8000

CMD ["python3", "-m", "hypercorn", "Phat_Django_Badass.asgi:application", "--bind", "0.0.0.0:8000"]
