import streamlit as st
import json
import os
import hashlib

# === PATH CONFIG ===
USER_DB = os.path.join(os.path.expanduser("~"), "Desktop", "project", "users.json")
os.makedirs(os.path.dirname(USER_DB), exist_ok=True)

# === HELPER FUNCTIONS ===
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

def username_exists(username):
    users = load_users()
    return username in users

# === STREAMLIT UI ===
st.set_page_config(page_title="User Registration", layout="centered")
st.title("📝 Register New User")

with st.form("register_form"):
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    submitted = st.form_submit_button("Register")

    if submitted:
        if not username or not password or not confirm:
            st.warning("⚠️ Please fill in all fields.")
        elif password != confirm:
            st.error("❌ Passwords do not match.")
        elif username_exists(username):
            st.error("🚫 Username already exists. Choose another.")
        else:
            users = load_users()
            users[username] = hash_password(password)
            save_users(users)
            st.success("✅ Registration successful! You can now log in.")
