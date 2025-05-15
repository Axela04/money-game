import streamlit as st
from streamlit_extras.let_it_rain import rain
from streamlit_extras.let_it_snow import snow
import matplotlib.pyplot as plt
import random
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="💸 Money Game for Kids", layout="centered")

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("MoneyGameData").sheet1

# Load from Google Sheets if available
try:
    values = sheet.get_all_records()
    if values:
        latest = values[-1]
        st.session_state.balance = float(latest['balance'])
        st.session_state.week = int(latest['week'])
        st.session_state.taxes_paid = float(latest['taxes_paid'])
        st.session_state.weekly_balances = eval(latest['weekly_balances'])
        st.session_state.history = eval(latest['history'])
except:
    pass

# At bottom, sync to sheet
def save_to_google():
    sheet.append_row([
        st.session_state.week,
        st.session_state.balance,
        st.session_state.taxes_paid,
        str(st.session_state.weekly_balances),
        str(st.session_state.history)
    ])

# At end of file, insert:
st.markdown("---")
st.markdown("### 🔗 Stay Connected")
st.markdown("[🎥 Visit our YouTube Channel](https://www.youtube.com/@aimomlab)")
st.markdown("[📝 Read our Blog on Blogger](https://aimomlab.blogspot.com)")

save_to_google()
