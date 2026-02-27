import sqlite3
import os

db_path = r'd:\SKILL\backend\instance\users.db'

def remove_users(user_ids):
    if not os.path.exists(db_path):
        print("Database not found")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Get emails for the users to be deleted (to clean up OTPs)
        placeholders = ', '.join(['?'] * len(user_ids))
        cursor.execute(f"SELECT email FROM user WHERE id IN ({placeholders})", user_ids)
        emails = [row[0] for row in cursor.fetchall()]

        # 1. Delete associated Credentials
        cursor.execute(f"DELETE FROM credential WHERE student_id IN ({placeholders}) OR issuer_id IN ({placeholders})", user_ids + user_ids)
        print(f"Deleted credentials associated with users {user_ids}")

        # 2. Delete associated OTPs
        if emails:
            email_placeholders = ', '.join(['?'] * len(emails))
            cursor.execute(f"DELETE FROM verification_otp WHERE email IN ({email_placeholders})", emails)
            print(f"Deleted OTP records for: {emails}")

        # 3. Delete the Users
        cursor.execute(f"DELETE FROM user WHERE id IN ({placeholders})", user_ids)
        print(f"Successfully deleted users with IDs: {user_ids}")

        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    ids_to_remove = [1, 4, 5]
    remove_users(ids_to_remove)
