import streamlit as st

st.set_page_config(
    page_title="Sales GPT",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Welcome to Sales GPT")

st.markdown("""
Welcome to **Sales GPT**, your AI assistant for analyzing sales data.

- Go to **Login** to start chatting with the bot.
- Use the sidebar to navigate between pages once logged in.
""")

# Optional button to redirect directly to login page
if st.button("Go to Login"):
    st.switch_page("pages/login.py")
