from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_mail import Mail, Message
from database import db
from models import User, Credential, VerificationOTP
from blockchain import skill_blockchain
from federated_learning import fl_engine
import hashlib
import random
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
# Permit CORS for all origins to prevent connection failures from local files
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'secret-key'

# Email Config (from .env)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('SkillsLink Verification', os.getenv('MAIL_DEFAULT_SENDER'))

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app) # Initialize Flask-Mail

# Create database tables
with app.app_context():
    db.create_all()
    
    # Rebuild in-memory blockchain from existing credentials to survive restarts
    if len(skill_blockchain.chain) == 1:
        existing_creds = Credential.query.order_by(Credential.issue_date).all()
        for cred in existing_creds:
            student = User.query.get(cred.student_id)
            skill_blockchain.add_block({
                "credential_id": cred.id,
                "credential_hash": cred.credential_hash,
                "student": student.name if student else "N/A",
                "issuer": cred.issuer_name,
                "skill": cred.skill_name
            })

# ============================================
# MODULE 1: USER REGISTRATION & AUTHENTICATION
# ============================================

# API: Register a new user with OTP
@app.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    
    # Validation check
    if not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({"message": "Missing required fields"}), 400
    
    # Confirm password check
    if data.get('password') != data.get('confirm_password'):
        return jsonify({"message": "Passwords do not match"}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(email=data.get('email')).first()
    if existing_user and existing_user.is_verified:
        return jsonify({"message": "Email already registered and verified"}), 400

    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    role = data.get('role', 'student')

    # Hash the password for security
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    # If user exists but not verified, we'll just update their info/OTP
    if existing_user:
        existing_user.name = name
        existing_user.password = hashed_pw
        existing_user.role = role
        user_to_update = existing_user
    else:
        # Create new user object (unverified)
        user_to_update = User(
            name=name,
            email=email,
            password=hashed_pw,
            role=role,
            is_verified=False
        )
        db.session.add(user_to_update)

    # Optional: Link to institution if name matches an existing record
    if data['role'] == 'student' and data.get('institution_name'):
        inst = User.query.filter_by(name=data['institution_name'], role='institution').first()
        if inst:
            user_to_update.institution_id = inst.id
            print(f"[SYSTEM] Registration: Student linked to {inst.name}")
        else:
            user_to_update.institution_id = None
            print(f"[SYSTEM] Registration: Institution '{data['institution_name']}' not found. No link established.")

    # Generate 6-digit OTP
    otp_code = str(random.randint(100000, 999999))
    
    # Save or update OTP in database
    existing_otp = VerificationOTP.query.filter_by(email=email).first()
    if existing_otp:
        existing_otp.otp = otp_code
        existing_otp.created_at = datetime.utcnow()
    else:
        new_otp = VerificationOTP(email=email, otp=otp_code)
        db.session.add(new_otp)

    db.session.commit()

    # REAL: Send email OTP using Flask-Mail
    try:
        msg = Message("Verification Code - Skill Portal",
                      recipients=[email])
        msg.body = f"Your 6-digit verification code for the Skill Credential Aggregator System is: {otp_code}"
        msg.html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #d4af37; text-align: center;">Skill Credential Aggregator</h2>
                <p>Hello {name},</p>
                <p>Thank you for joining our ecosystem. To complete your registration, please verify your email address using the following code:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <span style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #fff; background: #0a0e14; padding: 15px 30px; border-radius: 8px;">{otp_code}</span>
                </div>
                <p>This code will expire shortly. If you did not request this, please ignore this email.</p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 12px; color: #777;">Secure Blockchain-Based Verification System.</p>
            </div>
        """
        mail.send(msg)
        print(f"\n[SYSTEM] LIVE EMAIL SENT TO {email}\n")
    except Exception as e:
        print(f"\n[WARNING] Failed to send live email: {str(e)}")
        print(f"[FALLBACK] OTP code for {email} is: {otp_code}\n")

    return jsonify({"message": "OTP sent to your email. Please verify to complete registration."}), 200

# API: Verify OTP
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    email = data.get('email')
    otp_received = data.get('otp')

    otp_record = VerificationOTP.query.filter_by(email=email, otp=otp_received).first()
    
    if otp_record:
        # 1. OTP expiry check (5 minutes)
        from datetime import timedelta
        time_elapsed = datetime.utcnow() - otp_record.created_at
        if time_elapsed > timedelta(minutes=5):
            db.session.delete(otp_record)
            db.session.commit()
            return jsonify({"message": "OTP has expired. Please try registering again.", "verified": False}), 400

        # 2. Mark user as verified
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_verified = True
            db.session.delete(otp_record) 
            db.session.commit()
            return jsonify({"message": "Account verified successfully", "verified": True}), 200
    
    return jsonify({"message": "Invalid or incorrect OTP", "verified": False}), 400

# API: Login user
@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    # Find user by email
    user = User.query.filter_by(email=email).first()

    # Verify password and generate JWT token
    if user and bcrypt.check_password_hash(user.password, password):
        if not user.is_verified:
            return jsonify({"message": "Please verify your email before logging in", "verified": False}), 403
            
        token = create_access_token(identity=user.email)
        
        # Get institution name if student
        inst_name = None
        if user.role == 'student' and user.institution_id:
            inst = User.query.get(user.institution_id)
            if inst:
                inst_name = inst.name

        return jsonify({
            "message": "Login successful",
            "token": token,
            "role": user.role,
            "name": user.name,
            "user_id": user.id,
            "institution": inst_name
        })

    return jsonify({"message": "Invalid credentials"}), 401

# ============================================
# MODULE 2: CREDENTIAL ISSUANCE
# ============================================

# API: Issue a credential (only institutions can issue)
@app.route('/issue-credential', methods=['POST'])
@jwt_required()
def issue_credential():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    if user.role != 'institution':
        return jsonify({"message": "Only institutions can issue credentials"}), 403
    
    data = request.json
    
    # NEW: Validate student email
    student_email = data.get('student_email')
    if not student_email:
        return jsonify({"message": "student_email is required"}), 400
        
    student = User.query.filter_by(email=student_email).first()
    if not student or student.role != 'student':
        return jsonify({"message": "Invalid student email"}), 404

    if not data.get('skill_name') or not data.get('issuer_name'):
        return jsonify({"message": "skill_name and issuer_name are required"}), 400
    
    # Generate SHA-256 hash
    credential_string = f"{student.id}{user.id}{data['skill_name']}{data['issuer_name']}{datetime.utcnow()}"
    credential_hash = hashlib.sha256(credential_string.encode()).hexdigest()
    
    # Create new credential object
    new_credential = Credential(
        student_id=student.id,
        issuer_id=user.id,
        skill_name=data['skill_name'],
        issuer_name=data['issuer_name'],
        credential_hash=credential_hash,
        status='verified',
        credential_type='internal'
    )
    
    # Save to database
    db.session.add(new_credential)
    db.session.commit()
    
    # MODULE 3: Add to Blockchain
    skill_blockchain.add_block({
        "credential_id": new_credential.id,
        "credential_hash": credential_hash,
        "student": student.name,
        "issuer": user.name,
        "skill": data['skill_name']
    })
    
    return jsonify({
        "message": "Credential issued successfully & recorded on blockchain",
        "credential_id": new_credential.id,
        "credential_hash": credential_hash,
        "issue_date": new_credential.issue_date.isoformat(),
        "type": "internal"
    }), 201# API: Get credentials for a specific student (Public - no auth required)
@app.route('/public-profile/<int:student_id>', methods=['GET'])
def get_public_profile(student_id):
    student = User.query.get(student_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404
        
    credentials = Credential.query.filter_by(student_id=student_id).all()
    
    # Format the data
    output = []
    for cred in credentials:
        output.append({
            "id": cred.id,
            "skill_name": cred.skill_name,
            "issuer_name": cred.issuer_name,
            "issue_date": cred.issue_date,
            "credential_hash": cred.credential_hash,
            "status": cred.status,
            "type": cred.credential_type
        })
    
    return jsonify({
        "student_name": student.name,
        "credentials": output
    }), 200

# API: Add an external credential (added by student)
@app.route('/add-external-credential', methods=['POST'])
@jwt_required()
def add_external_credential():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    if user.role != 'student':
        return jsonify({"message": "Only students can manually add external credentials"}), 403
    
    data = request.json
    if not data.get('skill_name') or not data.get('issuer_name'):
        return jsonify({"message": "skill_name and issuer_name are required"}), 400
    
    # Generate SHA-256 hash
    credential_string = f"EXTERNAL{user.id}{data['skill_name']}{data['issuer_name']}{datetime.utcnow()}"
    credential_hash = hashlib.sha256(credential_string.encode()).hexdigest()
    
    new_credential = Credential(
        student_id=user.id,
        issuer_id=None,  # External source
        skill_name=data['skill_name'],
        issuer_name=data['issuer_name'],
        credential_hash=credential_hash,
        status='external',
        credential_type='external'
    )
    
    db.session.add(new_credential)
    db.session.commit()
    
    # Add to Blockchain for external credentials as well
    skill_blockchain.add_block({
        "credential_id": new_credential.id,
        "credential_hash": credential_hash,
        "student": user.name,
        "issuer": data['issuer_name'],
        "skill": data['skill_name']
    })
    
    return jsonify({
        "message": "External credential added successfully",
        "credential_id": new_credential.id,
        "credential_hash": credential_hash,
        "issue_date": new_credential.issue_date.isoformat(),
        "type": "external"
    }), 201

# API: Get all credentials
@app.route('/credentials', methods=['GET'])
def get_credentials():
    credentials = Credential.query.all()
    result = []
    for cred in credentials:
        result.append({
            "id": cred.id,
            "student_id": cred.student_id,
            "issuer_id": cred.issuer_id,
            "skill_name": cred.skill_name,
            "issuer_name": cred.issuer_name,
            "issue_date": cred.issue_date.isoformat(),
            "credential_hash": cred.credential_hash,
            "status": cred.status,
            "type": cred.credential_type
        })
    return jsonify(result), 200

# API: Get credentials issued by current institution
@app.route('/my-issued-credentials', methods=['GET'])
@jwt_required()
def get_my_issued_credentials():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    credentials = Credential.query.filter_by(issuer_id=user.id).all()
    result = []
    for cred in credentials:
        student = User.query.get(cred.student_id)
        result.append({
            "id": cred.id,
            "student_name": student.name if student else "Unknown",
            "skill_name": cred.skill_name,
            "issue_date": cred.issue_date.isoformat(),
            "credential_hash": cred.credential_hash,
            "status": cred.status
        })
    return jsonify(result), 200

# API: Get credentials for current student
@app.route('/my-credentials', methods=['GET'])
@jwt_required()
def get_my_credentials():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    credentials = Credential.query.filter_by(student_id=user.id).all()
    result = []
    for cred in credentials:
        result.append({
            "id": cred.id,
            "issuer_name": cred.issuer_name,
            "skill_name": cred.skill_name,
            "issue_date": cred.issue_date.isoformat(),
            "credential_hash": cred.credential_hash,
            "status": cred.status,
            "type": cred.credential_type
        })
    return jsonify(result), 200

# ============================================
# MODULE 5: CREDENTIAL VERIFICATION
# ============================================

@app.route('/verify-credential/<string:hash_value>', methods=['GET'])
def verify_credential(hash_value):
    # Search in Database
    credential = Credential.query.filter_by(credential_hash=hash_value).first()
    
    # Search in Blockchain
    block = skill_blockchain.get_block_by_hash(hash_value)
    
    if credential and block:
        student = User.query.get(credential.student_id)
        return jsonify({
            "verified": True,
            "message": "Credential search successful and verified on blockchain",
            "data": {
                "skill": credential.skill_name,
                "issuer": credential.issuer_name,
                "student": student.name if student else "N/A",
                "issue_date": credential.issue_date.isoformat(),
                "blockchain_block": block.index,
                "blockchain_timestamp": str(block.timestamp)
            }
        }), 200
        
    return jsonify({
        "verified": False,
        "message": "Credential not found or blockchain record missing"
    }), 404

# API: Get all users (admin only)
@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    # Get current user's email from JWT token
    current_user_email = get_jwt_identity()
    
    # Find the user in database
    user = User.query.filter_by(email=current_user_email).first()
    
    # Check if user is an admin
    if user.role != 'admin':
        return jsonify({"message": "Only admins can view all users"}), 403
    
    # Get all users
    users = User.query.all()
    
    result = []
    for u in users:
        result.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "created_at": u.created_at.isoformat()
        })
    return jsonify(result), 200

# API: Delete a user (admin only)
@app.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_email = get_jwt_identity()
    admin = User.query.filter_by(email=current_user_email).first()
    
    if admin.role != 'admin':
        return jsonify({"message": "Access Denied: Admin privileges required"}), 403
        
    user_to_delete = User.query.get(user_id)
    if not user_to_delete:
        return jsonify({"message": "User not found"}), 404
        
    # Prevent admin from deleting themselves
    if user_to_delete.email == admin.email:
        return jsonify({"message": "Admin accounts cannot be deleted from within the dashboard"}), 400

    # Clean up associated credentials first
    Credential.query.filter((Credential.student_id == user_id) | (Credential.issuer_id == user_id)).delete()
    
    # Clean up OTP records
    VerificationOTP.query.filter_by(email=user_to_delete.email).delete()
    
    # Delete the user
    db.session.delete(user_to_delete)
    db.session.commit()
    
    return jsonify({"message": f"User {user_to_delete.name} and all linked data successfully removed"}), 200

# ============================================
# MODULE 4: FEDERATED LEARNING (SKILL REC)
# ============================================

@app.route('/recommend-skills', methods=['GET'])
@jwt_required()
def recommend_skills():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    # Get student's current skills to avoid recommending what they already have
    student_credentials = Credential.query.filter_by(student_id=user.id).all()
    held_skills = [c.skill_name for c in student_credentials]
    
    # Get recommendations from the FL engine
    recommendations = fl_engine.get_recommendations(held_skills)
    
    return jsonify({
        "student": user.name,
        "recommendations": recommendations,
        "model_round": fl_engine.training_round
    }), 200

@app.route('/admin/train-fl', methods=['POST'])
@jwt_required()
def train_fl():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    if user.role != 'admin':
        return jsonify({"message": "Only admins can trigger FL rounds"}), 403
    
    result = fl_engine.run_federated_round()
    return jsonify({
        "message": "Federated Learning round completed successfully",
        "data": result
    }), 200

if __name__ == "__main__":
    app.run(debug=True)

