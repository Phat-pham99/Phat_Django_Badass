eval "$(poetry env activate)"
hypercorn Phat_Django_Badass.asgi:application --reload -b 0.0.0.0:8000 --access-logfile Django_log.log

