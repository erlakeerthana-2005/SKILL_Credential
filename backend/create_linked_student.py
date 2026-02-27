import sqlite3
import os
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask import Flask

# Need flask-bcrypt for password hashing compatible with the app
app = Flask(__name__)
bcrypt = Bcrypt(app)

db_path = r'd:\SKILL\backend\instance\users.db'

def create_linked_student():
    if not os.path.exists(db_path):
        print("Database not found")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 1. Find the Global Institute of Technology
        cursor.execute("SELECT id, name FROM user WHERE role='institution' LIMIT 1")
        inst = cursor.fetchone()
        
        if not inst:
            print("No institution found to link the student to.")
            return
        
        inst_id, inst_name = inst
        print(f"Linking new student to: {inst_name} (ID: {inst_id})")

        # 2. Prepare student details
        name = "New Student"
        email = "student@example.com"
        password = "password123"
        role = "student"
        # Generate hash using the same algorithm as the app
        with app.app_context():
            hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 3. Insert the new student
        cursor.execute("""
            INSERT INTO user (name, email, password, role, is_verified, institution_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, email, hashed_pw, role, 1, inst_id, created_at))

        conn.commit()
        new_id = cursor.lastrowid
        print(f"Successfully created student '{name}' with ID: {new_id} linked to {inst_name}")

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_linked_student()
