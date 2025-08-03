// Sayfa yüklendiğinde token kontrolü yap
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    
    // Eğer token varsa ve geçerliyse dashboard'a yönlendir
    if (token) {
        // Token'ın geçerliliğini kontrol et
        fetch('http://localhost:3000/api/auth/verify', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/pages/dashboard.html';
            } else {
                // Token geçersizse localStorage'ı temizle
                localStorage.removeItem('token');
                localStorage.removeItem('user');
            }
        })
        .catch(err => {
            console.error('Token doğrulama hatası:', err);
            localStorage.removeItem('token');
            localStorage.removeItem('user');
        });
    }
});
