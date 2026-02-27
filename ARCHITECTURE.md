# SYSTEM ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SKILL CREDENTIAL AGGREGATOR SYSTEM                   │
│                         (Modules 1-6 Complete)                      │
└─────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND LAYER                               │
│                         (HTML + JavaScript + CSS)                         │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────────┐    │
│  │  register.html  │  │   login.html    │  │ issue-credential.html│    │
│  │                 │  │                 │  │                      │    │
│  │ • Name input    │  │ • Email input   │  │ • Skill name input   │    │
│  │ • Email input   │  │ • Password input│  │ • Issuer name input  │    │
│  │ • Password input│  │ • Login button  │  │ • Issue button       │    │
│  │ • Role select   │  │                 │  │ • Display hash       │    │
│  │ • Register btn  │  │ Calls: login()  │  │                      │    │
│  │                 │  │                 │  │ Requires: JWT token  │    │
│  │ Calls:          │  └─────────────────┘  └──────────────────────┘    │
│  │ register()      │                                                     │
│  └─────────────────┘                                                     │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                        script.js                                │    │
│  │                                                                 │    │
│  │  • register() function  → POST /register                        │    │
│  │  • login() function     → POST /login                           │    │
│  │  • Stores JWT token in localStorage                             │    │
│  │  • Redirects based on user role                                 │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP Requests (Fetch API)
                                    │ CORS Enabled
                                    ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                              BACKEND LAYER                                │
│                           (Flask + Python)                                │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                          app.py                                 │    │
│  │                    (148 lines of code)                          │    │
│  ├─────────────────────────────────────────────────────────────────┤    │
│  │                                                                 │    │
│  │  MODULE 1: USER REGISTRATION & AUTHENTICATION                  │    │
│  │  ═══════════════════════════════════════════                   │    │
│  │                                                                 │    │
│  │  ┌─────────────────────────────────────────────────────┐       │    │
│  │  │ POST /register                                      │       │    │
│  │  │ • Receives: name, email, password, role             │       │    │
│  │  │ • Validates: email uniqueness                       │       │    │
│  │  │ • Hashes: password with bcrypt                      │       │    │
│  │  │ • Creates: User object                              │       │    │
│  │  │ • Saves: to database                                │       │    │
│  │  │ • Returns: success message                          │       │    │
│  │  └─────────────────────────────────────────────────────┘       │    │
│  │                                                                 │    │
│  │  ┌─────────────────────────────────────────────────────┐       │    │
│  │  │ POST /login                                         │       │    │
│  │  │ • Receives: email, password                         │       │    │
│  │  │ • Finds: user by email                              │       │    │
│  │  │ • Verifies: password with bcrypt                    │       │    │
│  │  │ • Generates: JWT token                              │       │    │
│  │  │ • Returns: token, role, name, user_id               │       │    │
│  │  └─────────────────────────────────────────────────────┘       │    │
│  │                                                                 │    │
│  │  MODULE 2: CREDENTIAL ISSUANCE                                 │    │
│  │  ══════════════════════════════                                │    │
│  │                                                                 │    │
│  │  ┌─────────────────────────────────────────────────────┐       │    │
│  │  │ POST /issue-credential (JWT Required)               │       │    │
│  │  │ • Validates: JWT token                              │       │    │
│  │  │ • Checks: user role = 'institution'                 │       │    │
│  │  │ • Receives: skill_name, issuer_name                 │       │    │
│  │  │ • Generates: SHA-256 hash                           │       │    │
│  │  │ • Creates: Credential object                        │       │    │
│  │  │ • Saves: to database                                │       │    │
│  │  │ • Returns: credential_id, hash, date                │       │    │
│  │  └─────────────────────────────────────────────────────┘       │    │
│  │                                                                 │    │
│  │  ┌─────────────────────────────────────────────────────┐       │    │
│  │  │ GET /credentials                                    │       │    │
│  │  │ • Fetches: all credentials from database            │       │    │
│  │  │ • Returns: array of credential objects              │       │    │
│  │  └─────────────────────────────────────────────────────┘       │    │
│  │                                                                 │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                        models.py                                │    │
│  │                                                                 │    │
│  │  ┌──────────────────────┐    ┌──────────────────────┐          │    │
│  │  │   User Model         │    │  Credential Model    │          │    │
│  │  │  ─────────────       │    │  ────────────────    │          │    │
│  │  │  • id (PK)           │    │  • id (PK)           │          │    │
│  │  │  • name              │    │  • user_id (FK)      │          │    │
│  │  │  • email (unique)    │    │  • skill_name        │          │    │
│  │  │  • password (hashed) │    │  • issuer_name       │          │    │
│  │  │  • role              │    │  • issue_date        │          │    │
│  │  │  • created_at        │    │  • credential_hash   │          │    │
│  │  └──────────────────────┘    └──────────────────────┘          │    │
│  │                                                                 │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ SQLAlchemy ORM
                                    ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                            DATABASE LAYER                                 │
