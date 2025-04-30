// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8000/api'; // Update with your actual API URL

// DOM Elements
const loginForm = document.getElementById('loginForm');
const loginAlert = document.getElementById('loginAlert');
const registerForm = document.getElementById('registerForm');
const registerAlert = document.getElementById('registerAlert');
const departmentSelect = document.getElementById('department');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    console.log('Application initialized');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }

    // Load departments for police registration
    if (departmentSelect) {
        loadDepartments();
    }
});

// Load Departments for Police Registration
async function loadDepartments() {
    try {
        const response = await fetch(`${API_BASE_URL}/departments/`);
        const data = await response.json();
        
        if (response.ok) {
            departmentSelect.innerHTML = '<option value="">Select Department</option>' +
                data.map(dept => `<option value="${dept.id}">${dept.name}</option>`).join('');
        } else {
            console.error('Failed to load departments:', data.detail);
        }
    } catch (error) {
        console.error('Error loading departments:', error);
    }
}

// Login Handler
async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                password
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Store the token in localStorage
            localStorage.setItem('token', data.access);
            localStorage.setItem('refreshToken', data.refresh);
            localStorage.setItem('userType', data.user_type);
            localStorage.setItem('username', username);

            // Redirect based on user type
            switch(data.user_type) {
                case 1: // Regular User
                    window.location.href = 'dashboard-user.html';
                    break;
                case 2: // Police Officer
                    window.location.href = 'dashboard-police.html';
                    break;
                case 3: // Department Admin
                    window.location.href = 'dashboard-admin.html';
                    break;
                default:
                    showAlert(loginAlert, 'Invalid user type', 'danger');
            }
        } else {
            showAlert(loginAlert, data.detail || 'Login failed', 'danger');
        }
    } catch (error) {
        console.error('Login error:', error);
        showAlert(loginAlert, 'An error occurred during login. Please check your connection and try again.', 'danger');
    }
}

// Registration Handler
async function handleRegister(e) {
    e.preventDefault();
    console.log('Registration form submitted');

    // Get the current page URL to determine user type
    const currentPage = window.location.pathname;
    let userType, formData, redirectPage;

    if (currentPage.includes('register-user.html')) {
        userType = 1; // Regular User
        redirectPage = 'login-user.html';
        formData = {
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            phone: document.getElementById('phone').value,
            address: document.getElementById('address').value,
            user_type: userType
        };
    } else if (currentPage.includes('register-police.html')) {
        userType = 2; // Police Officer
        redirectPage = 'login-police.html';
        formData = {
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            phone: document.getElementById('phone').value,
            address: document.getElementById('address').value,
            user_type: userType,
            police_id: document.getElementById('policeId').value,
            department: document.getElementById('department').value
        };
    } else if (currentPage.includes('register-department.html')) {
        userType = 3; // Department Admin
        redirectPage = 'login-admin.html';
        formData = {
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            phone: document.getElementById('phone').value,
            address: document.getElementById('address').value,
            user_type: userType,
            department_name: document.getElementById('departmentName').value,
            department_location: document.getElementById('departmentLocation').value
        };
    }

    console.log('Registration attempt for user type:', userType);

    try {
        const response = await fetch(`${API_BASE_URL}/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        const data = await response.json();
        console.log('Registration response:', {
            status: response.status,
            data: data
        });

        if (response.ok) {
            console.log('Registration successful');
            showAlert(registerAlert, 'Registration successful! Redirecting to login...', 'success');
            window.location.href = redirectPage;
            // setTimeout(() => {
            // }, 1500);
        } else {
            console.error('Registration failed:', data.detail);
            showAlert(registerAlert, data.detail || 'Registration failed. Please try again.', 'danger');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showAlert(registerAlert, 'An error occurred during registration. Please try again.', 'danger');
    }
}

// Alert Helper Function
function showAlert(element, message, type) {
    if (!element) return;
    
    element.textContent = message;
    element.className = `alert alert-${type} mt-3`;
    element.style.display = 'block';
    
    // Hide alert after 5 seconds
    setTimeout(() => {
        element.style.display = 'none';
    }, 5000);
}

// Check authentication on dashboard pages
function checkAuth() {
    const token = localStorage.getItem('token');
    const userType = localStorage.getItem('userType');
    const currentPage = window.location.pathname.split('/').pop();

    if (!token) {
        // Redirect to appropriate login page
        switch(currentPage) {
            case 'dashboard-user.html':
                window.location.href = 'login-user.html';
                break;
            case 'dashboard-police.html':
                window.location.href = 'login-police.html';
                break;
            case 'dashboard-admin.html':
                window.location.href = 'login-admin.html';
                break;
        }
        return;
    }

    // Check if user is on the correct dashboard
    const expectedUserType = currentPage.split('-')[1].split('.')[0];
    if (userType !== expectedUserType) {
        // Redirect to correct dashboard
        switch(userType) {
            case 'regular':
                window.location.href = 'dashboard-user.html';
                break;
            case 'police':
                window.location.href = 'dashboard-police.html';
                break;
            case 'department_admin':
                window.location.href = 'dashboard-admin.html';
                break;
        }
    }
}

// Logout functionality
document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
});

function handleLogout() {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('userType');
    localStorage.removeItem('username');
    
    // Redirect to appropriate login page based on current page
    const currentPage = window.location.pathname.split('/').pop();
    switch(currentPage) {
        case 'dashboard-user.html':
            window.location.href = 'login-user.html';
            break;
        case 'dashboard-police.html':
            window.location.href = 'login-police.html';
            break;
        case 'dashboard-admin.html':
            window.location.href = 'login-admin.html';
            break;
    }
}

// Check authentication when loading dashboard pages
if (window.location.pathname.includes('dashboard')) {
    checkAuth();
} 