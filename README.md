# 💸 AI Mom Lab: Money Game for Kids

A gamified financial learning app for kids, with Google Sheets sync.

## Features
- Weekly allowance, chores, and interest
- Options trading, tax system, audits
- PIN-protected parent controls
- Google Sheets save/load with user profiles

## Setup
1. Create a Google Sheet `MoneyGameData` with columns:
   username | week | balance | taxes_paid | weekly_balances | history

2. Add your credentials to Streamlit Secrets as:
   GOOGLE_CREDENTIALS = """{...}"""

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

Visit:
- [YouTube](https://www.youtube.com/@aimomlab)
- [Blog](https://aimomlab.blogspot.com)
