import sqlite3
import getpass
import webbrowser
import sys
from flask import Flask, request, render_template, redirect, session

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'bc210209607'  # Required for session management

db_file = 'users.db'

def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL,
                      role TEXT NOT NULL)''')
    cursor.execute("""INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin', 'admin')""")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    if 'user' in session:
        return redirect('/welcome')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user'] = username
            return redirect('/welcome')  # Redirect to the success page
        else:
            return render_template('login.html', error="Invalid credentials.")
    
    return render_template('login.html')


@app.route('/welcome')
def welcome():
    if 'user' in session:
        return render_template('welcome.html')
    return redirect('/login')

def cli_login():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        print("Login successful!")
        return True
    else:
        print("Invalid credentials")
        return False

def cli_admin_login():
    username = input("Enter admin username: ")
    password = getpass.getpass("Enter admin password: ")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ? AND role = 'admin'", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        print("Login successful! Accessing user management...")
        admin_menu()
    else:
        print("Invalid admin credentials. Access denied.")

def admin_menu():
    """Admin menu for user management."""
    while True:
        print("\nAdmin Menu:")
        print("1. Add User")
        print("2. Delete User")
        print("3. Modify User")
        print("4. Show All Users")
        print("5. Logout")
        choice = input("Enter option: ")
        if choice == '1':
            add_user()
        elif choice == '2':
            delete_user()
        elif choice == '3':
            modify_user()
        elif choice == '4':
            show_users()
        elif choice == '5':
            break
        else:
            print("Invalid option")

def add_user():
    """Add a new user with role selection."""
    username = input("Enter new username: ")
    password = getpass.getpass("Enter password: ")

    # Ask for role selection
    print("\nSelect Role:")
    print("1. Admin")
    print("2. User")
    role_choice = input("Enter option (1 or 2): ")

    if role_choice == '1':
        role = "admin"
    elif role_choice == '2':
        role = "user"
    else:
        print("Invalid choice! Defaulting to 'user'.")
        role = "user"

    # Insert user into database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        print(f"User '{username}' added successfully as {role}.")
    except sqlite3.IntegrityError:
        print("Username already exists!")
    finally:
        conn.close()

def delete_user():
    """Delete an existing user."""
    username = input("Enter username to delete: ")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    print("User deleted successfully.")

def modify_user():
    """Modify an existing user's details."""
    username = input("Enter username to modify: ")
    new_password = getpass.getpass("Enter new password: ")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
    conn.commit()
    conn.close()
    print("User modified successfully.")

def show_users():
    """Show all users in the system."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    conn.close()
    print("\nUser List:")
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Role: {user[2]}")

def main():
    init_db()
    if len(sys.argv) > 1 and sys.argv[1] == "user_management":
        cli_admin_login()
    else:
        if cli_login():
            print("Select Mode:\n1. Run on CLI\n2. Run on Browser")
            choice = input("Enter option (1 or 2): ")
            if choice == '1':
                print("Welcome to NaDS")
                print("Network Anomaly Detection System")
                print("Develop by: Hammad Ahmed (bc210209607)")
            elif choice == '2':
                webbrowser.open('http://127.0.0.1:5000/login')
                app.run(debug=True)
            else:
                print("Invalid option")

if __name__ == '__main__':
    main()
