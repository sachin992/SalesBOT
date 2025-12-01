# import streamlit as st
# import pandas as pd
# import requests

# API_URL = "http://127.0.0.1:8000/api/query/"

# st.title("📊 Sales — Natural Language Analytics")
# query = st.text_area("Ask a question about your sales data:")

# if st.button("Run Query"):
#     if not query.strip():
#         st.error("❗ Please type a question before running.")
#     else:
#         with st.spinner("⏳ Processing..."):
#             payload = {"user_prompt": query}
#             resp = requests.post(API_URL, json=payload)

#         # --- Handle errors from backend ---
#         if resp.status_code != 200:
#             st.error(f"❌ Server Error: {resp.json()}")
#         else:
#             data = resp.json()

#             # Show generated SQL
#             st.subheader("🧠 Generated SQL Query")
#             st.code(data["sql"], language="sql")

#             # Extract result rows
#             rows = data["result"].get("rows", [])

#             if rows:
#                 df = pd.DataFrame(rows)
#                 st.subheader("📄 Result Data")
#                 st.dataframe(df)

#                 # --- Simple Auto Chart Logic ---
#                 numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

#                 if "created_at" in df.columns:
#                     try:
#                         df["created_at"] = pd.to_datetime(df["created_at"])
#                         st.subheader("📈 Trend Chart")
#                         st.line_chart(df.set_index("created_at")[numeric_cols])
#                     except:
#                         pass
#                 elif len(numeric_cols) >= 1:
#                     st.subheader("📊 Bar Chart")
#                     st.bar_chart(df[numeric_cols[0]])
#                 else:
#                     st.info("⚠ Data returned but no numeric fields available to plot.")
#             else:
#                 st.warning("⚠ Query executed successfully but returned no records.")


# import streamlit as st
# import pandas as pd
# import requests

# API_URL = "http://127.0.0.1:8000/api/query/"

# # -------------------------
# # CSS for GPT-style chat
# # -------------------------
# chat_css = """
# <style>
# .chat-container {
#     max-height: 70vh;
#     overflow-y: auto;
#     padding: 10px;
#     display: flex;
#     flex-direction: column-reverse;
# }

# .chat-message {
#     padding: 0.8rem;
#     border-radius: 0.6rem;
#     margin-bottom: 0.5rem;
#     max-width: 90%;
#     word-wrap: break-word;
# }

# .chat-message.user {
#     background-color: #2b313e;
#     color: #fff;
#     align-self: flex-end;
# }

# .chat-message.bot {
#     background-color: #475063;
#     color: #fff;
#     align-self: flex-start;
# }

# .chat-message pre {
#     background: #333;
#     padding: 0.5rem;
#     border-radius: 0.4rem;
#     overflow-x: auto;
# }
# </style>
# """
# st.markdown(chat_css, unsafe_allow_html=True)

# # -------------------------
# # Theme
# # -------------------------
# if "theme" not in st.session_state:
#     st.session_state.theme = "Light"

# with st.sidebar:
#     st.title("Settings")
#     theme_choice = st.radio("Theme", ["Light", "Dark"], index=0)
#     st.session_state.theme = theme_choice

# if st.session_state.theme == "Dark":
#     st.markdown(
#         "<style>body{background-color:#1e1e1e;color:white;} </style>", unsafe_allow_html=True
#     )
# else:
#     st.markdown(
#         "<style>body{background-color:white;color:black;} </style>", unsafe_allow_html=True
#     )

# # -------------------------
# # Session state for chat
# # -------------------------
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # -------------------------
# # Render chat messages
# # -------------------------
# def render_chat():
#     st.markdown('<div class="chat-container">', unsafe_allow_html=True)
#     for entry in reversed(st.session_state.chat_history):
#         role = entry["role"]
#         content = entry["content"]
#         st.markdown(
#             f'<div class="chat-message {role}">{content}</div>', unsafe_allow_html=True
#         )
#     st.markdown('</div>', unsafe_allow_html=True)

# # -------------------------
# # Process user query
# # -------------------------
# def process_query(user_query):
#     st.session_state.chat_history.append({"role": "user", "content": user_query})

#     with st.spinner("⏳ GPT is generating SQL and fetching results..."):
#         payload = {"user_prompt": user_query}
#         try:
#             resp = requests.post(API_URL, json=payload, timeout=30)
#             if resp.status_code != 200:
#                 bot_msg = f"❌ Error: {resp.json()}"
#             else:
#                 data = resp.json()
#                 sql_text = data.get("sql", "")
#                 rows = data.get("result", {}).get("rows", [])

