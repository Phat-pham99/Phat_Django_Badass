eval "$(poetry env activate)"
granian --interface asgi Phat_Django_Badass.asgi:application --reload --port 8000 --no-ws --static-path-mount ./staticfiles
