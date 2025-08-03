let currentUser = null;
let lastMessageId = 0;
let messageCache = [];
let typingTimeout;
let tags = [];
let currentGuild = null;
const searchInput = document.getElementById('search-input');
const emojiShortcuts = {
    ':)': '😊',
    ':D': '😀',
    ':(': '☹️',
    ';)': '😉',
    ':p': '😛',
    '<3': '❤️',
    ':*': '😘',
    ':o': '😮',
    ':|': '😐',
    ':@': '😠',
    ':s': '😕',
    ':+1:': '👍',
    ':heart:': '❤️',
    ':fire:': '🔥'
};

const emojiCategories = {
    smileys: ['😀', '😃', '😄', '😁', '😅', '😂', '🤣', '😊', '😇', '🙂', '😉', '😌', '😍', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜'],
    gestures: ['👍', '👎', '👌', '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆', '👇', '☝️', '👊', '✊', '🤛', '🤜', '✍️', '👏', '🙌', '👐'],
    hearts: ['❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '💕', '💞', '💓', '💗', '💖', '💘', '💝']
};

// DOM Elemanları
const messagesContainer = document.getElementById('messages');
const messageInput = document.getElementById('message-text');
const sendButton = document.getElementById('send-message');
const userDisplayName = document.getElementById('user-displayname');
const userAvatar = document.getElementById('user-avatar');
const logoutButton = document.getElementById('logout-btn');
const typingIndicator = document.getElementById('typing-indicator');

// Fetch tags from the database
async function fetchTags() {
    try {
        const response = await fetch(`${API_URL}/tags`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        if (!response.ok) throw new Error('Taglar yüklenemedi');
        tags = await response.json();
        console.log('Fetched tags:', tags); // Debug log
    } catch (err) {
        console.error('Tag yükleme hatası:', err);
    }
}

// Fetch announcements from the database
async function fetchAnnouncements() {
    try {
        const response = await fetch(`${API_URL}/announcements`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        if (!response.ok) throw new Error('Duyurular yüklenemedi');
        const announcements = await response.json();
        displayAnnouncements(announcements);
    } catch (err) {
        console.error('Duyuru yükleme hatası:', err);
    }
}

// Display announcements
function displayAnnouncements(announcements) {
    const announcementsContainer = document.getElementById('announcements');
    if (!announcements || announcements.length === 0) {
        announcementsContainer.style.display = 'none';
        return;
    }

    announcementsContainer.style.display = 'block';
    announcementsContainer.innerHTML = announcements.map(announcement => `
        <div class="announcement-item">
            <div class="announcement-emoji">📢</div>
            <div class="announcement-text">
                ${announcement.message}
                <div class="announcement-time">
                    ${new Date(announcement.created_at).toLocaleString()}
                </div>
            </div>
        </div>
    `).join('');

    // Duyuru varsa margins'i ayarla
    const messagesContainer = document.querySelector('.messages');
    if (messagesContainer) {
        const announcementsHeight = announcementsContainer.offsetHeight;
        messagesContainer.style.height = `calc(100vh - ${180 + announcementsHeight}px)`;
    }
}

// Kullanıcı ve mesajları başlat
async function initializeChat() {
    try {
        const userJson = localStorage.getItem('user');
        if (!userJson) {
            window.location.href = '../index.html';
            return;
        }

        currentUser = JSON.parse(userJson);
        const adminMenu = document.getElementById('admin-menu');
        
        // Admin menüsünü sadece admin kullanıcılara göster
        if (adminMenu) {
            adminMenu.style.display = currentUser.is_admin ? 'block' : 'none';
        }

        // Kullanıcı bilgilerini ayarla
        userDisplayName.textContent = currentUser.display_name || currentUser.username;
        userAvatar.src = '../avatar/default-avatar.png'; // Use default avatar

        // Tagları yükle
        await fetchTags();

        // Duyuruları yükle
        await fetchAnnouncements();

        // Mesaj geçmişini yükle
        await loadMessages();
        
        // Periyodik güncelleme
        setInterval(loadMessages, 3000);
        setInterval(updateUserData, 30000); // Her 30 saniyede bir güncelle

        updateUserStats(); // İlk yükleme
        setInterval(updateUserStats, 30000); // Her 30 saniyede bir güncelle
    } catch (err) {
        console.error('Chat initialization error:', err);
        window.location.href = '../index.html';
    }
}

// Kimlik doğrulama kontrolü
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

        userDisplayName.textContent = currentUser.display_name || currentUser.username;
        userAvatar.src = currentUser.avatar_url || 'https://via.placeholder.com/50';

        // Mesajları yükle
        loadMessages();
    } catch (err) {
        console.error('User loading error:', err);
        window.location.href = '/index.html';
    }
});

// Mesajları yükle ve okundu bilgisi güncelle
async function loadMessages() {
    try {
        const token = localStorage.getItem('token');
        if (!token) throw new Error('Token bulunamadı');

        const response = await fetch(`${API_URL}/messages`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) throw new Error('Mesajlar yüklenemedi');

        const messages = await response.json();
        displayMessages(messages.reverse()); // En eski mesajlar üstte olacak şekilde sırala

        // Okundu bilgisi güncelle
        messages.forEach(msg => {
            if (msg.read_by && !msg.read_by.includes(currentUser.username)) {
                updateReadStatus(msg.id);
            }
        });
    } catch (err) {
        console.error('Mesaj yükleme hatası:', err);
    }
}

// Add console log to debug tag determination
function determineTag(userLevel) {
    console.log('Determining tag for level:', userLevel); // Debug log
    console.log('Available tags:', tags); // Debug log
    
    if (!userLevel || userLevel < 1) {
        userLevel = 1;
    }
    
    if (!tags || !tags.length) {
        return { name: 'Unknown', color_hex: '#000000' };
    }

    // Sort tags by required_level in ascending order
    const sortedTags = [...tags].sort((a, b) => a.required_level - b.required_level);
    
    // Find the highest matching tag
    let appropriateTag = sortedTags[0]; // Default to lowest tag
    
    for (const tag of sortedTags) {
        if (userLevel >= tag.required_level) {
            appropriateTag = tag;
        } else {
            break; // Stop when we find a level requirement that's too high
        }
    }
    
    console.log('Selected tag:', appropriateTag); // Debug log
    return appropriateTag;
}

// Update message display code to properly handle user level
function displayMessageWithTag(msg) {
    console.log('Message data in displayMessageWithTag:', msg); // Debug log
    const tag = determineTag(msg.user_level);
    return `
        <div class="message-tag-container">
            <span class="message-tag" style="color: ${tag.color_hex}; border: 1px solid ${tag.color_hex}">
                [${tag.name}]
            </span>
            <span class="message-author">${msg.display_name || msg.username}</span>
        </div>
    `;
}

// Mesajları uygun admin kontrolleri ile göster
function displayMessages(messages) {
    if (!currentUser) return;

    const messagesContainer = document.querySelector('.messages-container');
    const sortedMessages = [...messages].sort((a, b) => 
        new Date(a.created_at) - new Date(b.created_at)
    );

    messagesContainer.innerHTML = sortedMessages.map(msg => {
        // Tepkileri parse et
        let reactions = [];
        try {
            if (msg.reactions) {
                const parsed = JSON.parse(msg.reactions);
                reactions = parsed.reactions || [];
            }
        } catch (err) {
            console.error('Tepki parse hatası:', err);
            reactions = [];
        }

        // Tepki sayılarını hesapla
        const thumbsUpCount = reactions.filter(r => r.reaction === '👍').length;
        const heartCount = reactions.filter(r => r.reaction === '❤️').length;
        
        // Kullanıcının tepkilerini kontrol et
        const hasThumbsUp = reactions.some(r => r.userId === currentUser.id && r.reaction === '👍');
        const hasHeart = reactions.some(r => r.userId === currentUser.id && r.reaction === '❤️');

        // Mesaj tipine göre HTML oluştur
        if (msg.message_type === 'system') {
            return `
                <div class="message system">
                    <div class="message-text">${msg.message}</div>
                </div>
            `;
        }

        if (msg.message_type === 'announcement') {
            return `
                <div class="message announcement">
                    <div class="message-text">📢 ${msg.message}</div>
                </div>
            `;
        }

        const isAdmin = Boolean(msg.is_admin);
        const isOwnMessage = msg.user_id === currentUser.id;
        const messageClass = `message ${isAdmin ? 'admin-message' : ''} ${isOwnMessage ? 'own-message' : ''}`;

        const quotedMessage = msg.quoted_text ? `
            <div class="quoted-message">
                <div class="quoted-author">${msg.quoted_author}</div>
                <div class="quoted-text">${msg.quoted_text}</div>
            </div>
        ` : '';

        // Log the message object to debug
        console.log('Message data:', msg); // Debug log
        
        // Get user level from message
        const userLevel = parseInt(msg.user_level) || 1;
        const tag = determineTag(userLevel);
        
        console.log(`Message from ${msg.username}, Level: ${userLevel}, Tag:`, tag); // Debug log

        const messageActions = `
            <div class="message-actions">
                <button class="message-action-btn" onclick="quoteMessage(${msg.id})">
                    <i>💬</i> Alıntıla
                </button>
                <button class="message-action-btn" onclick="forwardMessage(${msg.id})">
                    <i>↪️</i> İlet
                </button>
                <button class="message-action-btn ${hasThumbsUp ? 'active' : ''}" 
                        onclick="reactToMessage(${msg.id}, '👍')">
                    <i>👍</i>
                    ${thumbsUpCount > 0 ? `<span class="count">${thumbsUpCount}</span>` : ''}
                </button>
                <button class="message-action-btn ${hasHeart ? 'active' : ''}"
                        onclick="reactToMessage(${msg.id}, '❤️')">
                    <i>❤️</i>
                    ${heartCount > 0 ? `<span class="count">${heartCount}</span>` : ''}
                </button>
            </div>
        `;

        return `
            <div class="${messageClass}" data-message-id="${msg.id}" data-username="${msg.username}">
                <div class="message-wrapper" ${currentUser.is_admin ? `oncontextmenu="handleContextMenu(event, ${msg.id}, '${msg.username}')"` : ''}>
                    ${messageActions} <!-- Move actions above the header -->
                    <img src="../avatar/default-avatar.png" alt="" class="message-avatar"> <!-- Use default avatar -->
                    <div class="message-content">
                        ${quotedMessage}
                        <div class="message-header">
                            <span class="message-tag" style="color: ${tag.color_hex}; border: 1px solid ${tag.color_hex}">[${tag.name}]</span>
                            <span class="message-author">
                                ${msg.display_name || msg.username}
                                ${isAdmin ? '<span class="admin-badge">Admin</span>' : ''}
                            </span>
                            <span class="message-time">${new Date(msg.created_at).toLocaleTimeString()}</span>
                        </div>
                        <div class="message-text">${msg.message}</div>
                        ${msg.is_edited ? '<small class="edited-mark">(düzenlendi)</small>' : ''}
                        ${msg.read_by ? `<div class="read-by">Okundu: ${msg.read_by.join(', ')}</div>` : ''}
                    </div>
                </div>
            </div>
        `;
    }).join('');

    scrollToBottom();
}

// Admin komutları için bağlam menüsü ekle
function handleContextMenu(event, messageId, username) {
    event.preventDefault();
    
    if (!currentUser.is_admin) return;
    
    const contextMenu = document.createElement('div');
    contextMenu.className = 'context-menu';
    contextMenu.innerHTML = `
        <div class="context-menu-item" onclick="handleAdminCommand('/edit ${messageId} ')">
            <i>✏️</i> Mesajı Düzenle
        </div>
        <div class="context-menu-item" onclick="handleAdminCommand('/delete ${messageId}')">
            <i>🗑️</i> Mesajı Sil
        </div>
        <div class="context-menu-item danger" onclick="handleAdminCommand('/ban ${username}')">
            <i>🚫</i> Kullanıcıyı Banla
        </div>
        <div class="context-menu-item" onclick="handleAdminCommand('/mute ${username} 5')">
            <i>🔇</i> Sustur (5 dk)
        </div>
    `;
    
    // Mevcut bağlam menülerini kaldır
    document.querySelectorAll('.context-menu').forEach(menu => menu.remove());
    
    // Bağlam menüsünü konumlandır
    contextMenu.style.top = `${event.pageY}px`;
    contextMenu.style.left = `${event.pageX}px`;
    document.body.appendChild(contextMenu);
}

// Bağlam menüsünü dışarı tıklayınca kapat
document.addEventListener('click', () => {
    document.querySelectorAll('.context-menu').forEach(menu => menu.remove());
});

// Bağlam menüsüne tıklayınca kapanmasını engelle
document.addEventListener('contextmenu', (e) => {
    if (e.target.closest('.context-menu')) {
        e.preventDefault();
    }
});

// Bağlam menüsünü global olarak kullanılabilir yap
window.handleContextMenu = handleContextMenu;

// Mesajları aşağı kaydırma fonksiyonu
function scrollToBottom() {
    const messagesDiv = document.querySelector('.messages');
    if (messagesDiv && isScrolledToBottom) {
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
}

// Mesajları güncellerken kaydırma konumunu korumak için
let isScrolledToBottom = true;
const messagesDiv = document.querySelector('.messages');

if (messagesDiv) {
    messagesDiv.addEventListener('scroll', () => {
        const threshold = 100; // 100px tolerans
        isScrolledToBottom = messagesDiv.scrollHeight - messagesDiv.scrollTop - messagesDiv.clientHeight < threshold;
    });
}

// Yeni mesajlar geldikten sonra kaydırmayı sağlamak için
window.addEventListener('resize', scrollToBottom);

// Mesaj gönderme
async function sendMessage(text) {
    try {
        const response = await fetch(`${API_URL}/messages`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();

        if (!response.ok) {
            if (response.status === 403) {
                showNotification(data.error, 'error');
                return;
            }
            throw new Error(data.error || 'Mesaj gönderilemedi');
        }

        messageInput.value = '';
        await loadMessages();
        scrollToBottom();

        // Update XP card with new user stats
        if (data.userStats) {
            updateXPCard(data.userStats);
        }
    } catch (err) {
        showNotification(err.message, 'error');
    }
}

// Olay dinleyicileri
sendButton.addEventListener('click', () => {
    const text = messageInput.value.trim();
    if (text) {
        sendMessage(text);
    }
});

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        const text = messageInput.value.trim();
        if (text) {
            sendMessage(text);
            messageInput.value = '';
        }
    }
});