#                 bot_msg = f"<b>Generated SQL:</b><br><pre>{sql_text}</pre>"
#                 if rows:
#                     df = pd.DataFrame(rows)
#                     bot_msg += f"<br><b>Result:</b> {len(df)} rows returned."
#                     # Store dataframe in session_state for charts panel
#                     st.session_state.last_df = df
#                 else:
#                     bot_msg += "<br><i>No records returned.</i>"
#         except Exception as e:
#             bot_msg = f"❌ Exception: {e}"

#     st.session_state.chat_history.append({"role": "bot", "content": bot_msg})

# # -------------------------
# # Main UI
# # -------------------------
# st.title("📊 Sales GPT — Chat with your sales data")

# render_chat()

# with st.form("query_form", clear_on_submit=True):
#     user_input = st.text_area("Type your question:", height=80)
#     submitted = st.form_submit_button("Send")
#     if submitted and user_input.strip():
#         process_query(user_input.strip())
#         render_chat()

# # -------------------------
# # Show charts in a separate panel
# # -------------------------
# if "last_df" in st.session_state:
#     df = st.session_state.last_df
#     st.subheader("📄 Result Data")
#     st.dataframe(df)

#     numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
#     if "created_at" in df.columns:
#         try:
#             df["created_at"] = pd.to_datetime(df["created_at"])
#             st.subheader("📈 Trend Chart")
#             st.line_chart(df.set_index("created_at")[numeric_cols])
#         except:
#             pass
#     elif len(numeric_cols) >= 1:
#         st.subheader("📊 Bar Chart")
#         st.bar_chart(df[numeric_cols[0]])
# import streamlit as st
# import pandas as pd
# import requests

# API_URL = "http://127.0.0.1:8000/api/query/"

# # -----------------------------
# # Remove Streamlit top padding
# # -----------------------------
# st.markdown("""
# <style>
# .block-container {padding-top:0.5rem !important; padding-bottom:0rem !important;}
# </style>
# """, unsafe_allow_html=True)

# # -----------------------------
# # ChatGPT-style CSS
# # -----------------------------
# st.markdown("""
# <style>
# .chat-wrapper { display:flex; flex-direction:column; min-height:300px; max-height:70vh; overflow:hidden; border-radius:12px; background:#f7f7f8; border:1px solid #ddd; box-shadow:0px 2px 8px rgba(0,0,0,0.08);}
# .chat-container { flex:1; padding:16px; overflow-y:auto; display:flex; flex-direction:column;}
# .message-row { display:flex; align-items:flex-start; gap:10px; margin:10px 0; animation:fadeIn 0.25s ease-in-out;}
# .message-row.user { justify-content:flex-end;}
# .avatar { width:36px; height:36px; border-radius:50%;}
# .message-bubble { padding:12px 16px; max-width:650px; border-radius:12px; line-height:1.4; font-size:1rem; white-space:pre-wrap;}
# .message-bubble.bot { background:#fff; border:1px solid #e0e0e0; color:black;}
# .message-bubble.user { background:#1e88e5; color:white;}
# .message-bubble pre { background:#222; color:#eee; padding:10px; border-radius:8px; overflow-x:auto;}
# .empty-message { text-align:center; color:#999; padding-top:20px; }
# .input-box { padding:14px; background:white; border-top:1px solid #ddd; }
# .chat-input { width:100%; padding:14px 18px; font-size:1rem; border-radius:24px; border:1px solid #ccc; outline:none;}
# .chat-input:focus { border-color:#1e88e5; box-shadow:0 0 0 2px rgba(30,136,229,0.2);}
# .typing-indicator { display:flex; gap:4px; }
# .typing-dot { width:6px; height:6px; background:#aaa; border-radius:50%; animation:blink 1.4s infinite both;}
# .typing-dot:nth-child(2) { animation-delay:0.2s; }
# .typing-dot:nth-child(3) { animation-delay:0.4s; }
# @keyframes blink { 0%{opacity:.2;}20%{opacity:1;}100%{opacity:.2;} }
# @keyframes fadeIn { from {opacity:0; transform:translateY(5px);} to {opacity:1; transform:translateY(0);} }
# </style>
# """, unsafe_allow_html=True)

# # -----------------------------
# # Session state initialization
# # -----------------------------
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# if "last_df" not in st.session_state:
#     st.session_state.last_df = None