│                              (SQLite)                                     │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                        users.db                                 │    │
│  │                  (instance/users.db)                            │    │
│  ├─────────────────────────────────────────────────────────────────┤    │
│  │                                                                 │    │
│  │  ┌────────────────────────────────────────────────────┐        │    │
│  │  │              user table                            │        │    │
│  │  ├────┬──────────┬──────────────┬──────────┬─────────┤        │    │
│  │  │ id │   name   │    email     │ password │  role   │        │    │
│  │  ├────┼──────────┼──────────────┼──────────┼─────────┤        │    │
│  │  │ 1  │ MIT Univ │ admin@mit.edu│ $2b$12.. │ instit. │        │    │
│  │  │ 2  │ John Doe │ john@stu.com │ $2b$12.. │ student │        │    │
│  │  └────┴──────────┴──────────────┴──────────┴─────────┘        │    │
│  │                                                                 │    │
│  │  ┌────────────────────────────────────────────────────┐        │    │
│  │  │           credential table                         │        │    │
│  │  ├────┬─────────┬──────────────┬────────────┬────────┤        │    │
│  │  │ id │ user_id │  skill_name  │issuer_name │  hash  │        │    │
│  │  ├────┼─────────┼──────────────┼────────────┼────────┤        │    │
│  │  │ 1  │    1    │ Python Prog. │ MIT Univ   │ a3f5.. │        │    │
│  │  │ 2  │    1    │ Data Science │ MIT Univ   │ b7d2.. │        │    │
│  │  └────┴─────────┴──────────────┴────────────┴────────┘        │    │
│  │                                                                 │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════
                            SECURITY LAYER
═══════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐    │
│  │  Bcrypt Hashing  │  │  JWT Tokens      │  │  Role-Based      │    │
│  │                  │  │                  │  │  Access Control  │    │
│  │  • Password      │  │  • Stateless     │  │                  │    │
│  │    encryption    │  │    auth          │  │  • Institution   │    │
│  │  • Salt added    │  │  • Expiration    │  │    can issue     │    │
│  │  • One-way       │  │  • Signed with   │  │  • Student       │    │
│  │    function      │  │    secret key    │  │    cannot issue  │    │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘    │
│                                                                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐    │
│  │  SHA-256 Hash    │  │  CORS Enabled    │  │  Input           │    │
│  │                  │  │                  │  │  Validation      │    │
│  │  • Credential    │  │  • Frontend can  │  │                  │    │
│  │    fingerprint   │  │    call backend  │  │  • Required      │    │
│  │  • Unique ID     │  │  • Cross-origin  │  │    fields        │    │
│  │  • Immutable     │  │    requests      │  │  • Email unique  │    │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════
                            DATA FLOW DIAGRAMS
═══════════════════════════════════════════════════════════════════════════

REGISTRATION FLOW:
──────────────────

User → register.html → script.js → POST /register → app.py
                                                       │
                                                       ▼
                                              Check email exists?
                                                       │
                                    ┌──────────────────┴──────────────────┐
                                    │                                     │
                                   Yes                                   No
                                    │                                     │
                                    ▼                                     ▼
                            Return error 400                    Hash password
                                                                        │
                                                                        ▼
                                                                 Create User
                                                                        │
                                                                        ▼
                                                                  Save to DB
                                                                        │
                                                                        ▼
                                                              Return success 201