logoutButton.addEventListener('click', () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/index.html';
});

// Mesajları periyodik olarak yenile
setInterval(loadMessages, 5000); // Her 5 saniyede bir

// Çevrimiçi kullanıcı sayısını güncelle
async function updateOnlineCount() {
    try {
        const response = await fetch(`${API_URL}/users/online`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        const data = await response.json();
        document.querySelector('.online-count').textContent = `${data.count} çevrimiçi`;
    } catch (err) {
        console.error('Online count error:', err);
    }
}

// Ayarlar menüsünü göster
function showSettings() {
    const settingsModal = document.createElement('div');
    settingsModal.className = 'settings-modal';
    settingsModal.innerHTML = `
        <div class="settings-content">
            <h2>Ayarlar</h2>
            <div class="setting-item">
                <label>Görüntü Adı</label>
                <input type="text" id="display-name-input" value="${currentUser.display_name}">
            </div>
            <div class="setting-item">
                <label>İsim Rengi</label>
                <input type="color" id="name-color-input" value="${currentUser.display_name_color || '#000000'}">
            </div>
            <div class="setting-item">
                <label>Durum Mesajı</label>
                <input type="text" id="status-input" value="${currentUser.custom_status || ''}">
            </div>
            <div class="setting-item">
                <label>Profil Fotoğrafı</label>
                <input type="file" id="avatar-input" accept="image/*">
            </div>
            <div class="setting-item">
                <label>Tema</label>
                <select id="theme-select">
                    <option value="light">Açık</option>
                    <option value="dark">Koyu</option>
                </select>
            </div>
            <div class="setting-item">
                <label>Bildirimler</label>
                <input type="checkbox" id="notifications-toggle" ${currentUser.notifications_enabled ? 'checked' : ''}>
            </div>
            <button onclick="saveSettings()">Kaydet</button>
            <button onclick="closeSettings()">İptal</button>
        </div>
    `;
    document.body.appendChild(settingsModal);
}

// Ayarları kaydet
async function saveSettings() {
    const settings = {
        display_name: document.getElementById('display-name-input').value,
        display_name_color: document.getElementById('name-color-input').value,
        custom_status: document.getElementById('status-input').value,
        theme: document.getElementById('theme-select').value,
        notifications_enabled: document.getElementById('notifications-toggle').checked
    };

    const avatarInput = document.getElementById('avatar-input');
    if (avatarInput.files.length > 0) {
        const formData = new FormData();
        formData.append('avatar', avatarInput.files[0]);
        await uploadAvatar(formData);
    }

    try {
        const response = await fetch(`${API_URL}/users/settings`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(settings)
        });

        if (response.ok) {
            currentUser = { ...currentUser, ...settings };
            localStorage.setItem('user', JSON.stringify(currentUser));
            closeSettings();
            showSuccess('Ayarlar kaydedildi');
        }
    } catch (err) {
        console.error('Settings save error:', err);
        showError('Ayarlar kaydedilemedi');
    }
}

