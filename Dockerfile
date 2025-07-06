FROM python:3.13.5-alpine3.21

WORKDIR .

COPY . ./

COPY requirements.txt ./

# Install any Python dependencies
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 8000
ENTRYPOINT ["python3","-m","hypercorn", "--reload", "Phat_Django_Badass.asgi:application", "--bind", "0.0.0.0:8000",]