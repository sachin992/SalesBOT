


import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import os
import json
import uuid
from streamlit_cookies_manager import EncryptedCookieManager

API_URL = "http://127.0.0.1:8000/api/query/"
REFRESH_URL = "http://127.0.0.1:8000/api/token/refresh/"

# -----------------------------
# Cookies setup
# -----------------------------
cookies = EncryptedCookieManager(
    prefix="sales_gpt_",
    password="YOUR_SECRET_PASSWORD_32CHARS"
)

if not cookies.ready():
    st.stop()  # wait for cookies to load

# -----------------------------
# Authentication check
# -----------------------------
authenticated = st.session_state.get("authenticated", False)
access = st.session_state.token
refresh = cookies.get("refresh")
username = cookies.get("username")
print(access, refresh, username, authenticated)
if not authenticated or not access:
     st.switch_page("pages/login.py")

# Ensure session_state token is up to date
st.session_state.token = access

# -----------------------------
# Helper: refresh token
# -----------------------------
def refresh_access_token():
    refresh = cookies.get("refresh")
    if not refresh:
        return False
    resp = requests.post(REFRESH_URL, json={"refresh": refresh})
    if resp.status_code == 200:
        new_access = resp.json().get("access")
        cookies["access"] = new_access
        cookies.save()
        st.session_state.token = new_access
        return True
    return False

# -----------------------------
# Session state defaults
# -----------------------------
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("last_df", None)
st.session_state.setdefault("is_typing", False)
st.session_state.setdefault("dark_mode", False)

# -----------------------------
# Persistent user ID
# -----------------------------
CHAT_DIR = "chat_data"
os.makedirs(CHAT_DIR, exist_ok=True)

if "user_id" not in cookies:
    cookies["user_id"] = str(uuid.uuid4())
    cookies.save()

user_id = cookies["user_id"]
chat_file = os.path.join(CHAT_DIR, f"{user_id}.json")

# Load chat history
if os.path.exists(chat_file):
    with open(chat_file, "r") as f:
        st.session_state.chat_history = json.load(f)
else:
    st.session_state.chat_history = []

def save_chat():
    with open(chat_file, "w") as f:
        json.dump(st.session_state.chat_history, f)

# -----------------------------
# Sidebar: Settings
# -----------------------------
st.sidebar.title("⚙️ Settings")
st.session_state.dark_mode = st.sidebar.checkbox("Dark Mode", value=st.session_state.dark_mode)

# -----------------------------
# CSS styling
# -----------------------------
if st.session_state.dark_mode:
    bg_color = "#1e1e1e"
    bubble_user_bg = "#1565c0"
    bubble_user_color = "#fff"
    bubble_bot_bg = "#2c2c2c"
    bubble_bot_color = "#fff"
    page_bg = "#121212"
    text_color = "#eee"
else:
    bg_color = "#f7f7f8"
    bubble_user_bg = "#1e88e5"
    bubble_user_color = "#fff"
    bubble_bot_bg = "#fff"
    bubble_bot_color = "#000"
    page_bg = "#fff"
    text_color = "#000"

