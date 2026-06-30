# 🤖 Beauty Clinic Bale Bot

<div align="center">

A production-ready **Beauty Clinic Bot** for **Bale Messenger**, built with **Python** and **MongoDB**.

Designed to automate customer registration, service selection, consultation requests, appointment data collection, and clinic administration.

<br>

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge\&logo=python\&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?style=for-the-badge\&logo=mongodb\&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-HTTP-black?style=for-the-badge)
![Bale API](https://img.shields.io/badge/Bale-Bot_API-blue?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/ArshiaBourbour/BaleBOT-BeautyClinic?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/ArshiaBourbour/BaleBOT-BeautyClinic?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/ArshiaBourbour/BaleBOT-BeautyClinic?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/ArshiaBourbour/BaleBOT-BeautyClinic?style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/ArshiaBourbour/BaleBOT-BeautyClinic?style=for-the-badge)

</div>

---

# ✨ Overview

Beauty Clinic Bale Bot is a complete customer management bot developed for Bale Messenger.

The bot guides users through different clinic services, collects customer information, stores data in MongoDB, provides an administrator panel, and generates CSV reports.

It has been designed with a modular architecture so new services and workflows can be added easily.

---

# ✨ Features

## 👥 Customer Features

* Interactive Inline Keyboard
* Multi-level service menus
* Laser services
* Injection services
* Weight loss services
* Personalized consultation flow
* Customer registration
* Automatic phone validation
* Persian & English digit support
* Store customer information
* Tehran timezone support
* Jalali date support

---

## 🩺 Supported Services

### ✨ Laser

* Hair Removal
* Rejuvenation
* Scar Treatment

### 💉 Injections

* Lip Filler
* Jawline
* Botox
* Body Filler

### 🏋 Weight Loss

* Consultation
* Diet Program
* Medical Devices
* Weight Packages

---

## 👨‍💼 Admin Features

* Secure login
* Username & Password authentication
* Session timeout
* Failed login protection
* CSV export
* Daily reports
* 2-day reports
* Weekly reports
* View bot statistics
* Logout

---

## 📊 Statistics

Administrator can view:

* Total registered customers
* Today's registrations
* Weekly registrations

---

# 📂 Project Structure

```text
BaleBOT-BeautyClinic/

├── main.py
├── config.py
├── database.py
├── keyboards.py
├── admin_panel.py
├── requirements.txt
├── README.md
│
├── offset.txt
│
└── MongoDB
```

---

# 🔄 User Flow

```text
User
 │
 ▼
/start
 │
 ▼
Main Menu
 │
 ├─────────────┐
 │             │
 ▼             ▼
Laser      Injections
 │             │
 ▼             ▼
Select Service
 │
 ▼
Enter Name
 │
 ▼
Enter Phone Number
 │
 ▼
Save To MongoDB
 │
 ▼
Registration Completed
```

---

# 👨‍💼 Admin Flow

```text
/admin
    │
    ▼
Username
    │
    ▼
Password
    │
    ▼
Authentication
    │
    ▼
Admin Panel
    │
    ├─────────────┐
    │             │
    ▼             ▼
CSV Export   Reports
```

---

# 🗄 Database

Database Engine

* MongoDB

Collection

```
users
```

Stored Fields

* fullname
* phone
* service
* customer_type
* weight
* height
* age
* gender
* تاریخ
* زمان
* timestamp

---

# 🛠 Tech Stack

* Python
* MongoDB
* Requests
* Bale Bot API
* Inline Keyboards
* CSV
* pytz
* jdatetime

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/ArshiaBourbour/BaleBOT-BeautyClinic.git

cd BaleBOT-BeautyClinic
```

---

## Create Virtual Environment

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## Install Requirements

```bash
pip install -r requirements.txt
```

---

## Install MongoDB

Ubuntu

```bash
sudo apt install mongodb
```

or

Install MongoDB Community Server from the official website.

---

## Start MongoDB

Linux

```bash
sudo systemctl start mongod
```

Windows

Run MongoDB Service.

---

# ⚙ Configuration

Edit:

```
config.py
```

Example

```python
TOKEN = "YOUR_BALE_TOKEN"

ADMIN_USERNAME = "admin"

ADMIN_PASSWORD = "password"
```

---

# ▶ Run

```bash
python main.py
```

The bot starts Long Polling automatically.

---

# 📥 CSV Export

Administrator can export:

* All users
* Today's users
* Last 2 days
* Last 7 days

Encoding

UTF-8 BOM

Compatible with Microsoft Excel.

---

# 🔐 Security

* Login attempt limitation
* Automatic blocking
* Session expiration
* Phone validation
* Callback-based navigation

---

# 📱 Phone Validation

Accepted

```
09123456789
```

```
۰۹۱۲۳۴۵۶۷۸۹
```

Supports

* Persian digits
* English digits
* +98 prefix

---

# 📈 Bot Statistics

Displayed after successful admin login

* Total Customers
* Today's Customers
* Weekly Customers

---

# 🎯 Keyboard Navigation

Main Menu

* Laser
* Injections
* Weight Loss

Laser

* Hair Removal
* Rejuvenation
* Scar Treatment

Weight Loss

* Consultation
* Diet
* Devices
* Packages

Injection

* Lip Filler
* Jawline
* Botox
* Body Filler

---

# 📝 Logging

Recommended logging includes

* User registration
* Admin login
* Export operations
* Exceptions
* Errors

---

# 📌 Roadmap

* Docker Support
* Redis Session Storage
* Multi Admin
* Appointment Scheduling
* Reminder Messages
* SMS Integration
* Payment Gateway
* Dashboard
* Docker Compose
* Webhook Mode
* Multi-language Support

---

# 📄 License

This project is released under the MIT License.

---

<div align="center">

Made with ❤️ using Python & Bale Bot API

⭐ If you like this project, don't forget to give it a Star.

</div>