// Çevrimiçi kullanıcı sayısını güncelleme aralığı
setInterval(updateOnlineCount, 30000);

// Yazıyor... göstergesi
messageInput.addEventListener('input', () => {
    if (typingIndicator) {
        clearTimeout(typingTimeout);
        typingTimeout = setTimeout(() => {
            typingIndicator.style.display = 'none';
        }, 1000);
        typingIndicator.style.display = 'block';
    }
});

// Mesaj alıntılama
function quoteMessage(messageId) {
    try {
        const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
        if (messageElement) {
            const messageText = messageElement.querySelector('.message-text').textContent;
            const authorName = messageElement.querySelector('.message-author').textContent.trim();
            messageInput.value = `> ${authorName}: ${messageText}\n\n`;
            messageInput.focus();
            messageInput.setSelectionRange(messageInput.value.length, messageInput.value.length);
        }
    } catch (err) {
        console.error('Alıntılama hatası:', err);
    }
}

// Mesaj iletme
function forwardMessage(messageId) {
    const message = messageCache.find(msg => msg.id === messageId);
    if (message) {
        // İletme işlemi burada yapılacak
        console.log(`Mesaj iletildi: ${message.message}`);
    }
}

// Tepki ekleme işlevini güncelle
async function reactToMessage(messageId, reaction) {
    try {
        const button = event.target.closest('.message-action-btn');
        if (!button) return;

        // Tıklama animasyonu
        button.style.transform = 'scale(0.9)';
        setTimeout(() => button.style.transform = '', 100);

        const response = await fetch(`${API_URL}/messages/${messageId}/react`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ reaction })
        });

        if (!response.ok) {
            throw new Error('Tepki eklenemedi');
        }

        // Tepkiyi görsel olarak güncelle
        button.classList.toggle('active');
        
        // Sayacı güncelle
        const countSpan = button.querySelector('.count');
        if (countSpan) {
            const currentCount = parseInt(countSpan.textContent) || 0;
            countSpan.textContent = button.classList.contains('active') ? 
                currentCount + 1 : Math.max(0, currentCount - 1);
        }

    } catch (err) {
        console.error('Tepki ekleme hatası:', err);
        showNotification('Tepki eklenirken bir hata oluştu', 'error');
    }
}

