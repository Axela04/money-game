import streamlit as st
from streamlit_extras.let_it_rain import rain

st.set_page_config(page_title="💸 Money Game for Kids", layout="centered")

# Initialize session state for persistent variables
if 'balance' not in st.session_state:
    st.session_state.balance = 100
    st.session_state.week = 1
    st.session_state.history = []

st.markdown("""
<style>
    .main { background-color: #f2f7ff; }
    h1, h2, h3, .stButton button {
        font-family: 'Comic Sans MS', cursive;
    }
    .stButton button {
        background-color: #FFDD57;
        color: black;
        border-radius: 10px;
        padding: 10px 16px;
        font-size: 16px;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.title("💸 AI-Powered Money Game for Kids")
st.subheader("Learn how to earn, save, and manage money — the fun way!")

income = 20
chore_options = ["🧹 Clean Room ($5)", "🍽 Wash Dishes ($7)", "🐕 Walk Dog ($8)"]
spending_options = ["🧸 Buy Toy ($15)", "🍬 Buy Snack ($5)", "❤️ Donate ($10)"]
tax_rate = 0.10

st.markdown(f"### 📅 Week {st.session_state.week}")
st.metric(label="💰 Your Balance", value=f"${st.session_state.balance:.2f}")

if st.button("💵 Earn Weekly Allowance"):
    taxed_income = income * (1 - tax_rate)
    st.session_state.balance += taxed_income
    st.session_state.history.append(f"Received ${taxed_income:.2f} allowance after ${income * tax_rate:.2f} tax")

st.markdown("---")
st.markdown("#### 🧽 Do a Chore:")
cols = st.columns(len(chore_options))
for idx, chore in enumerate(chore_options):
    with cols[idx]:
        if st.button(chore):
            amount = int(chore.split("($")[-1].replace(")", ""))
            taxed = amount * tax_rate
            final = amount - taxed
            st.session_state.balance += final
            st.session_state.history.append(f"Earned ${final:.2f} from {chore.split(' ($')[0]} (after ${taxed:.2f} tax)")

st.markdown("#### 🛍 What would you like to spend on?")
cols2 = st.columns(len(spending_options))
for idx, item in enumerate(spending_options):
    with cols2[idx]:
        if st.button(item):
            cost = int(item.split("($")[-1].replace(")", ""))
            if st.session_state.balance >= cost:
                st.session_state.balance -= cost
                st.session_state.history.append(f"Spent ${cost:.2f} on {item.split(' ($')[0]}")
            else:
                st.warning("Oops! Not enough money to buy that.")

if st.button("➡️ Go to Next Week"):
    st.session_state.week += 1
    if st.session_state.week % 3 == 0:
        surprise_cost = 12
        st.session_state.balance -= surprise_cost
        st.session_state.history.append(f"💥 Surprise! Your bike broke. Paid ${surprise_cost:.2f} for repairs.")
        st.error("🚲 Your bike broke this week! You had to pay $12 to fix it.")

st.markdown("---")
st.markdown("### 📜 Money Log")
for entry in reversed(st.session_state.history):
    st.write("-", entry)

rain(emoji="💸", font_size=28, falling_speed=5, animation_length="infinite")