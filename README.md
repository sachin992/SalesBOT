📄 Sales GPT — Streamlit Application

An AI-powered SQL generation and data exploration tool with authentication, chat history, secure cookies, and interactive visualizations.

🚀 Overview

Sales GPT is an intelligent chat-based analytics tool built using Streamlit, Django REST API, and JWT-based authentication.
Users can type natural language questions, and the app generates SQL, fetches data from the backend API, and displays results with interactive charts.

This project supports:

✔ Secure Login / Registration
✔ JWT Access + Refresh Tokens
✔ Encrypted Cookies
✔ Persistent Chat History (per user)
✔ SQL Generation (via backend API)
✔ Query Execution + Table Display
✔ Advanced Charts (Line, Bar, Area)
✔ Dark Mode UI
✔ Beautiful Chat UI with animations
✔ CSV Downloading

🏗️ Project Structure
project/
│
├── chat_data/                # Stores per-user chat history (JSON files)
├── pages/
│   ├── login.py              # Login/Registration page
│   ├── chat.py               # Main Sales GPT chat interface
│
└── README.md                 # Documentation

🔧 Tech Stack
Frontend

Streamlit

Pandas

Requests

EncryptedCookieManager

Custom HTML + CSS for chat UI

Streamlit Charts (Line, Bar, Area)

Backend

Django REST Framework (DRF)

API Endpoints:

/api/login/ — Login + Issue JWT

/api/register/ — Create account

/api/token/refresh/ — Refresh access token

/api/query/ — Generate SQL + execute database query

🔐 Authentication Flow

User logs in → Receives access + refresh tokens

Tokens stored in encrypted cookies (EncryptedCookieManager)

Access token is attached in every API request

If access token expires → Backend returns 401

App auto-refreshes token using refresh token

If refresh token is invalid → Redirect to Login

💾 Chat Persistence

Each user gets a UUID stored in cookies:

sales_gpt_user_id = <unique-id>


Chat history is saved in:

chat_data/<user-id>.json


This allows persistent chat history even after page refresh.

💬 Features Explained
1. Chat Interface

Modern chat bubble design

Fade-in animations & typing indicator

Both user and bot messages preserved

Supports SQL output via <details> block

2. SQL Generation

Backend returns:

{
  "sql": "SELECT * FROM sales WHERE date > '2023-01-01'",
  "result": { "rows": [...] }
}


App displays formatted SQL + results.

3. Data Visualization

Once a dataframe is returned:

Table view (st.dataframe)

Auto-detect numeric columns

Supports:

Line Chart

Bar Chart

Area Chart

CSV Export

⚙️ Environment Variables

Update inside your Streamlit code:

API_URL = "http://127.0.0.1:8000/api/"
REFRESH_URL = "http://127.0.0.1:8000/api/token/refresh/"


Change to production when deploying.

🧪 Running Locally
1️⃣ Install Dependencies
pip install streamlit pandas requests python-dotenv streamlit-cookies-manager

2️⃣ Start Django Backend
python manage.py runserver


Backend will run at:

http://127.0.0.1:8000/

3️⃣ Start Streamlit Frontend
streamlit run pages/login.py

🛡️ Security Notes

Use a 32-character secret key for cookies:

password="your_very_long_secure_key_32_chars"


Do not commit chat history files to GitHub

Always use HTTPS in production
