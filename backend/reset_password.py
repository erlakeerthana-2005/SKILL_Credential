import sqlite3
import os
from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)
bcrypt = Bcrypt(app)

db_path = r'd:\SKILL\backend\instance\users.db'

def reset_password(email, new_password):
    if not os.path.exists(db_path):
        print("Database not found")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        with app.app_context():
            hashed_pw = bcrypt.generate_password_hash(new_password).decode('utf-8')
        
        cursor.execute("UPDATE user SET password = ? WHERE email = ?", (hashed_pw, email))
        if cursor.rowcount > 0:
            print(f"Successfully reset password for {email} to {new_password}")
        else:
            print(f"User with email {email} not found")

        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    reset_password("institute@test.com", "admin@123")