# if "is_typing" not in st.session_state:
#     st.session_state.is_typing = False

# # -----------------------------
# # Main title
# # -----------------------------
# st.title("🤖 Sales GPT — Chat with Your Data")

# # -----------------------------
# # Chat rendering
# # -----------------------------
# st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
# st.markdown('<div id="chat-container" class="chat-container">', unsafe_allow_html=True)

# if len(st.session_state.chat_history) == 0:
#     st.markdown('<div class="empty-message">Start by asking a question…</div>', unsafe_allow_html=True)
# else:
#     for msg in st.session_state.chat_history:
#         if msg["role"] == "user":
#             avatar_html = '<img class="avatar user" src="https://cdn-icons-png.flaticon.com/512/847/847969.png">'
#             row_class = "message-row user"
#         else:
#             avatar_html = '<img class="avatar bot" src="https://cdn-icons-png.flaticon.com/512/4712/4712100.png">'
#             row_class = "message-row"

#         st.markdown(
#             f"""
#             <div class="{row_class}">
#                 {'<div class="message-bubble ' + msg['role'] + '">' + msg['content'] + '</div>' + avatar_html if msg['role']=="user" else avatar_html + '<div class="message-bubble ' + msg['role'] + '">' + msg['content'] + '</div>'}
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

# # Typing indicator
# if st.session_state.is_typing:
#     st.markdown("""
#         <div class="message-row">
#             <img class="avatar bot" src="https://cdn-icons-png.flaticon.com/512/4712/4712100.png">
#             <div class="message-bubble bot typing-indicator">
#                 <div class="typing-dot"></div>
#                 <div class="typing-dot"></div>
#                 <div class="typing-dot"></div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

# st.markdown('</div>', unsafe_allow_html=True)  # end chat-container

# # -----------------------------
# # Chart above input
# # -----------------------------
# if st.session_state.last_df is not None:
#     df = st.session_state.last_df
#     st.subheader("📊 Query Result Data / Charts")
#     st.dataframe(df, use_container_width=True)

#     numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
#     if "created_at" in df.columns:
#         try:
#             df["created_at"] = pd.to_datetime(df["created_at"])
#             st.line_chart(df.set_index("created_at")[numeric_cols])
#         except:
#             pass
#     elif numeric_cols:
#         st.bar_chart(df[numeric_cols[0]])

# # -----------------------------
# # Input bar at bottom
# # -----------------------------
# st.markdown('<div class="input-box">', unsafe_allow_html=True)

# def submit_question():
#     query = st.session_state.chat_input
#     if query.strip():
#         process_query(query.strip())
#         st.session_state.chat_input = ""  # safely clear input after sending

# st.text_input(
#     "Ask something...",
#     key="chat_input",
#     placeholder="Type your question here...",
#     label_visibility="collapsed",
#     on_change=submit_question
# )
# st.markdown('</div>', unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)  # end chat-wrapper

# # -----------------------------
# # Auto-scroll to bottom
# # -----------------------------
# st.markdown("""
# <script>
# const chatBox = document.getElementById("chat-container");
# if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;
# </script>
# """, unsafe_allow_html=True)

# # -----------------------------
# # Process user query
# # -----------------------------
# def process_query(user_query):
#     st.session_state.chat_history.append({"role": "user", "content": user_query})
#     st.session_state.is_typing = True

#     try:
#         resp = requests.post(API_URL, json={"user_prompt": user_query}, timeout=30)
#         data = resp.json() if resp.status_code == 200 else {}
#     except Exception as e:
#         st.session_state.chat_history.append({"role": "bot", "content": f"❌ Error: {str(e)}"})
#         st.session_state.is_typing = False
#         return

#     sql = data.get("sql", "")
#     rows = data.get("result", {}).get("rows", [])

#     bot_reply = f"<b>Generated SQL:</b><br><pre>{sql}</pre>"

#     if rows:
#         df = pd.DataFrame(rows)
#         st.session_state.last_df = df
#         bot_reply += f"<br><b>Rows Returned:</b> {len(df)}"
#     else:
#         bot_reply += "<br><i>No records returned.</i>"

#     st.session_state.chat_history.append({"role": "bot", "content": bot_reply})
#     st.session_state.is_typing = False




# import streamlit as st
# import pandas as pd
# import requests
# from datetime import datetime

# API_URL = "http://127.0.0.1:8000/api/query/"

# # -----------------------------
# # Session state initialization
# # -----------------------------
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# if "last_df" not in st.session_state:
#     st.session_state.last_df = None

