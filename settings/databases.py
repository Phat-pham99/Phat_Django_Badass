import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': os.getenv('ENGINE'),
        'CLOUDFLARE_DATABASE_ID': os.getenv('CLOUDFLARE_DATABASE_ID'),
        'CLOUDFLARE_ACCOUNT_ID': os.getenv('CLOUDFLARE_ACCOUNT_ID'),
        'CLOUDFLARE_TOKEN': os.getenv('CLOUDFLARE_TOKEN'),
        'CONN_MAX_AGE': 60 * 10,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"rediss://{os.getenv('UPSTASH_REDIS_USERNAME')}@{os.getenv('UPSTASH_REDIS_ENDPOINT')}:{os.getenv('UPSTASH_REDIS_PORT')}/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": os.getenv('UPSTASH_REDIS_PASSWORD'),
            # Upstash does not support CLIENT MAINT_NOTIFICATIONS (RESP3 feature).
            # redis-py >=7.1 defaults to RESP3 (protocol=3) which tries that command
            # and logs DEBUG "Failed to enable maintenance notifications".
            # Force RESP2 to silence it. See https://upstash.com/docs/redis/overall/rediscompatibility
            "CONNECTION_POOL_KWARGS": {"protocol": 2},
        }
    }
}