// Mesaj arama
function searchMessages(query) {
    const filteredMessages = messageCache.filter(msg => msg.message.includes(query));
    displayMessages(filteredMessages);
}

// Sohbet geçmişinde arama
if (searchInput) {
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        searchMessages(query);
    });
}

// Sayfa yüklendiğinde başlat
document.addEventListener('DOMContentLoaded', initializeChat);

// Emoji seçici işlevselliği
document.addEventListener('DOMContentLoaded', () => {
    const emojiButton = document.getElementById('emoji-button');
    const emojiPicker = document.getElementById('emoji-picker');
    const messageInput = document.getElementById('message-text');
    const emojiList = document.querySelector('.emoji-list');

    // Emoji seçiciyi aç/kapat
    emojiButton.addEventListener('click', () => {
        emojiPicker.classList.toggle('active');
    });

    // Emoji seçiciyi dışarı tıklayınca kapat
    document.addEventListener('click', (e) => {
        if (!emojiPicker.contains(e.target) && !emojiButton.contains(e.target)) {
            emojiPicker.classList.remove('active');
        }
    });

    // Varsayılan kategoriyi yükle
    loadEmojis('smileys');

    // Kategori değiştirme
    document.querySelectorAll('.emoji-categories button').forEach(button => {
        button.addEventListener('click', () => {
            loadEmojis(button.dataset.category);
        });
    });

    // Emoji seçimini işleme
    emojiList.addEventListener('click', (e) => {
        if (e.target.tagName === 'BUTTON') {
            insertEmoji(e.target.textContent);
        }
    });

    // Bir kategori için emojileri yükle
    function loadEmojis(category) {
        emojiList.innerHTML = emojiCategories[category]
            .map(emoji => `<button>${emoji}</button>`)
            .join('');
    }

    // Emojiyi imleç konumuna ekle
    function insertEmoji(emoji) {
        const start = messageInput.selectionStart;
        const end = messageInput.selectionEnd;
        const text = messageInput.value;
        const before = text.substring(0, start);
        const after = text.substring(end);
        messageInput.value = before + emoji + after;
        messageInput.focus();
        messageInput.selectionStart = messageInput.selectionEnd = start + emoji.length;
    }

    // Kısayolları emojilere dönüştür
    messageInput.addEventListener('input', () => {
        let text = messageInput.value;
        for (const [shortcut, emoji] of Object.entries(emojiShortcuts)) {
            text = text.replace(shortcut, emoji);
        }
        if (text !== messageInput.value) {
            messageInput.value = text;
        }
    });
});

