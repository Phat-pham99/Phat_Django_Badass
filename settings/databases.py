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
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"rediss://{os.getenv('UPSTASH_REDIS_USERNAME')}@{os.getenv('UPSTASH_REDIS_ENDPOINT')}:{os.getenv('UPSTASH_REDIS_PORT')}/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": os.getenv('UPSTASH_REDIS_PASSWORD'),
        }
    }
}
