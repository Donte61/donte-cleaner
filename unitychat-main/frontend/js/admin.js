// Add utility functions at the top
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function showError(message) {
    showNotification(message, 'error');
}

function showSuccess(message) {
    showNotification(message, 'success');
}

// Remove this line since it's now in config.js
// const API_URL = 'http://localhost:3000/api';

// Admin Commands
async function handleAdminCommand(text) {
    if (!currentUser?.is_admin) return false;
    
    const [command, ...args] = text.split(' ');
    const params = {};

    try {
        switch (command) {
            case '/ban':
                if (args.length < 1) {
                    showNotification('Kullanım: /ban <kullanıcı> [sebep]', 'error');
                    return true;
                }
                params.username = args[0];
                params.reason = args.slice(1).join(' ') || 'Sebep belirtilmedi';
                break;

            case '/unban':
                if (args.length < 1) {
                    showNotification('Kullanım: /unban <kullanıcı>', 'error');
                    return true;
                }
                params.username = args[0];
                break;

            // ...rest of the commands...
        }

        const response = await fetch(`${API_URL}/admin/command`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ command, params })
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error);
        }

        showNotification(data.message, 'success');
        loadMessages();
    } catch (err) {
        showNotification(err.message, 'error');
    }

    return true;
}

async function sendAdminCommand(command, params = {}) {
    try {
        console.log('Sending admin command:', { command, params }); // Debug log

        const response = await fetch(`${API_URL}/admin/command`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ command, params })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Komut başarısız oldu');
        }

        const data = await response.json();
        showNotification(data.message, 'success');
        await loadMessages();
    } catch (err) {
        console.error('Admin command error:', err);
        showNotification(err.message, 'error');
        throw err;
    }
}

function showAdminHelp() {
    const commands = [
        { command: '/clear', desc: 'Tüm mesajları siler' },
        { command: '/ban [kullanıcı] [sebep]', desc: 'Kullanıcıyı banlar' },
        { command: '/unban [kullanıcı]', desc: 'Kullanıcının banını kaldırır' },
        { command: '/mute [kullanıcı] [süre]', desc: 'Kullanıcıyı susturur' },
        { command: '/edit [mesaj_id] [yeni_mesaj]', desc: 'Mesajı düzenler' },
        { command: '/announce [mesaj]', desc: 'Duyuru yapar' },
        { command: '/help', desc: 'Bu yardım menüsünü gösterir' }
    ];

    const helpModal = document.createElement('div');
    helpModal.className = 'modal';
    helpModal.innerHTML = `
        <div class="modal-content">
            <h2>Admin Komutları</h2>
            <table>
                ${commands.map(cmd => `
                    <tr>
                        <td><code>${cmd.command}</code></td>
                        <td>${cmd.desc}</td>
                    </tr>
                `).join('')}
            </table>
            <button onclick="this.parentElement.parentElement.remove()">Kapat</button>
        </div>
    `;
    document.body.appendChild(helpModal);
}

function createContextMenu(event, messageId, username) {
    event.preventDefault();
    
    removeContextMenu();
    
    const contextMenu = document.createElement('div');
    contextMenu.className = 'context-menu';
    contextMenu.innerHTML = `
        <div class="context-menu-item" onclick="editMessage(${messageId})">
            <i>✏️</i> Mesajı Düzenle
        </div>
        <div class="context-menu-item" onclick="deleteMessage(${messageId})">
            <i>🗑️</i> Mesajı Sil
        </div>
        <div class="context-menu-item danger" onclick="banUser('${username}')">
            <i>🚫</i> Kullanıcıyı Banla
        </div>
        <div class="context-menu-item" onclick="muteUser('${username}')">
            <i>🔇</i> Sustur
        </div>
    `;
    
    contextMenu.style.top = `${event.pageY}px`;
    contextMenu.style.left = `${event.pageX}px`;
    document.body.appendChild(contextMenu);
}