# if "is_typing" not in st.session_state:
#     st.session_state.is_typing = False

# if "dark_mode" not in st.session_state:
#     st.session_state.dark_mode = False

# # -----------------------------
# # Sidebar Settings
# # -----------------------------
# st.sidebar.title("⚙️ Settings")
# st.session_state.dark_mode = st.sidebar.checkbox("Dark Mode", value=st.session_state.dark_mode)

# # -----------------------------
# # CSS
# # -----------------------------
# if st.session_state.dark_mode:
#     bg_color = "#1e1e1e"
#     bubble_user_bg = "#1565c0"
#     bubble_user_color = "#fff"
#     bubble_bot_bg = "#2c2c2c"
#     bubble_bot_color = "#fff"
#     page_bg = "#121212"
#     text_color = "#eee"
# else:
#     bg_color = "#f7f7f8"
#     bubble_user_bg = "#1e88e5"
#     bubble_user_color = "#fff"
#     bubble_bot_bg = "#fff"
#     bubble_bot_color = "#000"
#     page_bg = "#fff"
#     text_color = "#000"

# st.markdown(f"""
# <style>
# body {{ background-color: {page_bg}; color: {text_color}; }}
# .chat-wrapper {{ display:flex; flex-direction:column; min-height:300px; max-height:70vh; overflow:hidden; border-radius:12px; background:{bg_color}; border:1px solid #ddd; box-shadow:0px 2px 8px rgba(0,0,0,0.08);}}
# .chat-container {{ flex:1; padding:16px; overflow-y:auto; display:flex; flex-direction:column; }}
# .message-row {{ display:flex; align-items:flex-start; gap:10px; margin:10px 0; animation:fadeIn 0.25s ease-in-out; }}
# .message-row.user {{ justify-content:flex-end; }}
# .avatar {{ width:36px; height:36px; border-radius:50%; }}
# .message-bubble {{ padding:12px 16px; max-width:650px; border-radius:12px; line-height:1.4; font-size:1rem; white-space:pre-wrap; }}
# .message-bubble.bot {{ background:{bubble_bot_bg}; color:{bubble_bot_color}; border:1px solid #444; }}
# .message-bubble.user {{ background:{bubble_user_bg}; color:{bubble_user_color}; }}
# .message-bubble pre {{ background:#222; color:#eee; padding:10px; border-radius:8px; overflow-x:auto; }}
# .message-bubble pre.sql {{ background:#1e1e1e; color:#dcdcdc; }}
# .timestamp {{ font-size:0.7rem; color:#999; margin-top:4px; }}
# .empty-message {{ text-align:center; color:#999; padding-top:20px; }}
# .input-box {{ padding:14px; background:{page_bg}; border-top:1px solid #ddd; display:flex; gap:10px; }}
# .chat-input {{ flex:1; padding:14px 18px; font-size:1rem; border-radius:24px; border:1px solid #ccc; outline:none; }}
# .chat-input:focus {{ border-color:#1e88e5; box-shadow:0 0 0 2px rgba(30,136,229,0.2); }}
# .typing-indicator {{ display:flex; gap:4px; }}
# .typing-dot {{ width:6px; height:6px; background:#aaa; border-radius:50%; animation:blink 1.4s infinite both; }}
# .typing-dot:nth-child(2) {{ animation-delay:0.2s; }}
# .typing-dot:nth-child(3) {{ animation-delay:0.4s; }}
# @keyframes blink {{ 0%{{opacity:.2;}}20%{{opacity:1;}}100%{{opacity:.2;}} }}
# @keyframes fadeIn {{ from {{opacity:0; transform:translateY(5px);}} to {{opacity:1; transform:translateY(0);}} }}
# @media (max-width:768px) {{ .message-bubble {{ max-width:90%; font-size:0.9rem; }} }}
# </style>
# """, unsafe_allow_html=True)

# # -----------------------------
# # Title
# # -----------------------------
# st.title("🤖 Sales GPT — Chat with Your Data")

# # -----------------------------
# # Query processor
# # -----------------------------
# def process_query(user_query):
#     # Append user message
#     st.session_state.chat_history.append({
#         "role": "user",
#         "content": user_query,
#         "timestamp": datetime.now().strftime("%H:%M")
#     })
#     st.session_state.is_typing = True

