import streamlit as st
from streamlit_extras.let_it_rain import rain
from streamlit_extras.let_it_snow import snow
import matplotlib.pyplot as plt
import random
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from io import StringIO

st.set_page_config(page_title="💸 Money Game for Kids", layout="centered")

# User selector
st.sidebar.title("👤 Select User")
username = st.sidebar.text_input("Enter your name")

# Only proceed if username provided
if not username:
    st.warning("Please enter your name to start the game.")
    st.stop()

# Google Sheets setup using Streamlit secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = StringIO(st.secrets["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scope)
client = gspread.authorize(creds)
sheet = client.open("MoneyGameData").sheet1

# Load from Google Sheets
def load_user_data(username):
    records = sheet.get_all_records()
    for row in records:
        if row['username'] == username:
            st.session_state.balance = float(row['balance'])
            st.session_state.week = int(row['week'])
            st.session_state.taxes_paid = float(row['taxes_paid'])
            st.session_state.weekly_balances = json.loads(row['weekly_balances'])
            st.session_state.history = json.loads(row['history'])
            return True
    return False

# Save to Google Sheets
def save_user_data():
    sheet.append_row([
        username,
        st.session_state.week,
        st.session_state.balance,
        st.session_state.taxes_paid,
        json.dumps(st.session_state.weekly_balances),
        json.dumps(st.session_state.history)
    ])

# Try loading user data
if 'loaded' not in st.session_state:
    if load_user_data(username):
        st.success(f"Loaded saved data for {username}.")
    else:
        st.info(f"Welcome {username}! Starting fresh.")
    st.session_state.loaded = True

# Save/Load buttons
st.sidebar.markdown("---")
if st.sidebar.button("💾 Save Progress"):
    save_user_data()
    st.sidebar.success("Progress saved!")

if st.sidebar.button("🔄 Load Progress"):
    if load_user_data(username):
        st.sidebar.success("Progress loaded!")
    else:
        st.sidebar.error("No saved data found.")

# Footer
st.markdown("---")
st.markdown("### 🔗 Stay Connected")
st.markdown("[🎥 Visit our YouTube Channel](https://www.youtube.com/@aimomlab)")
st.markdown("[📝 Read our Blog on Blogger](https://aimomlab.blogspot.com)")
