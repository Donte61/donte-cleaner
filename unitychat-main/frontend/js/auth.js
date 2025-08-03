const API_URL = 'http://localhost:3000/api';

function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

function showSuccess(message) {
    const successDiv = document.getElementById('success-message');
    successDiv.textContent = message;
    successDiv.style.display = 'block';
    setTimeout(() => {
        successDiv.style.display = 'none';
    }, 3000);
}

function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validatePassword(password) {
    return password.length >= 6;
}

async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        showError('Tüm alanları doldurunuz');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Giriş başarısız');
        }

        showSuccess('Giriş başarılı! Yönlendiriliyorsunuz...');
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));

        setTimeout(() => {
            window.location.href = 'pages/dashboard.html';
        }, 1000);
    } catch (err) {
        showError(err.message);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const passwordConfirm = document.getElementById('password_confirm').value;
    const displayName = document.getElementById('display_name').value;

    // Validasyonlar
    if (!username || !email || !password || !passwordConfirm) {
        showError('Tüm zorunlu alanları doldurunuz');
        return;
    }

    if (!validateEmail(email)) {
        showError('Geçerli bir e-posta adresi giriniz');
        return;
    }

    if (!validatePassword(password)) {
        showError('Şifre en az 6 karakter olmalıdır');
        return;
    }

    if (password !== passwordConfirm) {
        showError('Şifreler eşleşmiyor');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                email,
                password,
                display_name: displayName || username
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Kayıt başarısız');
        }

        showSuccess('Kayıt başarılı! Yönlendiriliyorsunuz...');
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));

        setTimeout(() => {
            window.location.href = 'pages/dashboard.html';
        }, 1000);
    } catch (err) {
        showError(err.message);
    }
}

// Sayfa yüklendiğinde token kontrolü
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (token) {
        window.location.href = '/dashboard.html';
    }

    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (loginForm) loginForm.addEventListener('submit', handleLogin);
    if (registerForm) registerForm.addEventListener('submit', handleRegister);
});
