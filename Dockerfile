FROM python:3.13.4-alpine3.21

WORKDIR .

COPY . ./

COPY requirements.txt ./

# Install any Python dependencies
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 8000
ENTRYPOINT ["python3","-m","gunicorn", "--reload", "Phat_Django_Badass.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "2"]