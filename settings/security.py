import os

_hosts_raw: str = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost')
_hosts_raw: str = _hosts_raw.strip().strip("[]")
ALLOWED_HOSTS: list[str] = [h.strip().strip("'\"") for h in _hosts_raw.split(',') if h.strip()] or ['127.0.0.1', 'localhost']
CORS_ALLOW_ALL_ORIGINS: bool = True

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
