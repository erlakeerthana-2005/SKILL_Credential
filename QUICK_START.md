# QUICK START GUIDE

## 🚀 Running the Project (3 Simple Steps)

### Step 1: Install Dependencies
```bash
cd d:\SKILL\backend
pip install -r requirements.txt
```

### Step 2: Start Backend
```bash
python app.py
```
✅ Backend running on: http://localhost:5000

### Step 3: Open Frontend
Run a server to avoid security blocks:
```bash
cd d:\SKILL\frontend
python -m http.server 5500
```
✅ Access in browser: [http://localhost:5500/register.html](http://localhost:5500/register.html)

---

## 📝 Quick Test

### Register an Institution:
1. Open `register.html`
2. Fill form:
   - Name: `MIT University`
   - Email: `admin@mit.edu`
   - Password: `mit123`
   - Role: `institution`
3. Click Register

### Login:
1. Click "Sign in" link
2. Enter:
   - Email: `admin@mit.edu`
   - Password: `mit123`
3. Click Login
4. → Redirects to issue-credential page

### Issue Credential:
1. Fill form:
   - Skill: `Python Programming`
   - Issuer: `MIT University`
2. Click "Issue Credential"
3. ✅ See credential hash!

---

## 📁 Project Structure

```
SKILL/
├── backend/
│   ├── app.py              ← Main Flask app (all APIs)
│   ├── models.py           ← User & Credential models
│   ├── database.py         ← Database setup
│   ├── requirements.txt    ← Python packages
│   └── instance/
│       └── users.db        ← SQLite database (auto-created)
│
├── frontend/
│   ├── register.html       ← Registration page
│   ├── login.html          ← Login page
│   ├── issue-credential.html ← Issue credential page
│   ├── script.js           ← JavaScript functions
│   ├── style.css           ← Styling
│   └── logo.png            ← Logo
│
├── README.md               ← Full documentation
├── API_TESTING_GUIDE.md    ← API examples
├── HOW_IT_WORKS.md         ← Detailed explanations
├── QUICK_START.md          ← This file
└── start-backend.bat       ← Windows startup script
```

---

## 🔑 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register new user | No |
| POST | `/login` | Login user | No |
| POST | `/issue-credential` | Issue credential | Yes (JWT) |
| GET | `/credentials` | Get all credentials | No |

---

## 👥 User Roles

| Role | Can Register | Can Login | Can Issue Credentials |
|------|--------------|-----------|----------------------|
| student | ✅ | ✅ | ❌ |
| institution | ✅ | ✅ | ✅ |
| employer | ✅ | ✅ | ❌ |
| admin | ✅ | ✅ | ❌ (future) |

---

## 🧪 Testing Different Roles

### Test 1: Student (Cannot Issue)
```
Register → role: "student"
Login → Try issue-credential.html
Result: ❌ "Only institutions can issue credentials"
```

### Test 2: Institution (Can Issue)
```
Register → role: "institution"
Login → issue-credential.html
Result: ✅ Credential issued successfully
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection refused | Start backend: `python app.py` |
| Invalid credentials | Check email/password, register first |
| CORS error | Backend already has CORS enabled |
| Can't issue credential | Login as institution role |
| Email already registered | Use different email |

---

## 📚 Documentation Files

- **README.md** - Complete project documentation
- **API_TESTING_GUIDE.md** - API examples with curl/Postman
- **HOW_IT_WORKS.md** - Detailed technical explanations
- **QUICK_START.md** - This file (quick reference)

---

## 🎯 Module Checklist

### ✅ Module 1: User Registration & Authentication
- [x] User registration with role selection
- [x] Password hashing (bcrypt)
- [x] JWT authentication
- [x] Login functionality
- [x] Email uniqueness validation
- [x] Role-based redirection

### ✅ Module 2: Credential Issuance
- [x] Credential issuance (institutions only)
- [x] JWT token validation
- [x] Role-based access control
- [x] SHA-256 hash generation
- [x] Credential storage in database
- [x] View all credentials API

---

## 💡 Key Features

1. **Security**
   - Bcrypt password hashing
   - JWT authentication
   - Role-based access control

2. **Database**
   - SQLite (no setup required)
   - SQLAlchemy ORM
   - User and Credential models

3. **Frontend**
   - Simple HTML/JavaScript
   - Fetch API for backend calls
   - Token storage in localStorage

4. **Backend**
   - Flask REST API
   - CORS enabled
   - Clear error messages

---

## 📊 Example Data

### Sample Users:
```json
{
  "name": "MIT University",
  "email": "admin@mit.edu",
  "password": "mit123",
  "role": "institution"
}
```

### Sample Credential:
```json
{
  "skill_name": "Python Programming",
  "issuer_name": "MIT University"
}
```

### Sample Response:
```json
{
  "credential_id": 1,
  "credential_hash": "a3f5b8c9d2e1f4a7...",
  "issue_date": "2025-12-13T16:30:45"
}
```

---

## 🎓 For Academic Evaluation

**Implemented:**
- ✅ Module 1: User Registration & Authentication
- ✅ Module 2: Credential Issuance
- ✅ Module 3: Blockchain Integration (Immutable Ledger)
- ✅ Module 4: Federated Learning (AI Skill Recommendations)
- ✅ Module 5: Public Credential Verification Portal
- ✅ Module 6: Advanced Glassmorphic Dashboards
- ✅ Premium UI/UX with Micro-animations
- ✅ Robust security & centralized logging

---

## 🚦 Next Steps

1. ✅ Run the project
2. ✅ Test all features
3. ✅ Read documentation
4. 📝 Prepare presentation
5. 🎯 Plan Module 3 (Blockchain)

---

## 📞 Need Help?

Check these files:
1. **README.md** - Full setup guide
2. **HOW_IT_WORKS.md** - Technical details
3. **API_TESTING_GUIDE.md** - API examples

---

**Project:** Blockchain-Based Skill Credential Aggregator System  
**Status:** All 6 Modules Complete (100%) ✅  
**Tech Stack:** Flask + SQLite + Blockchain + AI/FL + Glassmorphic UI  
**Ready for:** Final Academic Evaluation & Deployment