function removeContextMenu() {
    const existingMenu = document.querySelector('.context-menu');
    if (existingMenu) {
        existingMenu.remove();
    }
}

// Admin user actions
async function banUser(username) {
    const reason = prompt('Ban sebebi:');
    if (!reason) return;
    await sendAdminCommand('/ban', { username, reason });
}

async function muteUser(username) {
    const duration = prompt('Susturma süresi (dakika):');
    if (!duration) return;
    await sendAdminCommand('/mute', { username, duration });
}

// Helper function for notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Admin UI initialization
function initializeAdminUI() {
    const adminMenu = document.getElementById('admin-menu');
    if (currentUser?.is_admin) {
        adminMenu.style.display = 'block';
    }
}

// Update the admin list functions
async function showBanList() {
    try {
        const response = await fetch(`${API_URL}/admin/bans`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (!response.ok) throw new Error('Banlı kullanıcılar alınamadı');

        const bans = await response.json();
        
        const modal = document.createElement('div');
        modal.className = 'admin-modal';
        modal.innerHTML = `
            <h2>Banlı Kullanıcılar</h2>
            <div class="user-list">
                ${bans.length ? bans.map(ban => `
                    <div class="user-item">
                        <div>
                            <strong>${ban.username}</strong>
                            <p>Sebep: ${ban.reason}</p>
                            <small>Ban Tarihi: ${new Date(ban.ban_date).toLocaleString()}</small>
                        </div>
                        <div class="user-actions">
                            <button onclick="unbanUser('${ban.username}')" class="unban-btn">
                                Ban Kaldır
                            </button>
                        </div>
                    </div>
                `).join('') : '<p>Banlı kullanıcı bulunmuyor</p>'}
            </div>
            <button onclick="this.parentElement.remove()" class="modal-close">Kapat</button>
        `;
        document.body.appendChild(modal);
    } catch (err) {
        showNotification(err.message, 'error');
    }
}

async function showMutedList() {
    try {
        const response = await fetch(`${API_URL}/admin/mutes`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (!response.ok) throw new Error('Susturulan kullanıcılar alınamadı');

        const mutes = await response.json();
        
        const modal = document.createElement('div');
        modal.className = 'admin-modal';
        modal.innerHTML = `
            <h2>Susturulan Kullanıcılar</h2>
            <div class="user-list">
                ${mutes.length ? mutes.map(mute => `
                    <div class="user-item">
                        <div>
                            <strong>${mute.username}</strong>
                            <p>Süre: ${mute.duration_minutes} dakika</p>
                            <small>Bitiş: ${new Date(mute.unmute_time).toLocaleString()}</small>
                        </div>
                        <div class="user-actions">
                            <button class="unmute-btn" onclick="handleAdminCommand('/unmute ${mute.username}')">
                                Susturmayı Kaldır
                            </button>
                        </div>
                    </div>
                `).join('') : '<p>Susturulan kullanıcı bulunmuyor</p>'}
            </div>
            <button onclick="this.parentElement.remove()">Kapat</button>
        `;
        document.body.appendChild(modal);
    } catch (err) {
        showError('Susturulan kullanıcılar yüklenemedi');
    }
}

async function showUserList() {
    try {
        const response = await fetch(`${API_URL}/admin/users`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (!response.ok) throw new Error('Kullanıcı listesi alınamadı');

        const users = await response.json();
        
        const modal = document.createElement('div');
        modal.className = 'admin-modal';
        modal.innerHTML = `
            <h2>Tüm Kullanıcılar</h2>
            <div class="user-list">
                ${users.map(user => `
                    <div class="user-item">
                        <div>
                            <strong>${user.username}</strong>
                            ${user.is_online ? '🟢' : '⚪️'}
                            ${user.is_admin ? '👑' : ''}
                        </div>
                        <div class="user-actions">
                            <button onclick="handleAdminCommand('/ban ${user.username}')">Ban</button>
                            <button onclick="handleAdminCommand('/mute ${user.username}')">Sustur</button>
                        </div>
                    </div>
                `).join('')}
            </div>
            <button onclick="this.parentElement.remove()">Kapat</button>
        `;
        document.body.appendChild(modal);
    } catch (err) {
        showError('Kullanıcı listesi yüklenemedi');
    }
}

// Muted List Management
async function showMutedList() {
    try {
        const response = await fetch(`${API_URL}/admin/mutes`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const mutes = await response.json();

        const modal = document.createElement('div');
        modal.className = 'admin-modal';
        modal.innerHTML = `
            <h2>Susturulan Kullanıcılar</h2>
            <div class="user-list">
                ${mutes.map(mute => `
                    <div class="user-item">
                        <span>${mute.username} - ${mute.duration_minutes} dakika</span>
                        <div class="user-actions">
                            <button class="unmute-btn" onclick="unmuteUser('${mute.username}')">
                                Susturmayı Kaldır
                            </button>
                        </div>
                    </div>
                `).join('') || '<p>Susturulan kullanıcı yok</p>'}
            </div>
            <button onclick="this.parentElement.remove()" style="margin-top: 20px">Kapat</button>
        `;
        document.body.appendChild(modal);
    } catch (err) {
        showError('Susturulan kullanıcılar yüklenemedi');
    }
}

// Announcement Form
function showAnnouncementForm() {
    const modal = document.createElement('div');
    modal.className = 'admin-modal';
    modal.innerHTML = `
        <h2>Duyuru Yap</h2>
        <textarea 
            id="announcement-text" 
            style="width: 100%; min-height: 100px; margin: 10px 0; padding: 8px;"
            placeholder="Duyuru mesajını yazın..."
        ></textarea>
        <div style="display: flex; gap: 10px; justify-content: flex-end;">
            <button onclick="sendAnnouncement()">Gönder</button>
            <button onclick="this.parentElement.parentElement.remove()">İptal</button>
        </div>
    `;
    document.body.appendChild(modal);
}

async function sendAnnouncement() {
    const text = document.getElementById('announcement-text').value;
    if (!text) return;

    try {
        await sendAdminCommand('/announce', { message: text });
        document.querySelector('.admin-modal').remove();
    } catch (err) {
        showError('Duyuru gönderilemedi');
    }
}

// User List Management
async function showUserList() {
    try {
        const response = await fetch(`${API_URL}/admin/users`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const users = await response.json();

        const modal = document.createElement('div');
        modal.className = 'admin-modal';
        modal.innerHTML = `
            <h2>Tüm Kullanıcılar</h2>
            <div class="user-list">
                ${users.map(user => `
                    <div class="user-item">
                        <span>${user.username} ${user.is_online ? '🟢' : '⚪'}</span>
                        <div class="user-actions">
                            <button onclick="banUser('${user.username}')">Ban</button>
                            <button onclick="muteUser('${user.username}')">Sustur</button>
                        </div>
                    </div>
                `).join('')}
            </div>
            <button onclick="this.parentElement.remove()" style="margin-top: 20px">Kapat</button>
        `;
        document.body.appendChild(modal);
    } catch (err) {
        showError('Kullanıcı listesi yüklenemedi');
    }
}

// Initialize admin UI when page loads
document.addEventListener('DOMContentLoaded', () => {
    if (currentUser?.is_admin) {
        initializeAdminUI();
    }
});

// Export admin functions
window.handleAdminCommand = handleAdminCommand;
window.createContextMenu = createContextMenu;
window.removeContextMenu = removeContextMenu;
window.banUser = banUser;
window.muteUser = muteUser;
window.showAdminHelp = showAdminHelp;
window.showNotification = showNotification;

// Admin user management functions
async function unmuteUser(username) {
    try {
        await sendAdminCommand('/unmute', { username });
        showNotification(`${username} kullanıcısının susturulması kaldırıldı`, 'success');
        showMutedList(); // Listeyi yenile
    } catch (err) {
        showNotification('Susturma kaldırılamadı', 'error');
    }
}

async function clearAllMessages() {
    if (!confirm('Tüm mesajları silmek istediğinize emin misiniz?')) return;
    
    try {
        await sendAdminCommand('/clear');
        showNotification('Tüm mesajlar silindi', 'success');
        loadMessages(); // Chat'i yenile
    } catch (err) {
        showNotification('Mesajlar silinemedi', 'error');
    }
}

// Admin list helper functions
function showAdminList(title, items, renderItem) {
    const modal = document.createElement('div');
    modal.className = 'admin-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <h2>${title}</h2>
            <div class="user-list">
                ${items.length ? items.map(renderItem).join('') : `<p>Kayıt bulunamadı</p>`}
            </div>
            <button onclick="this.parentElement.parentElement.remove()" class="modal-close">Kapat</button>
        </div>
    `;
    document.body.appendChild(modal);
}

// Admin commands handler
async function handleAdminCommand(command, params = {}) {
    try {
        const response = await fetch(`${API_URL}/admin/command`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ command, params })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Komut çalıştırılamadı');
        }

        const data = await response.json();
        showNotification(data.message, 'success');
        await loadMessages();
    } catch (err) {
        showNotification(err.message, 'error');
    }
}

// Additional admin functions
async function showAnnouncementForm() {
    const modal = document.createElement('div');
    modal.className = 'admin-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <h2>Duyuru Yap</h2>
            <textarea id="announcement-text" placeholder="Duyuru mesajını yazın..." 
                      style="width: 100%; min-height: 100px; margin: 10px 0; padding: 8px;"></textarea>
            <div class="modal-buttons">
                <button onclick="sendAnnouncement()">Gönder</button>
                <button onclick="this.parentElement.parentElement.parentElement.remove()">İptal</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

async function sendAnnouncement() {
    const text = document.getElementById('announcement-text').value.trim();
    if (!text) return;

    try {
        await handleAdminCommand('/announce', { message: text });
        document.querySelector('.admin-modal').remove();
    } catch (err) {
        showNotification('Duyuru gönderilemedi', 'error');
    }
}

// Make functions available globally
window.unmuteUser = unmuteUser;
window.clearAllMessages = clearAllMessages;
window.showAnnouncementForm = showAnnouncementForm;
window.sendAnnouncement = sendAnnouncement;

// Add these lines at the end of the file
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-close')) {
        e.target.closest('.admin-modal').remove();
    }
});

async function unbanUser(username) {
    try {
        // Fix: Add proper parameters for /unban command
        await sendAdminCommand('/unban', { username: username });
        showNotification(`${username} kullanıcısının banı kaldırıldı`, 'success');
        await loadMessages(); // Refresh messages
        showBanList(); // Refresh ban list
    } catch (err) {
        showNotification(err.message || 'Ban kaldırma işlemi başarısız oldu', 'error');
    }
}

// Make sure functions are globally available
window.unbanUser = unbanUser;
window.showBanList = showBanList;

// ...existing code...

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/index.html';
        return;
    }

    try {
        // Kullanıcı bilgilerini yükle
        const storedUser = localStorage.getItem('user');
        if (!storedUser) {
            throw new Error('User info not found');
        }

        currentUser = JSON.parse(storedUser);

        // Admin menüsünü sadece admin kullanıcılara göster
        const adminMenu = document.getElementById('admin-menu');
        if (adminMenu) {
            adminMenu.style.display = currentUser.is_admin ? 'block' : 'none';
        }

        // Diğer admin.js kodları...
    } catch (err) {
        console.error('User loading error:', err);
        window.location.href = '/index.html';
    }
});

// ...existing code...