#     try:
#         resp = requests.post(API_URL, json={"user_prompt": user_query}, timeout=30)
#         data = resp.json() if resp.status_code == 200 else {}
#     except Exception as e:
#         st.session_state.chat_history.append({
#             "role": "bot",
#             "content": f"❌ Error: {str(e)}",
#             "timestamp": datetime.now().strftime("%H:%M")
#         })
#         st.session_state.is_typing = False
#         return

#     sql = data.get("sql", "")
#     rows = data.get("result", {}).get("rows", [])

#     bot_reply = f"<b>Generated SQL:</b><br><details><summary>View SQL</summary><pre class='sql'>{sql}</pre></details>"

#     if rows:
#         df = pd.DataFrame(rows)
#         st.session_state.last_df = df
#         bot_reply += f"<br><b>Rows Returned:</b> {len(df)}"
#     else:
#         bot_reply += "<br><i>No records returned.</i>"

#     st.session_state.chat_history.append({
#         "role": "bot",
#         "content": bot_reply,
#         "timestamp": datetime.now().strftime("%H:%M")
#     })
#     st.session_state.is_typing = False

# # -----------------------------
# # Render chat
# # -----------------------------
# st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
# st.markdown('<div id="chat-container" class="chat-container">', unsafe_allow_html=True)

# if len(st.session_state.chat_history) == 0:
#     st.markdown('<div class="empty-message">Start by asking a question…</div>', unsafe_allow_html=True)
# else:
#     for msg in st.session_state.chat_history:
#         timestamp = msg.get("timestamp", "")
#         if msg["role"] == "user":
#             avatar_html = '<img class="avatar user" src="https://cdn-icons-png.flaticon.com/512/847/847969.png">'
#             row_class = "message-row user"
#             bubble_html = f'<div class="message-bubble user">{msg["content"]}<div class="timestamp">{timestamp}</div></div>'
#             st.markdown(f'<div class="{row_class}">{bubble_html}{avatar_html}</div>', unsafe_allow_html=True)
#         else:
#             avatar_html = '<img class="avatar bot" src="https://cdn-icons-png.flaticon.com/512/4712/4712100.png">'
#             row_class = "message-row"
#             bubble_html = f'<div class="message-bubble bot">{msg["content"]}<div class="timestamp">{timestamp}</div></div>'
#             st.markdown(f'<div class="{row_class}">{avatar_html}{bubble_html}</div>', unsafe_allow_html=True)

# # Typing indicator
# if st.session_state.is_typing:
#     st.markdown("""
#         <div class="message-row">
#             <img class="avatar bot" src="https://cdn-icons-png.flaticon.com/512/4712/4712100.png">
#             <div class="message-bubble bot typing-indicator">
#                 <div class="typing-dot"></div>
#                 <div class="typing-dot"></div>
#                 <div class="typing-dot"></div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

# st.markdown('</div>', unsafe_allow_html=True)  # end chat-container

# # -----------------------------
# # Data visualization
# # -----------------------------
# if st.session_state.last_df is not None:
#     df = st.session_state.last_df
#     st.subheader("📊 Query Result Data / Charts")
#     st.dataframe(df, width="stretch")  # replaces deprecated use_container_width

#     numeric_cols = df.select_dtypes(include="number").columns.tolist()
#     chart_type = st.selectbox("Select chart type", ["Line", "Bar", "Area"])

#     if numeric_cols:
#         if "created_at" in df.columns:
#             try:
#                 df["created_at"] = pd.to_datetime(df["created_at"])
#                 df_plot = df.set_index("created_at")[numeric_cols]
#             except:
#                 df_plot = df[numeric_cols]
#         else:
#             df_plot = df[numeric_cols]

#         if chart_type == "Line":
#             st.line_chart(df_plot)
#         elif chart_type == "Bar":
#             st.bar_chart(df_plot)
#         elif chart_type == "Area":
#             st.area_chart(df_plot)

#     st.download_button("📥 Download CSV", df.to_csv(index=False), "data.csv")

# # -----------------------------
# # Input box
# # -----------------------------
# st.markdown('<div class="input-box">', unsafe_allow_html=True)

# def submit_question():
#     query = st.session_state.chat_input.strip()
#     if query:
#         process_query(query)
#         st.session_state.chat_input = ""

# st.text_area(
#     "Ask something...",
#     key="chat_input",
#     placeholder="Type your question here...",
#     label_visibility="collapsed",
#     height=80
# )
# st.button("Send", on_click=submit_question)
# st.markdown('</div>', unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)  # end chat-wrapper

