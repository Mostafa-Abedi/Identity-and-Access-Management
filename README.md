# Identity-and-Access-Management
Identity and Access Management (IAM) is a framework for managing digital identities and controlling user access to systems, applications, and data. This project aims to design and implement an IAM system that ensures secure authentication, authorization, and access control for users in a web or mobile environment.

# Windows Authenticator App

## 📌 Overview
This is a Windows-based authenticator application similar to Google Authenticator. It supports Time-Based One-Time Passwords (TOTP) and allows users to manually enter authentication secrets.

## 🛠 Setup & Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/Mostafa-Abedi/Identity-and-Access-Management.git
cd Identity-and-Access-Management
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv env
source env/bin/activate  # On Mac/Linux
env\Scripts\activate  # On Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Run the Authenticator App
```sh
python authenticator.py
```

## 🚀 Using the App
- Click **"Add Account Manually"** to enter an account name and the TOTP secret key.
- Select an account from the list to **generate OTP codes**.
- Use the generated OTP code on the login page of the corresponding service.

## 📌 Features
✅ **TOTP Generation** – Generates secure 6-digit OTP codes every 30 seconds.
✅ **Manual Entry** – Add accounts manually by entering the secret key.
✅ **Secure Storage** – Encrypts and stores authentication secrets locally.
✅ **Simple UI** – Easy-to-use PyQt5 interface for managing accounts.

## 📜 License
This project is licensed under the MIT License. Feel free to contribute!

---

📩 **Maintainer:** [Mostafa Abedi](https://github.com/Mostafa-Abedi/)
