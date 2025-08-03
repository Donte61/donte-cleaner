document.addEventListener('DOMContentLoaded', () => {
    const settingsForm = document.getElementById('settings-form');
    const themeSelect = document.getElementById('theme');
    const fontSizeInput = document.getElementById('font-size');
    const displayNameInput = document.getElementById('display-name');
    const customStatusInput = document.getElementById('custom-status');
    const notificationsInput = document.getElementById('notifications');

    // Load settings from localStorage
    const settings = JSON.parse(localStorage.getItem('settings')) || {};
    themeSelect.value = settings.theme || 'light';
    fontSizeInput.value = settings.fontSize || 16;
    displayNameInput.value = settings.displayName || '';
    customStatusInput.value = settings.customStatus || '';
    notificationsInput.checked = settings.notifications || false;

    // Apply settings
    applySettings(settings);

    settingsForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const newSettings = {
            theme: themeSelect.value,
            fontSize: fontSizeInput.value,
            displayName: displayNameInput.value,
            customStatus: customStatusInput.value,
            notifications: notificationsInput.checked
        };

        // Save settings to localStorage
        localStorage.setItem('settings', JSON.stringify(newSettings));

        // Apply settings
        applySettings(newSettings);

        // Save settings to server
        try {
            const response = await fetch(`${API_URL}/users/settings`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify(newSettings)
            });

            if (!response.ok) {
                throw new Error('Ayarlar kaydedilemedi');
            }

            alert('Ayarlar kaydedildi');
        } catch (err) {
            console.error('Ayarlar kaydedilemedi:', err);
            alert('Ayarlar kaydedilemedi');
        }
    });

    function applySettings(settings) {
        document.body.style.fontSize = `${settings.fontSize}px`;
        document.body.className = settings.theme;
    }
});
