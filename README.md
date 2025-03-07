NaDS - Network Anomaly Detection System

NaDS (Network Anomaly Detection System) is a Python-based tool designed for network anomaly detection, featuring dual-interface access via CLI & Web App. It includes user authentication, admin-controlled user management, and SQLite database storage.

Directory Structure:
NaDS/
    app.py                     # Main application file
    requirements.txt           # Required dependencies
    users.db                   # SQLite database file (auto-created)
    static/
        style.css              # CSS styles for web pages
        background.jpg         # Background image for login page
    templates/
        login.html             # User login page
        login_success.html     # Post-login success page
    README.txt                 # Documentation file

Installation:

1. Create a Virtual Environment
    python -m venv venv
    venv\Scripts\activate

2. Install Dependencies
    pip install -r requirements.txt

Usage:

1. Start the Application
    Run python app.py

1.1 It will prompt for login before showing two options:
    a. Run on CLI : Runs the CLI tool
    b. Run on Browser : Opens the web login page

2. User Management
    To access User Management, run: python app.py user_management
    It will ask for the admin username and password before allowing the following operations:
        1. Add User
        2. Delete User
        3. Modify User
        4. Show All Users
        5. Logout

Configuration:
    Default User:
        Username: admin
        Password: admin

Using SQLite with in NaDS:

1. Open SQLite Database in CLI
    sqlite3 users.db

2. View All Tables in users.db
    .tables

3. View the Structure of the users Table
    PRAGMA table_info(users);

4. Show All Users in the Database
    SELECT * FROM users;

5. Exit SQLite Shell
    .exit

Deactivate the Virtual Environment:
    deactivate


Author:
Developed by: Hammad Ahmed (bc210209607)
Project: Final Year Project (FYP)