// Mesaj okundu bilgisi güncelleme
async function updateReadStatus(messageId) {
    try {
        const response = await fetch(`${API_URL}/messages/${messageId}/read`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (!response.ok) throw new Error('Okundu bilgisi güncellenemedi');
    } catch (err) {
        console.error('Okundu bilgisi güncelleme hatası:', err);
    }
}

// Update XP card
function updateXPCard(userData) {
    if (userData.level === null || userData.level === undefined) {
        userData.level = 1; // Varsayılan olarak 1. seviyeyi ayarla
    }
    const xpProgress = (userData.experience / userData.next_level_xp) * 100;
    const currentTag = determineTag(userData.level);
    
    document.querySelector('.current-tag').textContent = currentTag.name;
    document.querySelector('.current-tag').style.color = currentTag.color_hex;
    document.querySelector('.current-level').textContent = `Level ${userData.level}`;
    document.querySelector('.xp-progress').style.width = `${xpProgress}%`;
    document.querySelector('.current-xp').textContent = userData.experience;
    document.querySelector('.next-level-xp').textContent = `/ ${userData.next_level_xp} XP`;
}



// Modify existing displayMessages function to use the new tag display
// In the message template, replace the username display with:
// ${displayMessageWithTag(msg)}

// Update user data periodically
async function updateUserData() {
    try {
        const response = await fetch(`${API_URL}/users/me`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const userData = await response.json();
        updateXPCard(userData);
    } catch (err) {
        console.error('Failed to update user data:', err);
    }
}

// XP ve Level sistemi
async function updateUserStats() {
    try {
        const response = await fetch(`${API_URL}/users/stats`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        if (!response.ok) throw new Error('Kullanıcı bilgileri alınamadı');
        
        const stats = await response.json();
        updateXPCard(stats);
    } catch (err) {
        console.error('Stats update error:', err);
    }
}

function updateXPCard(stats) {
    const xpCard = document.querySelector('.xp-card');
    if (!xpCard) return;

    const tag = determineTag(stats.level);
    const progress = (stats.experience / stats.next_level_xp) * 100;

    xpCard.innerHTML = `
        <div class="level-info">
            <span class="current-level">Level ${stats.level}</span>
            <span class="tag-display" style="color: ${tag.color_hex}">
                ${tag.name}
            </span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: ${progress}%"></div>
        </div>
        <div class="xp-info">
            <span>${stats.experience} XP</span>
            <span>${stats.next_level_xp - stats.experience} XP to next level</span>
        </div>
    `;

    // Level up efekti
    if (stats.levelUp) {
        xpCard.classList.add('level-up');
        setTimeout(() => xpCard.classList.remove('level-up'), 2000);
    }
}

// Fetch guilds from the database
async function fetchGuilds() {
    try {
        const response = await fetch(`${API_URL}/guilds`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        if (!response.ok) throw new Error('Guilds could not be loaded');
        const guilds = await response.json();
        displayGuilds(guilds);
    } catch (err) {
        console.error('Guild loading error:', err);
    }
}

// Display guilds
function displayGuilds(guilds) {
    const guildList = document.getElementById('guild-list');
    guildList.innerHTML = guilds.map(guild => `
        <div class="guild" onclick="selectGuild(${guild.id})">
            ${guild.name}
        </div>
    `).join('');
}

// Select a guild
function selectGuild(guildId) {
    if (!guildId || isNaN(guildId)) {
        showNotification('Invalid guild selected', 'error');
        return;
    }
    
    currentGuild = guildId;
    document.getElementById('guild-chat').style.display = 'block';
    document.getElementById('chat-tab').style.display = 'none';
    fetchGuildDetails(guildId);
    loadGuildMessages(guildId);
}

// Load guild messages
async function loadGuildMessages(guildId) {
    try {
        const response = await fetch(`${API_URL}/guilds/${guildId}/messages`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        if (!response.ok) throw new Error('Guild messages could not be loaded');
        const messages = await response.json();
        displayGuildMessages(messages);
    } catch (err) {
        console.error('Guild message loading error:', err);
    }
}

// Display guild messages
function displayGuildMessages(messages) {
    const messagesContainer = document.querySelector('#guild-messages .messages-container');
    messagesContainer.innerHTML = messages.map(msg => `
        <div class="message">
            <div class="message-content">
                <div class="message-header">
                    <span class="message-author">${msg.username}</span>
                    <span class="message-time">${new Date(msg.created_at).toLocaleTimeString()}</span>
                </div>
                <div class="message-text">${msg.message}</div>
            </div>
        </div>
    `).join('');
    scrollToBottom();
}

// Send guild message
function sendGuildMessage(guildId, message) {
    // Validate guildId
    if (!guildId || isNaN(parseInt(guildId))) {
        showNotification('Invalid guild ID', 'error');
        return;
    }

    fetch(`${API_URL}/guilds/${guildId}/messages`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`
        },
        body: JSON.stringify({ message })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Message could not be sent');
            });
        }
        return response.json();
    })
    .then(data => {
        appendGuildMessage(data);
        // Clear input after successful send
        const input = document.getElementById('guild-message-text');
        if (input) input.value = '';
    })
    .catch(error => {
        console.error('Guild message send error:', error);
        showNotification(error.message || 'Could not send message', 'error');
    });
}

// Event listeners for guild chat
document.getElementById('send-guild-message').addEventListener('click', () => {
    const input = document.getElementById('guild-message-text');
    const message = input?.value.trim();
    const guildId = currentGuild;
    
    if (!message) {
        showNotification('Please enter a message', 'error');
        return;
    }
    
    if (!guildId) {
        showNotification('No guild selected', 'error');
        return;
    }

    sendGuildMessage(guildId, message);
    input.value = ''; // Clear input after sending
});

document.getElementById('guild-message-text').addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        const input = document.getElementById('guild-message-text');
        const message = input?.value.trim();
        const guildId = currentGuild;
        
        if (!message) {
            showNotification('Please enter a message', 'error');
            return;
        }
        
        if (!guildId) {
            showNotification('No guild selected', 'error');
            return;
        }

        sendGuildMessage(guildId, message);
        input.value = ''; // Clear input after sending
    }
});

// Initialize guilds on page load
document.addEventListener('DOMContentLoaded', () => {
    fetchGuilds();
    // ...existing code...
});

// Show create guild form
function showCreateGuildForm() {
    document.getElementById('create-guild-modal').style.display = 'block';
}

// Close create guild form
function closeCreateGuildForm() {
    document.getElementById('create-guild-modal').style.display = 'none';
}

// Create guild
async function createGuild(event) {
    event.preventDefault();
    const guildName = document.getElementById('guild-name').value.trim();
    const guildDescription = document.getElementById('guild-description').value.trim();

    if (!guildName || !guildDescription) {
        alert('Please fill in all fields');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/guilds`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ name: guildName, description: guildDescription })
        });

        if (!response.ok) throw new Error('Guild could not be created');
        closeCreateGuildForm();
        fetchGuilds(); // Refresh guild list
    } catch (err) {
        console.error('Guild creation error:', err);
    }
}

// Event listener for guild creation form
document.getElementById('create-guild-form').addEventListener('submit', createGuild);

// Leave guild functionality
function leaveGuild() {
    const guildId = currentGuild;
    
    if (confirm('Are you sure you want to leave this guild?')) {
        fetch(`${API_URL}/guilds/${guildId}/leave`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Could not leave guild');
            return response.json();
        })
        .then(() => {
            showNotification('Successfully left the guild', 'success');
            hideGuildChat();
            fetchGuilds(); // Refresh guild list
        })
        .catch(error => {
            console.error('Guild leave error:', error);
            showNotification('Could not leave guild', 'error');
        });
    }
}

