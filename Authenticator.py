import sys
import pyotp
import sqlite3
import base64
import qrcode
import cv2
import numpy as np
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QListWidget, QLineEdit, QMessageBox, QFileDialog, QInputDialog)
from PyQt5.QtGui import QPixmap, QImage
import os

# Function to load or generate encryption key
def load_or_generate_key():
    key_file = "key.key"
    if os.path.exists(key_file):
        with open(key_file, "rb") as file:
            return file.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, "wb") as file:
            file.write(key)
        return key

# Load encryption key (ensuring it stays the same)
KEY = load_or_generate_key()
cipher_suite = Fernet(KEY)

# Database Setup
db_conn = sqlite3.connect("authenticator.db")
cursor = db_conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    secret TEXT NOT NULL
)
""")
db_conn.commit()

def encrypt_secret(secret):
    return cipher_suite.encrypt(secret.encode()).decode()

def decrypt_secret(encrypted_secret):
    try:
        return cipher_suite.decrypt(encrypted_secret.encode()).decode()
    except:
        return None  # Return None if decryption fails (invalid key or corrupted data)

class AuthenticatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows Authenticator App")
        self.setGeometry(100, 100, 400, 500)
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Your Authentication Accounts")
        self.layout.addWidget(self.label)
        
        self.account_list = QListWidget()
        self.account_list.itemClicked.connect(self.generate_otp)
        self.layout.addWidget(self.account_list)
        
        self.add_account_btn = QPushButton("Add Account Manually")
        self.add_account_btn.clicked.connect(self.add_account_manual)
        self.layout.addWidget(self.add_account_btn)
        
        self.totp_label = QLabel("Generated OTP:")
        self.layout.addWidget(self.totp_label)
        
        self.setLayout(self.layout)
        self.load_accounts()
    
    def load_accounts(self):
        self.account_list.clear()
        cursor.execute("SELECT name FROM accounts")
        for row in cursor.fetchall():
            self.account_list.addItem(row[0])
    
    def add_account_manual(self):
        name, ok1 = QInputDialog.getText(self, "Add Account", "Enter Account Name:")
        if not ok1 or not name:
            return
        secret, ok2 = QInputDialog.getText(self, "Enter Secret", "Enter the TOTP Secret Key:")
        if ok2 and secret:
            encrypted_secret = encrypt_secret(secret)
            cursor.execute("INSERT INTO accounts (name, secret) VALUES (?, ?)", (name, encrypted_secret))
            db_conn.commit()
            self.load_accounts()
            QMessageBox.information(self, "Success", f"Account '{name}' added successfully!")
    
    def generate_otp(self, item):
        account_name = item.text()
        cursor.execute("SELECT secret FROM accounts WHERE name = ?", (account_name,))
        row = cursor.fetchone()
        if row:
            decrypted_secret = decrypt_secret(row[0])
            if decrypted_secret:
                totp = pyotp.TOTP(decrypted_secret)
                otp = totp.now()
                self.totp_label.setText(f"Generated OTP: {otp}")
            else:
                QMessageBox.warning(self, "Error", "Failed to decrypt secret. Possible key mismatch.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthenticatorApp()
    window.show()
    sys.exit(app.exec_())
