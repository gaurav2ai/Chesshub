# ♟️ ChessHub

A modern chess tournament and booking management platform built with Django, MySQL, and Tailwind CSS.

ChessHub allows players to register, book tournament slots, manage bookings, make payments, and participate in chess events through an easy-to-use web interface.

---

## 🚀 Features

### 🔐 Authentication System

* User Registration
* User Login
* Logout Functionality
* Password Reset via Email
* Secure Authentication

### 📅 Tournament Management

* Create Tournament Slots
* Manage Tournament Schedules
* Holiday-Based Tournament Planning
* Slot Availability Tracking

### 🎟️ Booking System

* Tournament Booking
* Booking History
* Booking Management
* Real-Time Slot Allocation

### 💳 Payment Integration

* Online Payment Support
* Payment Tracking
* Booking Confirmation After Payment

### 📧 Email Notifications

* Password Reset Emails
* Booking Confirmation Emails
* User Notifications

### 👨‍💼 Admin Dashboard

* Manage Users
* Manage Bookings
* Manage Tournament Slots
* View Payments
* Monitor System Activity

### 🎨 Modern UI

* Tailwind CSS
* Responsive Design
* Mobile Friendly Interface
* Clean Dashboard Layout

---

# 🛠️ Tech Stack

## Backend

* Python
* Django
* Django ORM

## Database

* MySQL

## Frontend

* HTML
* Tailwind CSS
* JavaScript

## Additional Services

* Gmail SMTP
* Payment Gateway Integration

---

# 📂 Project Structure

```text
ChessHub
│
├── chesshub/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── signals.py
│   ├── admin.py
│   └── services/
│
├── pro1/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/
│   ├── auth/
│   ├── bookings/
│   ├── dashboard/
│   └── partials/
│
├── theme/
│
├── manage.py
├── requirements.txt
└── Procfile
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/gaurav2ai/Chesshub.git
cd Chesshub
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv env
env\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv env
source env/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ Database Configuration

Create MySQL Database:

```sql
CREATE DATABASE chesshub;
```

Update your database configuration in:

```python
pro1/settings.py
```

Example:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chesshub',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

---

# 📧 Email Configuration

Create a `.env` file:

```env
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

Update settings.py:

```python
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
```

---

# 🏃 Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# 👤 Create Superuser

```bash
python manage.py createsuperuser
```

---

# ▶️ Run Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000
```

---

# 🔑 Admin Panel

Login using superuser credentials:

```text
http://127.0.0.1:8000/admin
```

From the Admin Panel you can:

* Manage Users
* Create Tournament Slots
* Manage Bookings
* Track Payments
* Configure Tournaments

---

# 📸 Screenshots

Add screenshots here after deployment.

```text
screenshots/
├── login.png
├── dashboard.png
├── bookings.png
└── tournaments.png
```

---

# 🔒 Security Notes

Never commit:

```text
.env
env/
venv/
__pycache__/
db.sqlite3
```

Store all credentials using environment variables.

---

# 🚀 Future Enhancements

* Real-Time Chess Matches
* Live Tournament Tracking
* Player Ratings System
* Leaderboards
* Match History
* Multiplayer Chess Integration
* AI Opponent Support

---

# 👨‍💻 Author

## Gaurav Arvind Chaubey

Full Stack Developer

### Connect With Me

🔗 LinkedIn: [www.linkedin.com/in/gauravv-choubey-774b59381](http://www.linkedin.com/in/gauravv-choubey-774b59381)

### Skills

* Python
* Django
* MySQL
* JavaScript
* Tailwind CSS
* REST APIs

---

⭐ If you like this project, consider giving it a star on GitHub.
