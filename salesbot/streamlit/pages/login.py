# import streamlit as st
# import requests
# from streamlit_cookies_manager import EncryptedCookieManager

# API_URL = "http://127.0.0.1:8000/api/"



# cookies = EncryptedCookieManager(
#     prefix="sales_gpt_",
#     password="VERY_SECRET_KEY_32_CHARS_LONG!!"
# )
# if not cookies.ready():
#     st.stop()



# # -----------------------------
# # Page Config
# # -----------------------------
# st.set_page_config(
#     page_title="Sales GPT - Login",
#     page_icon="🔐",
#     layout="centered",
# )

# # -----------------------------
# # CSS for styling
# # -----------------------------
# st.markdown("""
# <style>
# /* Center the card */
# .login-card {
#     max-width: 450px;
#     margin: 80px auto;
#     padding: 40px;
#     border-radius: 12px;
#     background-color: #fff;
#     box-shadow: 0 10px 25px rgba(0,0,0,0.1);
# }

# /* Inputs */
# .login-card input {
#     height: 45px;
#     padding: 10px;
#     border-radius: 8px;
#     border: 1px solid #ddd;
#     width: 100%;
#     margin-bottom: 20px;
# }

# /* Buttons */
# .login-card button {
#     width: 48%;
#     height: 45px;
#     border-radius: 8px;
#     border: none;
#     font-weight: bold;
#     cursor: pointer;
#     transition: all 0.2s;
# }

# .login-btn {
#     background-color: #1e88e5;
#     color: white;
# }
# .login-btn:hover {
#     background-color: #1565c0;
# }

# .register-btn {
#     background-color: #e0e0e0;
# }
# .register-btn:hover {
#     background-color: #bdbdbd;
# }

# /* Title */
# .login-title {
#     text-align: center;
#     font-size: 1.8rem;
#     font-weight: bold;
#     margin-bottom: 30px;
#     color: #1565c0;
# }
# </style>
# """, unsafe_allow_html=True)

# # -----------------------------
# # Login card
# # -----------------------------
# st.markdown('<div class="login-card">', unsafe_allow_html=True)
# st.markdown('<div class="login-title">Sales GPT Login</div>', unsafe_allow_html=True)

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
     

# if "token" not in st.session_state:
#     st.session_state.token = None  # Initialize token


# username = st.text_input("Username", key="login_username")
# password = st.text_input("Password", type="password", key="login_password")

# col1, col2 = st.columns(2)

# with col1:
#     if st.button("Login", key="login_btn"):
#         if username and password:
#             try:
#                 resp = requests.post(f"{API_URL}login/", json={"username": username, "password": password})
#                 data = resp.json()
#                 print(data)
#                 if resp.status_code == 200:
#                     cookies["access"] = data.get("access")
#                     cookies["refresh"] = data.get("refresh")
#                     cookies["username"] = data.get("username")
#                     cookies.save()
#                     print(cookies["access "])
#                     print(cookies["refresh"])
#                     print(cookies["username"])
#                     st.session_state.authenticated = True
#                     st.success("✅ Login successful! Redirecting…")
#                     st.session_state.token = data.get("access")  # Store JWT token
#                     st.session_state.username = data.get("username")
#                     print("Logged in as:", st.session_state.username)
#                     print("Token:", st.session_state.token)
                    
#                     # Redirect to chat page using new st.query_params
#                     st.switch_page("pages/chat.py")
#                 else:
#                     st.error(data.get("detail", "Login failed"))
#             except Exception as e:
#                 st.error(f"❌ Error: {str(e)}")
#         else:
#             st.warning("⚠️ Please enter both username and password.")

# with col2:
#     if st.button("Register", key="register_btn"):
#         if username and password:
#             try:
#                 resp = requests.post(f"{API_URL}register/", json={"username": username, "password": password})
#                 data = resp.json()
#                 if resp.status_code == 201:
#                     st.success("✅ Registration successful! You can now log in.")
#                 else:
#                     st.error(data.get("detail", "Registration failed"))
#             except Exception as e:
#                 st.error(f"❌ Error: {str(e)}")
#         else:
#             st.warning("⚠️ Please enter both username and password.")

# st.markdown('</div>', unsafe_allow_html=True)
import streamlit as st
import requests
from streamlit_cookies_manager import EncryptedCookieManager

API_URL = "http://127.0.0.1:8000/api/"

# -----------------------------
# Cookies Setup
# -----------------------------
cookies = EncryptedCookieManager(
    prefix="sales_gpt_",
    password="VERY_SECRET_KEY_32_CHARS_LONG!!"
)

if not cookies.ready():
    st.stop()

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Sales GPT - Login",
    page_icon="🔐",
    layout="centered",
)

# -----------------------------
# CSS Styling
# -----------------------------
st.markdown("""
<style>
.login-card {
    max-width: 450px;
    margin: 80px auto;
    padding: 40px;
    border-radius: 12px;
    background-color: #fff;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}
.login-card input {
    height: 45px;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ddd;
    width: 100%;
    margin-bottom: 20px;
}
.login-card button {
    width: 48%;
    height: 45px;
    border-radius: 8px;
    border: none;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s;
}
.login-btn {
    background-color: #1e88e5;
    color: white;
}
.login-btn:hover {
    background-color: #1565c0;
}
.register-btn {
    background-color: #e0e0e0;
}
.register-btn:hover {
    background-color: #bdbdbd;
}
.login-title {
    text-align: center;
    font-size: 1.8rem;
    font-weight: bold;
    margin-bottom: 30px;
    color: #1565c0;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Login Session Management
# -----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "token" not in st.session_state:
    st.session_state.token = None

# -----------------------------
# Login Card UI
# -----------------------------
st.markdown('<div class="login-card">', unsafe_allow_html=True)
st.markdown('<div class="login-title">Sales GPT Login</div>', unsafe_allow_html=True)

username = st.text_input("Username", key="login_username")
password = st.text_input("Password", type="password", key="login_password")

col1, col2 = st.columns(2)

# -----------------------------
# Login Button
# -----------------------------
with col1:
    if st.button("Login", key="login_btn"):
        if username and password:
            try:
                resp = requests.post(f"{API_URL}login/", json={
                    "username": username,
                    "password": password
                })
                data = resp.json()
                print(data)
                if resp.status_code == 200:
                    cookies["access"] = data.get("access")
                    cookies["refresh"] = data.get("refresh")
                    cookies["username"] = data.get("username")
                    cookies.save()

                    st.session_state.authenticated = True
                    st.session_state.token = data.get("access")
                    st.session_state.username = data.get("username")

                    st.success("✅ Login successful! Redirecting…")

                    st.switch_page("pages/chat.py")

                else:
                    st.error(data.get("detail", "Login failed"))

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

        else:
            st.warning("⚠️ Please enter both username and password.")

# -----------------------------
# Register Button
# -----------------------------
with col2:
    if st.button("Register", key="register_btn"):
        if username and password:
            try:
                resp = requests.post(f"{API_URL}register/", json={
                    "username": username,
                    "password": password
                })
                data = resp.json()

                if resp.status_code == 201:
                    st.success("✅ Registration successful! You can now log in.")
                else:
                    st.error(data.get("detail", "Registration failed"))

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

        else:
            st.warning("⚠️ Please enter both username and password.")

st.markdown('</div>', unsafe_allow_html=True)
