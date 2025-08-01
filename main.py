import streamlit as st
from Crypto.Cipher import AES
import base64
import os
import json
from datetime import datetime

# === CONFIGURATION ===
ENCRYPT_FOLDER = os.path.join(os.path.expanduser("~"), "Desktop", "project", "exam_questions")
USER_CREDENTIALS_FILE = os.path.join(ENCRYPT_FOLDER, "users.json")
METADATA_FILE = os.path.join(ENCRYPT_FOLDER, "metadata.json")

os.makedirs(ENCRYPT_FOLDER, exist_ok=True)

# === UTILITY FUNCTIONS ===
def pad(text):
    pad_len = 16 - len(text.encode('utf-8')) % 16
    return text + chr(pad_len) * pad_len

def encrypt(text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = pad(text)
    encrypted = cipher.encrypt(padded_text.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def save_encrypted_file(content, subject, course_code, lecturer):
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{subject}_{course_code}_{now}.enc"
    filepath = os.path.join(ENCRYPT_FOLDER, filename)

    with open(filepath, "w") as f:
        f.write(content)

    metadata = {}
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            metadata = json.load(f)

    metadata[filename] = {
        "subject": subject,
        "course_code": course_code,
        "lecturer": lecturer,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=4)

    return filename

def load_users():
    if os.path.exists(USER_CREDENTIALS_FILE):
        with open(USER_CREDENTIALS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_CREDENTIALS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# === PAGE CONFIGURATION ===
st.set_page_config(page_title="Question Encryption System", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #004080;
            color: white;
        }
        .stTextInput>div>div>input,
        .stTextArea>div>textarea {
            background-color: white !important;
            color: black !important;
        }
        .stButton>button {
            color: black !important;
            background-color: #87CEFA !important;
        }
        .success-message {
            color: white !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# === AUTHENTICATION ===
if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False

users = load_users()

def register():
    st.subheader("📝 Register")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Register"):
        if new_password != confirm_password:
            st.error("❌ Passwords do not match.")
        elif new_username in users:
            st.error("❌ Username already exists.")
        else:
            users[new_username] = new_password
            save_users(users)
            st.success("✅ Registration successful! Please login.")

def login():
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.user_logged_in = True
            st.session_state.username = username
            st.success("✅ Login successful!")
        else:
            st.error("❌ Invalid username or password.")

# === ROUTING ===
menu = st.sidebar.selectbox("Select Option", ["Login", "Register"] if not st.session_state.user_logged_in else ["Encrypt Question", "Logout"])

if not st.session_state.user_logged_in:
    if menu == "Login":
        login()
    elif menu == "Register":
        register()
else:
    if menu == "Logout":
        st.session_state.user_logged_in = False
        st.experimental_rerun()
    elif menu == "Encrypt Question":
        st.title("🔐 Exam Question Encryption")

        subject = st.text_input("Subject")
        course_code = st.text_input("Course Code")
        lecturer = st.text_input("Lecturer Name")
        question_text = st.text_area("Enter Examination Question(s)", height=200)
        custom_key = st.text_input("Enter 16-character Encryption Key")

        if st.button("Encrypt and Save"):
            if not all([subject, course_code, lecturer, question_text, custom_key]):
                st.error("❗ All fields including encryption key are required.")
            elif len(custom_key.encode('utf-8')) != 16:
                st.error("❗ Encryption key must be exactly 16 bytes (characters) for AES-128.")
            else:
                encrypted = encrypt(question_text, custom_key.encode('utf-8'))
                filename = save_encrypted_file(encrypted, subject, course_code, lecturer)
                st.success(f"✅ Encrypted and saved as: {filename}")
                with open(os.path.join(ENCRYPT_FOLDER, filename), "rb") as f:
                    st.download_button(
                        label="⬇️ Download Encrypted File",
                        data=f,
                        file_name=filename,
                        mime="text/plain"
                    )