function hideGuildChat() {
    const generalChat = document.querySelector('.chat-area');
    generalChat.classList.remove('guild-chat-active');
    document.getElementById('guild-chat').style.display = 'none';
}

// Add to your existing guild list loading function
function createGuildElement(guild) {
    const div = document.createElement('div');
    div.className = 'guild-item';
    div.innerHTML = `
        <h4>${escapeHtml(guild.name)}</h4>
        <p>${escapeHtml(guild.description)}</p>
        <span class="guild-member-count">${guild.memberCount} members</span>
    `;
    div.onclick = () => handleGuildClick(guild.id);
    return div;
}

// ...existing code...

// Add this helper function near the top of the file
function getToken() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/index.html';
        throw new Error('No authentication token found');
    }
    return token;
}

// Update selectGuild function to use correct API path
function selectGuild(guildId) {
    currentGuild = guildId;
    document.getElementById('guild-chat').style.display = 'flex';
    document.getElementById('messages').style.display = 'none';
    fetchGuildDetails(guildId);
    loadGuildMessages(guildId);
}

// Update loadGuildMessages function
function loadGuildMessages(guildId) {
    fetch(`${API_URL}/guilds/${guildId}/messages`, {
        headers: {
            'Authorization': `Bearer ${getToken()}`
        }
    })
    .then(response => {
        if (!response.ok) throw new Error('Guild messages could not be loaded');
        return response.json();
    })
    .then(messages => {
        const container = document.querySelector('#guild-messages .messages-container');
        container.innerHTML = ''; // Clear existing messages
        messages.forEach(message => {
            appendGuildMessage(message);
        });
        scrollToBottom(container);
    })
    .catch(error => {
        console.error('Guild message loading error:', error);
        showNotification('Could not load guild messages', 'error');
    });
}

