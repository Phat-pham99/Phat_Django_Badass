eval "$(poetry env activate)"
granian --interface asgi Phat_Django_Badass.asgi:application --port 8000 --static-path-mount ./staticfiles --workers-kill-timeout 5
