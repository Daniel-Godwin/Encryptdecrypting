# 🔐 Symmetric-Key Encryption System (Streamlit App)

This is a mini-project built with **Python** and **Streamlit** to demonstrate secure encryption for exam data protection.  
The application allows users (students or admins) to register, log in, upload exam question papers, and encrypt them using a symmetric key. The encrypted file can then be downloaded securely.

🌐 Live Demo: [EncryptDecryptingMe Streamlit App](https://encryptdecryptingme.streamlit.app/)

## 📖 Features
- **User & Admin Registration/Login**  
  Secure authentication system for different roles.
- **Upload Question Papers**  
  Include subject name and course code metadata.
- **Generate Encryption Key**  
  Symmetric key creation for secure encryption.
- **Encrypt & Save**  
  One-click encryption of uploaded files.
- **Download Encrypted File**  
  Download button provided for easy access to encrypted data.


## 🎯 Project Goals
- Build a secure encryption system for exam data protection.  
- Apply cryptographic techniques for secure communication.  
- Ensure confidentiality and integrity of exam-related files.  

## 🛠️ Technologies Used
- **Python**  
- **Streamlit** (for web interface)  
- **Cryptography libraries** (for symmetric-key encryption)  

## 🚀 How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/encryption-streamlit-app.git
   cd encryption-streamlit-app
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
4. Open the local URL provided in your terminal.

## 📌 Impact
- Ensures secure communication and data confidentiality.  
- Protects sensitive exam data from unauthorized access.  
- Demonstrates practical application of symmetric-key cryptography.  

## 🖥️ Usage Example
Here’s how a typical workflow looks:

1. **Register/Login**  
   - Create a new account as a user or admin.  
   - Log in to access the dashboard.  

2. **Upload Question Paper**  
   - Select a file (e.g., PDF or DOCX).  
   - Enter subject name and course code.  

3. **Generate Encryption Key**  
   - Click the "Create Key" button.  
   - A symmetric key is generated for encryption.  

4. **Encrypt File**  
   - Press the "Encrypt" button.  
   - The system encrypts the uploaded file using the generated key.  

5. **Download Encrypted File**  
   - A download button appears.  
   - Save the encrypted file securely to your device.  

## 📚 Notes
- This is a **student mini-project** designed for learning purposes.  
- The app is deployed on **Streamlit Cloud** and accessible via the link above.
- Working on the description button.