st.markdown(f"""
<style>
body {{ background-color: {page_bg}; color: {text_color}; }}
.chat-wrapper {{ display:flex; flex-direction:column; min-height:300px; max-height:70vh; overflow:hidden; border-radius:12px; background:{bg_color}; border:1px solid #ddd; box-shadow:0px 2px 8px rgba(0,0,0,0.08);}}

/* Message styling */
.chat-container {{ flex:1; padding:16px; overflow-y:auto; display:flex; flex-direction:column; }}
.message-row {{ display:flex; align-items:flex-start; gap:10px; margin:10px 0; animation:fadeIn 0.25s ease-in-out; }}
.message-row.user {{ justify-content:flex-end; }}
.avatar {{ width:36px; height:36px; border-radius:50%; }}
.message-bubble {{ padding:12px 16px; max-width:650px; border-radius:12px; line-height:1.4; font-size:1rem; white-space:pre-wrap; }}
.message-bubble.bot {{ background:{bubble_bot_bg}; color:{bubble_bot_color}; border:1px solid #444; }}
.message-bubble.user {{ background:{bubble_user_bg}; color:{bubble_user_color}; }}
.message-bubble pre {{ background:#222; color:#eee; padding:10px; border-radius:8px; overflow-x:auto; }}
.message-bubble pre.sql {{ background:#1e1e1e; color:#dcdcdc; }}
.timestamp {{ font-size:0.7rem; color:#999; margin-top:4px; }}
.empty-message {{ text-align:center; color:#999; padding-top:20px; }}
.input-box {{ padding:14px; background:{page_bg}; border-top:1px solid #ddd; display:flex; gap:10px; }}
.chat-input {{ flex:1; padding:14px 18px; font-size:1rem; border-radius:24px; border:1px solid #ccc; outline:none; }}
.chat-input:focus {{ border-color:#1e88e5; box-shadow:0 0 0 2px rgba(30,136,229,0.2); }}
.typing-indicator {{ display:flex; gap:4px; }}
.typing-dot {{ width:6px; height:6px; background:#aaa; border-radius:50%; animation:blink 1.4s infinite both; }}
.typing-dot:nth-child(2) {{ animation-delay:0.2s; }}
.typing-dot:nth-child(3) {{ animation-delay:0.4s; }}
@keyframes blink {{ 0%{{opacity:.2;}}20%{{opacity:1;}}100%{{opacity:.2;}} }}
@keyframes fadeIn {{ from {{opacity:0; transform:translateY(5px);}} to {{opacity:1; transform:translateY(0);}} }}
@media (max-width:768px) {{ .message-bubble {{ max-width:90%; font-size:0.9rem; }} }}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.title("🤖 Sales GPT — Chat with Your Data")

# -----------------------------
# Process user query
# -----------------------------
def process_query(user_query):
    # Save user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_query,
        "timestamp": datetime.now().strftime("%H:%M")
    })
    save_chat()
    st.session_state.is_typing = True

    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    resp = requests.post(API_URL, json={"user_prompt": user_query}, headers=headers)

    # Refresh token if expired
    if resp.status_code == 401:
        if refresh_access_token():
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            resp = requests.post(API_URL, json={"user_prompt": user_query}, headers=headers)
        else:
            st.error("Session expired. Please log in again.")
            cookies["access"] = ""
            cookies["refresh"] = ""
            cookies.save()
            st.switch_page("pages/login.py")
            return

    data = resp.json()
    sql = data.get("sql", "")
    rows = data.get("result", {}).get("rows", [])

    bot_msg = f"<b>Generated SQL:</b><br><details><summary>View SQL</summary><pre>{sql}</pre></details>"

    if rows:
        df = pd.DataFrame(rows)
        st.session_state.last_df = df
        bot_msg += f"<br><b>{len(df)} rows returned.</b>"
    else:
        bot_msg += "<br><i>No data returned.</i>"

    st.session_state.chat_history.append({
        "role": "bot",
        "content": bot_msg,
        "timestamp": datetime.now().strftime("%H:%M")
    })
    save_chat()
    st.session_state.is_typing = False

# -----------------------------
# Render chat messages
# -----------------------------
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
st.markdown('<div id="chat-container" class="chat-container">', unsafe_allow_html=True)

if not st.session_state.chat_history:
    st.markdown('<div class="empty-message">Start by asking a question…</div>', unsafe_allow_html=True)
else:
    for msg in st.session_state.chat_history:
        timestamp = msg.get("timestamp", "")
        if msg["role"] == "user":
            avatar_html = '<img class="avatar user" src="https://cdn-icons-png.flaticon.com/512/847/847969.png">'
            row_class = "message-row user"
            bubble_html = f'<div class="message-bubble user">{msg["content"]}<div class="timestamp">{timestamp}</div></div>'
            st.markdown(f'<div class="{row_class}">{bubble_html}{avatar_html}</div>', unsafe_allow_html=True)
        else:
            avatar_html = '<img class="avatar bot" src="https://cdn-icons-png.flaticon.com/512/4712/4712100.png">'
            row_class = "message-row"
            bubble_html = f'<div class="message-bubble bot">{msg["content"]}<div class="timestamp">{timestamp}</div></div>'
            st.markdown(f'<div class="{row_class}">{avatar_html}{bubble_html}</div>', unsafe_allow_html=True)

# Typing indicator
if st.session_state.is_typing:
    st.markdown("""
        <div class="message-row">
            <img class="avatar bot" src="https://cdn-icons-png.flaticon.com/512/4712/4712100.png">
            <div class="message-bubble bot typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # end chat-container

# -----------------------------
# Data visualization
# -----------------------------
if st.session_state.last_df is not None:
    df = st.session_state.last_df
    st.subheader("📊 Query Result Data / Charts")
    st.dataframe(df, width="stretch")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    chart_type = st.selectbox("Select chart type", ["Line", "Bar", "Area"])

    if numeric_cols:
        df_plot = df[numeric_cols]
        if "created_at" in df.columns:
            try:
                df["created_at"] = pd.to_datetime(df["created_at"])
                df_plot = df.set_index("created_at")[numeric_cols]
            except:
                pass

        if chart_type == "Line":
            st.line_chart(df_plot)
        elif chart_type == "Bar":
            st.bar_chart(df_plot)
        elif chart_type == "Area":
            st.area_chart(df_plot)

    st.download_button("📥 Download CSV", df.to_csv(index=False), "data.csv")

# -----------------------------
# Input box with form (Enter submits)
# -----------------------------
# -----------------------------
# Input box with form (Enter submits)
# -----------------------------
st.markdown('<div class="input-box">', unsafe_allow_html=True)

def submit_question_callback():
    query = st.session_state.chat_input.strip()

    if query:
        process_query(query)

    # Safe reset BEFORE widget is rebuilt
    st.session_state.chat_input = ""

    # Force re-run to avoid modification-after-render error
    st.rerun()


with st.form("chat_form"):
    st.text_area(
        "Ask something...",
        key="chat_input",
        placeholder="Type your question here...",
        label_visibility="collapsed",
        height=80,
    )

    st.form_submit_button("Send", on_click=submit_question_callback)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
