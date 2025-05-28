# eval "$(poetry env activate)"
source /home/codespace/.cache/pypoetry/virtualenvs/phat-django-badass-Y9-ht7DM-py3.12/bin/activate
gunicorn Phat_Django_Badass.wsgi:application --threads 5 --bind 0.0.0.0:8000
