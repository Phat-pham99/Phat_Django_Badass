# `python-base` sets up all our shared environment variables
# FROM python:3.11-buster as builder
# FROM patrickhuber/sqlite:3.31.0 as builder
# # 
# # RUN  pip install --upgrade sqlite3
# # RUN sqlite3 --version

# WORKDIR .

# # COPY pyproject.toml poetry.lock ./
# COPY requirements.txt ./

# RUN  pip install -r requirements.txt

# Stage 1: SQLite
# FROM patrickhuber/sqlite:3.31.0 AS sqlite_stage

# Stage 2: Python with SQLite
FROM python:3.13.3-alpine3.21

# Copy SQLite from the first stage
# COPY --from=sqlite_stage / /

# RUN apt update -y
# RUN apt upgrade -y
# RUN apt install -f libc6 
# Set working directory
WORKDIR .

# Copy your Python application
COPY . ./

COPY requirements.txt ./

# Install any Python dependencies
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 8000
# ENTRYPOINT ["gunicorn", "--reload", "Phat_Django_Badass.wsgi:app"]
ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]