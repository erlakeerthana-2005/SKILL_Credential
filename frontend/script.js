// API Configuration
const API_BASE_URL = "http://127.0.0.1:5000";

// Global Toast System
const toastContainer = document.createElement('div');
toastContainer.id = 'toast-container';
document.body.appendChild(toastContainer);

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${type === 'success' ? '✓' : 'ℹ'}</span> ${message}`;
    toastContainer.appendChild(toast);

    // Animate in
    setTimeout(() => toast.classList.add('show'), 10);

    // Animate out and remove
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 500);
    }, 4000);
}

// Function to register a new user (Step 1: Details)
function register() {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("confirm_password").value;
    const role = document.getElementById("role").value;
    const institution_name = document.getElementById("institution_name").value.trim();

    // Comprehensive Validation
    if (!name || !email || !password || !confirm_password) {
        showToast("Please fill in all required fields", "error");
        return;
    }

    if (!email.includes("@") || !email.includes(".")) {
        showToast("Please enter a valid email address", "error");
        return;
    }

    if (password !== confirm_password) {
        showToast("Passwords do not match", "error");
        return;
    }

    if (password.length < 6) {
        showToast("Password must be at least 6 characters", "error");
        return;
    }

    const regBtn = document.getElementById("regBtn");
    regBtn.disabled = true;
    regBtn.textContent = "Sending OTP...";

    fetch(`${API_BASE_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name: name,
            email: email,
            password: password,
            confirm_password: confirm_password,
            role: role,
            institution_name: institution_name
        })
    })
        .then(res => res.json())
        .then(data => {
            regBtn.disabled = false;
            regBtn.textContent = "Create Secure Account";

            if (data.message && data.message.includes("OTP sent")) {
                showToast(data.message, "success");
                // Transition to OTP view
                document.getElementById("registrationForm").style.display = "none";
                document.getElementById("otpSection").style.display = "block";
            } else {
                showToast(data.message || "Server Error", "error");
            }
        })
        .catch(err => {
            console.error("Registration Fetch Error:", err);
            regBtn.disabled = false;
            regBtn.textContent = "Create Secure Account";
            showToast("Connection Fail. Is the Flask server (D:\\SKILL\\start-backend.bat) running on port 5000?", "error");
        });
}

// Step 2: Verify OTP
function verifyOTP() {
    const email = document.getElementById("email").value;
    const otp = document.getElementById("otp").value;

    if (otp.length !== 6) {
        showToast("Enter a valid 6-digit OTP", "error");
        return;
    }

    fetch(`${API_BASE_URL}/verify-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, otp: otp })
    })
        .then(res => res.json())
        .then(data => {
            if (data.verified) {
                showToast(data.message, "success");
                setTimeout(() => window.location.href = "login.html", 1500);
            } else {
                showToast(data.message || "Invalid OTP", "error");
            }
        })
        .catch(err => {
            console.error("OTP Verification Error:", err);
            showToast("Check Server Connection.", "error");
        });
}

// Helper: Go back to register form
function showRegisterForm() {
    document.getElementById("otpSection").style.display = "none";
    document.getElementById("registrationForm").style.display = "block";
}

// UI: Show/Hide Institute field based on role
function toggleInstituteField() {
    const role = document.getElementById("role").value;
    const instField = document.getElementById("instField");
    if (role === 'student') {
        instField.style.display = 'block';
    } else {
        instField.style.display = 'none';
        document.getElementById("institution_name").value = "";
    }
}

// Function to login user
function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;


    // Normal login for other users
    fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.token) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('role', data.role);
                localStorage.setItem('name', data.name);
                localStorage.setItem('user_id', data.user_id);
                if (data.institution) localStorage.setItem('institution', data.institution);

                showToast("Identity Verified. Welcome " + data.name, "success");

                setTimeout(() => {
                    if (data.role === 'institution') {
                        window.location.href = "institution-dashboard.html";
                    } else if (data.role === 'admin') {
                        window.location.href = "admin-dashboard.html";
                    } else {
                        window.location.href = "student-dashboard.html";
                    }
                }, 1200);
            } else {
                showToast(data.message || "Auth Failed", "error");
            }
        })
        .catch(err => {
            console.error("Login Fetch Error:", err);
            showToast("Server Unavailable. Flask failed.", "error");
        });
}

// Function to logout
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('name');
    showToast("Session Terminated. Redirecting...", "info");
    setTimeout(() => window.location.href = "login.html", 1000);
}


