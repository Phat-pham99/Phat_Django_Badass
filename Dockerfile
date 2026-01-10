# --- Stage 1: Build Stage ---
FROM python:3.13-slim as builder
WORKDIR /app
COPY requirements.txt .
# Use --no-cache-dir to keep the layer small
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# --- Stage 2: Deployment Stage ---
FROM python:3.13-slim
WORKDIR /app

# Copy only installed packages and code from builder to keep image lean
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /app /app

ENV GRANIAN_HOST=0.0.0.0
EXPOSE 8000

# Chaining commands: Runs collectstatic, then starts Granian
CMD python3 manage.py collectstatic --clear --noinput && \
    granian --interface asgi Phat_Django_Badass.asgi:application --port 8000 --static-path-mount ./staticfiles