LOGIN FLOW:
───────────

User → login.html → script.js → POST /login → app.py
                                                  │
                                                  ▼
                                         Find user by email
                                                  │
                                   ┌──────────────┴──────────────┐
                                   │                             │
                                Found                        Not Found
                                   │                             │
                                   ▼                             ▼
                          Verify password                 Return error 401
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                  Valid                       Invalid
                    │                             │
                    ▼                             ▼
            Generate JWT token            Return error 401
                    │
                    ▼
         Return token + role + name
                    │
                    ▼
         Store in localStorage
                    │
                    ▼
         Redirect based on role


CREDENTIAL ISSUANCE FLOW:
─────────────────────────

Institution → issue-credential.html → POST /issue-credential (with JWT)
                                                │
                                                ▼
                                        Validate JWT token
                                                │
                                 ┌──────────────┴──────────────┐
                                 │                             │
                              Valid                        Invalid
                                 │                             │
                                 ▼                             ▼
                          Get user from token          Return error 401
                                 │
                                 ▼
                          Check user role
                                 │
                  ┌──────────────┴──────────────┐
                  │                             │
            institution                    other role
                  │                             │
                  ▼                             ▼
         Validate input fields           Return error 403
                  │
                  ▼
         Generate SHA-256 hash
                  │
                  ▼
         Create Credential object
                  │
                  ▼
         Save to database
                  │
                  ▼
         Return credential details


═══════════════════════════════════════════════════════════════════════════
                         TECHNOLOGY STACK
═══════════════════════════════════════════════════════════════════════════

Backend:                    Frontend:                   Database:
────────                    ─────────                   ─────────
• Python 3.x                • HTML5                     • SQLite
• Flask                     • JavaScript (Vanilla)      • SQLAlchemy ORM
• Flask-Bcrypt              • CSS3                      • 2 tables
• Flask-JWT-Extended        • Fetch API                 • Foreign keys
• Flask-CORS                • localStorage              • Auto-created
• Flask-SQLAlchemy


═══════════════════════════════════════════════════════════════════════════
                         FILE ORGANIZATION
═══════════════════════════════════════════════════════════════════════════

d:\SKILL\
│
├── 📂 backend/              ← All Python/Flask code
│   ├── app.py              ← Main application (4 APIs)
│   ├── models.py           ← Database models (2 models)
│   ├── database.py         ← DB initialization
│   ├── requirements.txt    ← Dependencies
│   └── instance/
│       └── users.db        ← SQLite database
│
├── 📂 frontend/             ← All HTML/JS/CSS
│   ├── register.html       ← Registration page
│   ├── login.html          ← Login page
│   ├── issue-credential.html ← Issue credential page
│   ├── script.js           ← JavaScript functions
│   └── style.css           ← Styling
│
└── 📂 Documentation/        ← All guides
    ├── README.md           ← Main documentation
    ├── QUICK_START.md      ← Quick guide
    ├── API_TESTING_GUIDE.md ← API examples
    ├── HOW_IT_WORKS.md     ← Technical details
    └── PROJECT_SUMMARY.md  ← Overview


═══════════════════════════════════════════════════════════════════════════
                    FUTURE ARCHITECTURE (Planned)
═══════════════════════════════════════════════════════════════════════════

Current:                              Future:
────────                              ───────

Frontend ──→ Backend ──→ SQLite       Frontend ──→ Backend ──→ Blockchain
                                                      │              │
                                                      │              ▼
                                                      │         Smart Contract
                                                      │              │
                                                      ▼              ▼
                                                  PostgreSQL    Credential
                                                      │         Verification
                                                      │              │
                                                      ▼              ▼
                                                  Federated     Immutable
                                                  Learning       Record
                                                      │
                                                      ▼
                                                  ML Model
                                                  (Skill Rec.)