# # -----------------------------
# # Auto-scroll JS
# # -----------------------------
# st.markdown("""
# <script>
# const chatBox = document.getElementById("chat-container");
# if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;
# </script>
# """, unsafe_allow_html=True)





# import streamlit as st
# import pandas as pd
# import requests
# from datetime import datetime
# import os
# import json
# import uuid
# from streamlit_cookies_manager import EncryptedCookieManager

# API_URL = "http://127.0.0.1:8000/api/query/"
# REFRESH_URL = "http://127.0.0.1:8000/api/token/refresh/"

# authenticated = st.session_state.get("authenticated", False)
# if not authenticated:
#     st.switch_page("pages/login.py")
    
# # if "token" not in st.session_state or st.session_state.token is None:
# #     st.switch_page("pages/login.py")



# # -----------------------------
# # Cookies for persistent user ID
# # -----------------------------
# cookies = EncryptedCookieManager(
#     prefix="sales_gpt_",
#     password="YOUR_SECRET_PASSWORD_32CHARS"  # Must be 32 chars
# )

# if not cookies.ready():
#     st.stop()  # Wait for cookies to load

# access = cookies.get("access")
# refresh = cookies.get("refresh")
# username = cookies.get("username")

# print(access, refresh, username)

# def refresh_access_token():
#     """Auto-refresh expired access token using refresh token."""
#     global access

#     if not refresh:
#         return False

#     resp = requests.post(REFRESH_URL, json={"refresh": refresh})
#     if resp.status_code == 200:
#         new_access = resp.json()["access"]
#         cookies["access"] = new_access
#         cookies.save()
#         access = new_access
#         return True

#     return False


# # -----------------------------
# # Session state initialization
# # -----------------------------
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# if "last_df" not in st.session_state:
#     st.session_state.last_df = None

# if "is_typing" not in st.session_state:
#     st.session_state.is_typing = False

# if "dark_mode" not in st.session_state:
#     st.session_state.dark_mode = False

#  # Initialize token


# # -----------------------------
# # Load previous chat from disk
# # -----------------------------
# CHAT_DIR = "chat_data"
# os.makedirs(CHAT_DIR, exist_ok=True)

# # Persistent user ID
# if "user_id" not in cookies:
#     cookies["user_id"] = str(uuid.uuid4())
#     cookies.save()

# user_id = cookies["user_id"]

# chat_file = os.path.join(CHAT_DIR, f"{user_id}.json")

# # Load chat history
# if os.path.exists(chat_file):
#     with open(chat_file, "r") as f:
#         st.session_state.chat_history = json.load(f)
# else:
#     st.session_state.chat_history = []

# def save_chat():
#     with open(chat_file, "w") as f:
#         json.dump(st.session_state.chat_history, f)

# # -----------------------------
# # Sidebar Settings
# # -----------------------------
# st.sidebar.title("⚙️ Settings")
# st.session_state.dark_mode = st.sidebar.checkbox("Dark Mode", value=st.session_state.dark_mode)

# # -----------------------------
# # CSS
# # -----------------------------
# if st.session_state.dark_mode:
#     bg_color = "#1e1e1e"
#     bubble_user_bg = "#1565c0"
#     bubble_user_color = "#fff"
#     bubble_bot_bg = "#2c2c2c"
#     bubble_bot_color = "#fff"
#     page_bg = "#121212"
#     text_color = "#eee"
# else:
#     bg_color = "#f7f7f8"
#     bubble_user_bg = "#1e88e5"
#     bubble_user_color = "#fff"
#     bubble_bot_bg = "#fff"
#     bubble_bot_color = "#000"
#     page_bg = "#fff"
#     text_color = "#000"

