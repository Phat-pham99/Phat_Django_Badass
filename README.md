# Phat_Django_Badass
> This is the Django backend to handle all the stuff in my life.
I meant from personal finance, investment, dividend income or my gym routine to other stuffs that requires data management.
I intended to build this not for my own usage only but for my family as well. User authentication and permission will be not a big deal tho
-----

<h2>Financial Dashboard</h2>
<p>My personal financial dashboard to keep things up-to-date</p>

<img title="" alt="" src="statics/Phat_Django_Dashboard.png"
style="width:100%"/>

-----

<h2>Investment</h2>
<p>Track my investment progress overtime, data input via Django admin model input form</p>

<img title="" alt="" src="statics/phat_investment_portfolio.png"
style="width:100%"/>

## Tech used
I want to keep cost down so I try some free-tier services, which also get the job done (the user pool is small, to be hosnest 👀😏)

- Clouflare D1 databasse <-> SQLite 🛢️\
The main database is hosted using Clouflare D1, this is the most suitable SQL cloudbase I can find to be cost-effective and lightweight. Of course, the database needs to be ACID compliant, or else the whole transaction thingy will be pointless.

- Upstash Redis <-> Redis 🟥 \
Redis is a exellent key-value based database, suitable for rapidly update value like balances, expenses and my real-time financial dashboard

## Docker
`sudo docker build . --tag Phat_Django_Badass:<version>`

## Static files
Templates reference assets via `{% static %}` (served from `STATIC_URL = "static/"`).

- **Development (`DEBUG=True`):** `runserver` serves static files automatically.
- **Production (`DEBUG=False`):** the app serves static files through a dedicated route in `Phat_Django_Badass/urls.py` (only registered when `DEBUG` is off). When deploying behind a reverse proxy (e.g. Caddy/nginx), prefer serving `staticfiles/` from the proxy after `python manage.py collectstatic` instead of relying on the in-app route.

## Release history
- **1.3.2** – Serve static files when `DEBUG` is `False` (fixes 404 CSS/JS on the dashboard and other pages).