// Update fetchGuildDetails function
function fetchGuildDetails(guildId) {
    fetch(`${API_URL}/guilds/${guildId}`, {
        headers: {
            'Authorization': `Bearer ${getToken()}`
        }
    })
    .then(response => {
        if (!response.ok) throw new Error('Guild details could not be loaded');
        return response.json();
    })
    .then(guild => {
        document.getElementById('guild-chat-title').textContent = guild.name;
        document.querySelector('.member-count').textContent = `${guild.memberCount} members`;
        document.querySelector('.guild-creator').textContent = `Created by: ${guild.creator_username}`;
        document.querySelector('.guild-created-at').textContent = `Created at: ${new Date(guild.created_at).toLocaleString()}`;
    })
    .catch(error => {
        console.error('Guild details fetch error:', error);
        showNotification('Could not load guild details', 'error');
    });
}

// Ensure createMessageElement function is defined
function createMessageElement(message) {
    // Create a message element based on the message object
    const messageElement = document.createElement('div');
    messageElement.className = 'message';
    messageElement.innerHTML = `
        <div class="message-content">
            <div class="message-header">
                <span class="message-author">${message.username}</span>
                <span class="message-time">${new Date(message.created_at).toLocaleTimeString()}</span>
            </div>
            <div class="message-text">${message.message}</div>
        </div>
    `;
    return messageElement;
}

