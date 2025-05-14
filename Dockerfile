# `python-base` sets up all our shared environment variables
FROM python:3.10

RUN apt update
RUN pip install "poetry===2.1.3"
RUN pip install "gunicorn===20.1.0"

COPY poetry.lock pyproject.toml ./
COPY . ./

# quicker install as runtime deps are already installed
# RUN poetry install --no-root

# will become mountpoint of our code
WORKDIR .

EXPOSE 8000
CMD ["gunicorn", "--reload", "Phat_Django_Badass.wsgi:app"]

#Activate poetry env, bruh