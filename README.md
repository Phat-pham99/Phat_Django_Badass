<p align="center">
  <h1 align="center">Phat_Django_Badass</h1>
  <p align="center">
    <b>Your personal command center for finance, investments, and life admin.</b><br>
    Built with Django. Designed for family-scale use.
  </p>
</p>

---

## About

This Django backend powers everything from personal finance, investments, and dividend income to gym routines and any other data-driven corners of life.

Originally built for myself and extended for my family, it comes with robust user authentication and permission management baked in from day one.

---

## Features

### Financial Dashboard
A clean, real-time dashboard to keep your personal finances up to date.

<p align="center">
  <img alt="Dashboard - Light Mode" src="statics/Phat_Django_Dashboard_light.png" width="100%">
  <img alt="Dashboard - Dark Mode" src="statics/Phat_Django_Dashboard_dark.png" width="100%">
</p>

### Expense Tracker
Visualize spending habits and expenses at a glance.

<p align="center">
  <img alt="Expense Tracker" src="statics/Phat_Expense.png" width="100%">
</p>

### Investment Tracker
Track investment progress over time. Data is entered via Django's built-in admin interface.

<p align="center">
  <img alt="Investment Portfolio" src="statics/phat_investment_portfolio.png" width="100%">
</p>

---

## Tech Stack

Kept lean and cost-effective — running on generous free-tier services that easily handle a small user pool (just family & friends 👀).

| Service | Role | Why It Fits |
|---------|------|-------------|
| **Django** | Backend & Admin | Python web framework for rapid, secure development |
| **Cloudflare D1** 🛢️ | Primary Database | Serverless SQLite — ACID compliant, lightweight, and cost-effective |
| **Upstash Redis** 🟥 | Caching & Real-time | Lightning-fast key-value store for balances, expenses, and live dashboard metrics |
| **Docker** 🐳 | Deployment | Consistent, portable environments across the board |

---

## Docker

Build the image:

```bash
sudo docker build . --tag Phat_Django_Badass:<version>
```

---

## License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute it as you see fit.
See [LICENSE](LICENSE) for full details.
