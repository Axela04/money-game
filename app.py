import streamlit as st
from streamlit_extras.let_it_rain import rain
import matplotlib.pyplot as plt
import random
import time

st.set_page_config(page_title="💸 Money Game for Kids", layout="centered")

# Initialize session state for persistent variables
if 'balance' not in st.session_state:
    st.session_state.balance = 100
    st.session_state.week = 1
    st.session_state.history = []
    st.session_state.weekly_balances = [100]
    st.session_state.interest_rate = 0.05  # 5% compound interest per week
    st.session_state.reading_challenge_completed = False
    st.session_state.gadgets = []
    st.session_state.chore_timestamps = {}
    st.session_state.daily_chore_count = 0
    st.session_state.daily_chore_time = 0
    st.session_state.max_chores_per_day = 3

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
chore_options = ["🧹 Clean Room ($5, 15min)", "🍽 Wash Dishes ($7, 10min)", "🐕 Walk Dog ($8, 20min)"]
chore_times = {"🧹 Clean Room ($5, 15min)": 15, "🍽 Wash Dishes ($7, 10min)": 10, "🐕 Walk Dog ($8, 20min)": 20}
spending_options = ["🧸 Buy Toy ($15)", "🍬 Buy Snack ($5)", "❤️ Donate ($10)", "📱 Gadget ($50)"]
tax_rate = 0.10
chore_cooldown = 60 * 20  # 20 minutes
current_time = int(time.time())

st.markdown(f"### 📅 Week {st.session_state.week}")
st.metric(label="💰 Your Balance", value=f"${st.session_state.balance:.2f}")

st.markdown(f"**Daily Chores Done:** {st.session_state.daily_chore_count} / {st.session_state.max_chores_per_day}")
st.markdown(f"**Total Time Spent on Chores Today:** {st.session_state.daily_chore_time} min")

if st.button("💵 Earn Weekly Allowance"):
    taxed_income = income * (1 - tax_rate)
    st.session_state.balance += taxed_income
    st.session_state.history.append(f"Received ${taxed_income:.2f} allowance after ${income * tax_rate:.2f} tax")

st.markdown("---")
st.markdown("#### 🧽 Do a Chore:")
cols = st.columns(len(chore_options))
for idx, chore in enumerate(chore_options):
    with cols[idx]:
        last_done = st.session_state.chore_timestamps.get(chore, 0)
        if st.session_state.daily_chore_count >= st.session_state.max_chores_per_day:
            st.button(f"{chore}\n🚫 Max chores done today", disabled=True)
        elif current_time - last_done < chore_cooldown:
            minutes_left = int((chore_cooldown - (current_time - last_done)) / 60)
            st.button(f"{chore}\n⏳ {minutes_left} min left", disabled=True)
        else:
            if st.button(chore):
                amount = int(chore.split("($")[-1].split(",")[0])
                chore_duration = chore_times[chore]
                taxed = amount * tax_rate
                final = amount - taxed
                st.session_state.balance += final
                st.session_state.daily_chore_count += 1
                st.session_state.daily_chore_time += chore_duration
                st.session_state.history.append(f"Earned ${final:.2f} from {chore.split(' ($')[0]} (after ${taxed:.2f} tax)")
                st.session_state.chore_timestamps[chore] = current_time

st.markdown("#### 🧠 Weekly Reading Challenge:")
if not st.session_state.reading_challenge_completed:
    if st.button("📖 Complete Reading Challenge (+$10 reward)"):
        st.session_state.balance += 10
        st.session_state.reading_challenge_completed = True
        st.session_state.history.append("Completed weekly reading challenge and earned $10")
else:
    st.success("You've already completed this week's reading challenge!")

st.markdown("#### 🛍 What would you like to spend on?")
cols2 = st.columns(len(spending_options))
for idx, item in enumerate(spending_options):
    with cols2[idx]:
        if st.button(item):
            cost = int(item.split("($")[-1].replace(")", ""))
            if st.session_state.balance >= cost:
                st.session_state.balance -= cost
                item_name = item.split(" ($")[0]
                if "Gadget" in item:
                    st.session_state.gadgets.append(f"{item_name} (Week {st.session_state.week})")
                st.session_state.history.append(f"Spent ${cost:.2f} on {item_name}")
            else:
                st.warning("Oops! Not enough money to buy that.")

if st.button("➡️ Go to Next Week"):
    st.session_state.week += 1
    # Apply compound interest
    interest = st.session_state.balance * st.session_state.interest_rate
    st.session_state.balance += interest
    st.session_state.history.append(f"Earned ${interest:.2f} in weekly interest (5%)")
    # Save weekly balance
    st.session_state.weekly_balances.append(round(st.session_state.balance, 2))
    # Reset daily chore stats
    st.session_state.daily_chore_count = 0
    st.session_state.daily_chore_time = 0
    # Reset reading challenge
    st.session_state.reading_challenge_completed = False
    # Random surprise expense
    if st.session_state.week % 3 == 0:
        surprise_cost = 12
        st.session_state.balance -= surprise_cost
        st.session_state.history.append(f"💥 Surprise! Your bike broke. Paid ${surprise_cost:.2f} for repairs.")
        st.error("🚲 Your bike broke this week! You had to pay $12 to fix it.")

st.markdown("---")
st.markdown("### 📈 Weekly Savings Growth Chart")
fig, ax = plt.subplots()
ax.plot(range(1, len(st.session_state.weekly_balances)+1), st.session_state.weekly_balances, marker='o')
ax.set_title("Balance Over Time")
ax.set_xlabel("Week")
ax.set_ylabel("Balance ($)")
st.pyplot(fig)

st.markdown("---")
st.markdown("### 📜 Money Log")
for entry in reversed(st.session_state.history):
    st.write("-", entry)

if st.session_state.gadgets:
    st.markdown("### 🧸 Gadgets You've Earned:")
    for g in st.session_state.gadgets:
        st.write("-", g)

rain(emoji="💸", font_size=28, falling_speed=5, animation_length="infinite")