# st.markdown(f"""
# <style>
# body {{ background-color: {page_bg}; color: {text_color}; }}
# .chat-wrapper {{ display:flex; flex-direction:column; min-height:300px; max-height:70vh; overflow:hidden; border-radius:12px; background:{bg_color}; border:1px solid #ddd; box-shadow:0px 2px 8px rgba(0,0,0,0.08);}}
# .chat-container {{ flex:1; padding:16px; overflow-y:auto; display:flex; flex-direction:column; }}
# .message-row {{ display:flex; align-items:flex-start; gap:10px; margin:10px 0; animation:fadeIn 0.25s ease-in-out; }}
# .message-row.user {{ justify-content:flex-end; }}
# .avatar {{ width:36px; height:36px; border-radius:50%; }}
# .message-bubble {{ padding:12px 16px; max-width:650px; border-radius:12px; line-height:1.4; font-size:1rem; white-space:pre-wrap; }}
# .message-bubble.bot {{ background:{bubble_bot_bg}; color:{bubble_bot_color}; border:1px solid #444; }}
# .message-bubble.user {{ background:{bubble_user_bg}; color:{bubble_user_color}; }}
# .message-bubble pre {{ background:#222; color:#eee; padding:10px; border-radius:8px; overflow-x:auto; }}
# .message-bubble pre.sql {{ background:#1e1e1e; color:#dcdcdc; }}
# .timestamp {{ font-size:0.7rem; color:#999; margin-top:4px; }}
# .empty-message {{ text-align:center; color:#999; padding-top:20px; }}
# .input-box {{ padding:14px; background:{page_bg}; border-top:1px solid #ddd; display:flex; gap:10px; }}
# .chat-input {{ flex:1; padding:14px 18px; font-size:1rem; border-radius:24px; border:1px solid #ccc; outline:none; }}
# .chat-input:focus {{ border-color:#1e88e5; box-shadow:0 0 0 2px rgba(30,136,229,0.2); }}
# .typing-indicator {{ display:flex; gap:4px; }}
# .typing-dot {{ width:6px; height:6px; background:#aaa; border-radius:50%; animation:blink 1.4s infinite both; }}
# .typing-dot:nth-child(2) {{ animation-delay:0.2s; }}
# .typing-dot:nth-child(3) {{ animation-delay:0.4s; }}
# @keyframes blink {{ 0%{{opacity:.2;}}20%{{opacity:1;}}100%{{opacity:.2;}} }}
# @keyframes fadeIn {{ from {{opacity:0; transform:translateY(5px);}} to {{opacity:1; transform:translateY(0);}} }}
# @media (max-width:768px) {{ .message-bubble {{ max-width:90%; font-size:0.9rem; }} }}
# </style>
# """, unsafe_allow_html=True)

# # -----------------------------
# # Title
# # -----------------------------
# st.title("🤖 Sales GPT — Chat with Your Data")

# # -----------------------------
# # Process user query

# def process_query(user_query):
#     global access

#     # Save user message
#     st.session_state.chat_history.append({
#         "role": "user",
#         "content": user_query,
#         "timestamp": datetime.now().strftime("%H:%M")
#     })
#     save_chat()
#     st.session_state.is_typing = True

#     headers = {"Authorization": f"Bearer {access}"}

#     resp = requests.post(API_URL, json={"user_prompt": user_query}, headers=headers)

#     # If access token expired → refresh + retry
#     if resp.status_code == 401:
#         if refresh_access_token():
#             headers = {"Authorization": f"Bearer {cookies.get('access')}"}
#             resp = requests.post(API_URL, json={"user_prompt": user_query}, headers=headers)
#         else:
#             st.error("Session expired. Please log in again.")
#             cookies["access"] = ""
#             cookies["refresh"] = ""
#             cookies.save()
#             st.switch_page("login.py")
#             return

#     data = resp.json()

#     sql = data.get("sql", "")
#     rows = data.get("result", {}).get("rows", [])

#     bot_msg = f"<b>Generated SQL:</b><br><details><summary>View SQL</summary><pre>{sql}</pre></details>"

#     if rows:
#         df = pd.DataFrame(rows)
#         st.session_state.last_df = df
#         bot_msg += f"<br><b>{len(df)} rows returned.</b>"
#     else:
#         bot_msg += "<br><i>No data returned.</i>"

#     st.session_state.chat_history.append({
#         "role": "bot",
#         "content": bot_msg,
#         "timestamp": datetime.now().strftime("%H:%M")
#     })
#     save_chat()
#     st.session_state.is_typing = False



# # -----------------------------
# # def process_query(user_query):
# #     st.session_state.chat_history.append({
# #         "role": "user",
# #         "content": user_query,
# #         "timestamp": datetime.now().strftime("%H:%M")
# #     })
# #     st.session_state.is_typing = True
# #     save_chat()  # save user message immediately
# #     headers = {"Authorization": f"Bearer {st.session_state.token}"}

# #     try:
# #         resp = requests.post(API_URL, json={"user_prompt": user_query}, headers=headers, timeout=30)
# #         data = resp.json() if resp.status_code == 200 else {}
# #     except Exception as e:
# #         st.session_state.chat_history.append({
# #             "role": "bot",
# #             "content": f"❌ Error: {str(e)}",
# #             "timestamp": datetime.now().strftime("%H:%M")
# #         })
# #         st.session_state.is_typing = False
# #         save_chat()
# #         return