// Ensure appendGuildMessage function is defined
function appendGuildMessage(message) {
    const container = document.querySelector('#guild-messages .messages-container');
    const messageElement = createMessageElement(message); // Reuse existing message creation
    container.appendChild(messageElement);
    scrollToBottom(container);
}

// Update sendGuildMessage function to use correct path
function sendGuildMessage(guildId, message) {
    fetch(`${API_URL}/guilds/${guildId}/messages`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`
        },
        body: JSON.stringify({ message })
    })
    .then(response => {
        if (!response.ok) throw new Error('Message could not be sent');
        return response.json();
    })
    .then(data => {
        appendGuildMessage(data);
    })
    .catch(error => {
        console.error('Guild message send error:', error);
        showNotification('Could not send message', 'error');
    });
}

// Add error handling for invalid guild IDs
function selectGuild(guildId) {
    if (!guildId || isNaN(guildId)) {
        showNotification('Invalid guild selected', 'error');
        return;
    }
    
    currentGuild = guildId;
    document.getElementById('guild-chat').style.display = 'flex';
    document.getElementById('messages').style.display = 'none';
    fetchGuildDetails(guildId);
    loadGuildMessages(guildId);
}

// Invite user to guild
function inviteUserToGuild() {
    const username = prompt('Enter the username of the user to invite:');
    if (!username) return;

    fetch(`${API_URL}/guilds/${currentGuild}/invite`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`
        },
        body: JSON.stringify({ username })
    })
    .then(response => {
        if (!response.ok) throw new Error('Could not invite user to guild');
        return response.json();
    })
    .then(() => {
        showNotification('User invited to guild successfully', 'success');
    })
    .catch(error => {
        console.error('Guild invite error:', error);
        showNotification('Could not invite user to guild', 'error');
    });
}

// Update guild header to include additional details
document.addEventListener('DOMContentLoaded', () => {
    fetchGuilds();
    // ...existing code...
});

// Fetch guild details
function fetchGuildDetails(guildId) {
    fetch(`${API_URL}/guilds/${guildId}`, {
        headers: {
            'Authorization': `Bearer ${getToken()}`
        }
    })
    .then(response => {
        if (!response.ok) throw new Error('Guild details could not be loaded');
        return response.json();
    })
    .then(guild => {
        document.getElementById('guild-chat-title').textContent = guild.name;
        document.querySelector('.member-count').textContent = `${guild.memberCount} members`;
        document.querySelector('.guild-creator').textContent = `Created by: ${guild.creator_username}`;
        document.querySelector('.guild-created-at').textContent = `Created at: ${new Date(guild.created_at).toLocaleString()}`;
    })
    .catch(error => {
        console.error('Guild details fetch error:', error);
        showNotification('Could not load guild details', 'error');
    });
}




