# 💸 AI Mom Lab: Money Game for Kids

A gamified financial learning app for kids, powered by Streamlit.

## 🔑 Features
- Weekly allowance system
- Chore tracking with time limits
- Tax payments and random IRS audits
- Compound interest
- Options trading simulation
- Parent PIN controls
- Persistent save/load with Google Sheets
- Weekly balance tracking

## 🌐 Hosted on Streamlit + Synced with Google Sheets

## ▶️ To Run
1. Clone the repo
2. Add `google_credentials.json` to root
3. Create a Google Sheet titled `MoneyGameData` with these columns:
   ```
   week | balance | taxes_paid | weekly_balances | history
   ```
4. Install requirements:
   ```
   pip install -r requirements.txt
   ```
5. Run app:
   ```
   streamlit run app.py
   ```

## 📺 Follow Us
- [YouTube Channel](https://www.youtube.com/@aimomlab)
- [Blogger Site](https://aimomlab.blogspot.com)