# #     sql = data.get("sql", "")
# #     rows = data.get("result", {}).get("rows", [])

# #     bot_reply = f"<b>Generated SQL:</b><br><details><summary>View SQL</summary><pre class='sql'>{sql}</pre></details>"

# #     if rows:
# #         df = pd.DataFrame(rows)
# #         st.session_state.last_df = df
# #         bot_reply += f"<br><b>Rows Returned:</b> {len(df)}"
# #     else:
# #         bot_reply += "<br><i>No records returned.</i>"

# #     st.session_state.chat_history.append({
# #         "role": "bot",
# #         "content": bot_reply,
# #         "timestamp": datetime.now().strftime("%H:%M")
# #     })
# #     st.session_state.is_typing = False
# #     save_chat()

# # -----------------------------
# # Render chat
# # -----------------------------
# st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
# st.markdown('<div id="chat-container" class="chat-container">', unsafe_allow_html=True)

# if len(st.session_state.chat_history) == 0:
#     st.markdown('<div class="empty-message">Start by asking a question…</div>', unsafe_allow_html=True)
# else:
#     for msg in st.session_state.chat_history:
#         timestamp = msg.get("timestamp", "")
#         if msg["role"] == "user":
#             avatar_html = '<img class="avatar user" src="https://cdn-icons-png.flaticon.com/512/847/847969.png">'
#             row_class = "message-row user"
#             bubble_html = f'<div class="message-bubble user">{msg["content"]}<div class="timestamp">{timestamp}</div></div>'
#             st.markdown(f'<div class="{row_class}">{bubble_html}{avatar_html}</div>', unsafe_allow_html=True)
#         else:
#             avatar_html = '<img class="avatar bot" src="https://cdn-icons-png.flaticon.com/512/4712/4712100.png">'
#             row_class = "message-row"
#             bubble_html = f'<div class="message-bubble bot">{msg["content"]}<div class="timestamp">{timestamp}</div></div>'
#             st.markdown(f'<div class="{row_class}">{avatar_html}{bubble_html}</div>', unsafe_allow_html=True)

# # Typing indicator
# if st.session_state.is_typing:
#     st.markdown("""
#         <div class="message-row">
#             <img class="avatar bot" src="https://cdn-icons-png.flaticon.com/512/4712/4712100.png">
#             <div class="message-bubble bot typing-indicator">
#                 <div class="typing-dot"></div>
#                 <div class="typing-dot"></div>
#                 <div class="typing-dot"></div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

# st.markdown('</div>', unsafe_allow_html=True)  # end chat-container

# # -----------------------------
# # Data visualization
# # -----------------------------
# if st.session_state.last_df is not None:
#     df = st.session_state.last_df
#     st.subheader("📊 Query Result Data / Charts")
#     st.dataframe(df, width="stretch")  # full width

#     numeric_cols = df.select_dtypes(include="number").columns.tolist()
#     chart_type = st.selectbox("Select chart type", ["Line", "Bar", "Area"])

#     if numeric_cols:
#         if "created_at" in df.columns:
#             try:
#                 df["created_at"] = pd.to_datetime(df["created_at"])
#                 df_plot = df.set_index("created_at")[numeric_cols]
#             except:
#                 df_plot = df[numeric_cols]
#         else:
#             df_plot = df[numeric_cols]

#         if chart_type == "Line":
#             st.line_chart(df_plot)
#         elif chart_type == "Bar":
#             st.bar_chart(df_plot)
#         elif chart_type == "Area":
#             st.area_chart(df_plot)

#     st.download_button("📥 Download CSV", df.to_csv(index=False), "data.csv")

# # -----------------------------
# # Input box
# # -----------------------------
# st.markdown('<div class="input-box">', unsafe_allow_html=True)

# def submit_question():
#     query = st.session_state.chat_input.strip()
#     if query:
#         process_query(query)
#         st.session_state.chat_input = ""

# st.text_area(
#     "Ask something...",
#     key="chat_input",
#     placeholder="Type your question here...",
#     label_visibility="collapsed",
#     height=80
# )
# st.button("Send", on_click=submit_question)
# st.markdown('</div>', unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)  # end chat-wrapper

# # -----------------------------
# # Auto-scroll JS
# # -----------------------------
# st.markdown("""
# <script>
# const chatBox = document.getElementById("chat-container");
# if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;
# </script>
# """, unsafe_allow_html=True)


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
