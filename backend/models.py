from database import db
from datetime import datetime

# User Model - stores user information for authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)  # Email must be unique
    password = db.Column(db.String(200))  # Stores hashed password
    role = db.Column(db.String(50))  # student, institution, employer, admin
    is_verified = db.Column(db.Boolean, default=False)  # For email OTP verification
    institution_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Linked institute for students
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Model to store OTPs for email verification
class VerificationOTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Credential Model - stores credentials issued by institutions or added by students
class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ID of the student
    issuer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)     # ID of the institution (null for external)
    skill_name = db.Column(db.String(200), nullable=False)  # Name of the skill
    issuer_name = db.Column(db.String(200), nullable=False)  # Name of the issuing institution/website
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)  # Date when credential was issued
    credential_hash = db.Column(db.String(64), nullable=False)  # SHA-256 hash
    status = db.Column(db.String(20), default='verified')  # verified, pending, revoked, external
    credential_type = db.Column(db.String(20), default='internal')  # internal, external
