import streamlit as st
import os
import json
from decrypt_utils import decrypt_question
from datetime import datetime
from docx import Document
import io


# === CONFIGURATION ===
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"  # Change this securely in real use
ENCRYPT_FOLDER = os.path.join(os.path.expanduser("~"), "Desktop", "project", "exam_questions")
METADATA_FILE = os.path.join(ENCRYPT_FOLDER, "metadata.json")
os.makedirs(ENCRYPT_FOLDER, exist_ok=True)

# === STYLING ===
st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.markdown("""
    <style>
        .main { background-color: #003366; color: white; }
        .stTextInput > div > input,
        .stPassword > div > input,
        .stTextArea > div > textarea {
            background-color: white; color: black;
        }
        .stButton > button {
            color: black !important; background-color: #66b3ff !important;
        }
        .success-text {
            color: white;
            font-weight: bold;
            background-color: green;
            padding: 8px;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# === HELPERS ===
def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_metadata(metadata):
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=4)

def authenticate(username, password):
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

# === LOGIN ===
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.title("🔐 Admin Login")
    with st.form("admin_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted and authenticate(username, password):
            st.session_state.admin_logged_in = True
            st.success("✅ Logged in successfully")
        elif submitted:
            st.error("❌ Invalid credentials")
    st.stop()

# === LOGOUT BUTTON ===
st.sidebar.button("🚪 Logout", on_click=lambda: st.session_state.update(admin_logged_in=False))

# === MAIN DASHBOARD ===
st.title("📁 Encrypted Exam Files Dashboard")
metadata = load_metadata()
files = [f for f in os.listdir(ENCRYPT_FOLDER) if f.endswith(".enc")]

if not files:
    st.info("No encrypted files available.")
else:
    selected_file = st.selectbox("📂 Select Encrypted File", files)
    file_path = os.path.join(ENCRYPT_FOLDER, selected_file)

    # Show metadata if available
    if selected_file in metadata:
        st.markdown("### 🗂️ File Metadata")
        meta = metadata[selected_file]
        st.write(f"📘 Subject: **{meta.get('subject', 'N/A')}**")
        st.write(f"📙 Course Code: **{meta.get('course_code', 'N/A')}**")
        st.write(f"👨‍🏫 Lecturer: **{meta.get('lecturer', 'N/A')}**")
        st.write(f"🕒 Saved At: **{meta.get('saved_at', 'N/A')}**")

    # Show encrypted content preview
    with open(file_path, "r") as f:
        encrypted_content = f.read()

    st.markdown("### 🔒 Encrypted Content (Preview)")
    st.code(encrypted_content[:300] + "..." if len(encrypted_content) > 300 else encrypted_content)

    # === DECRYPTION SECTION ===
    st.markdown("---")
    st.markdown("### 🔓 Decrypt File")
    key = st.text_input("🔑 Enter Decryption Key", type="password")
    if st.button("Decrypt"):
        decrypted = decrypt_question(encrypted_content, key)
        if decrypted.startswith("Decryption failed"):
            st.error(f"❌ {decrypted}")
        else:
            st.success("✅ File Decrypted Successfully!")
            st.text_area("📄 Decrypted Content", decrypted, height=250)

            filename = selected_file.replace(".enc", "_decrypted.txt")
            st.download_button("⬇️ Download Decrypted File", decrypted, file_name=filename)

    # === FILE DELETION SECTION ===
    st.markdown("---")
    st.markdown("### 🗑️ Delete File")
    confirm_delete = st.checkbox("Yes, I really want to delete this file")
    if st.button("Delete File", type="primary"):
        if confirm_delete:
            try:
                os.remove(file_path)
                if selected_file in metadata:
                    del metadata[selected_file]
                    save_metadata(metadata)
                st.success(f"✅ File '{selected_file}' has been deleted.")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error deleting file: {e}")
        else:
            st.warning("⚠️ Please confirm deletion by checking the box.")
