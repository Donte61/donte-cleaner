const express = require('express');
const sql = require('mssql');
const cors = require('cors');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const config = require('./config');

const app = express();
app.use(cors());
app.use(express.json());

const JWT_SECRET = 'your-secret-key';  // Güvenli bir secret key kullanın

// Auth Middleware
const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) return res.status(401).json({ error: 'Token gerekli' });

    jwt.verify(token, JWT_SECRET, (err, user) => {
        if (err) return res.status(403).json({ error: 'Geçersiz token' });
        req.user = user;
        next();
    });
};

// Basit test endpoint'i
app.get('/', (req, res) => {
    res.json({ message: 'Server is running!' });
});

// Bağlantı testi endpoint'i
app.get('/test', async (req, res) => {
    try {
        console.log('Bağlantı yapılandırması ile veritabanı bağlantısı deneniyor:', {
            ...config,
            password: '[GİZLİ]'
        });

        const pool = await sql.connect(config);
        console.log('Bağlantı kuruldu');

        const result = await pool.request()
            .query('SELECT @@VERSION AS VERSION, @@SERVERNAME AS SERVERNAME');
        
        await pool.close();
        
        res.json({
            status: 'success',
            sql_version: result.recordset[0].VERSION,
            server_name: result.recordset[0].SERVERNAME,
            connection: {
                server: config.server,
                database: config.database,
                user: config.user,
                instance: config.options.instanceName
            }
        });
    } catch (err) {
        console.error('Detaylı bağlantı hatası:', err);
        res.status(500).json({
            status: 'error',
            message: err.message,
            code: err.code,
            connection_info: {
                server: config.server,
                database: config.database,
                user: config.user,
                instance: config.options.instanceName
            }
        });
    }
});

// Auth endpoints
app.post('/api/auth/register', async (req, res) => {
    try {
        const { username, password, email, display_name } = req.body;
        
        // Check if user already exists
        const pool = await sql.connect(config);
        const checkUser = await pool.request()
            .input('username', sql.NVarChar, username)
            .input('email', sql.NVarChar, email)
            .query('SELECT * FROM Users WHERE username = @username OR email = @email');
        
        if (checkUser.recordset.length > 0) {
            return res.status(400).json({ 
                error: 'Bu kullanıcı adı veya email zaten kullanımda'
            });
        }

        const hashedPassword = await bcrypt.hash(password, 10);
        
        const result = await pool.request()
            .input('username', sql.NVarChar, username)
            .input('password', sql.NVarChar, hashedPassword)
            .input('email', sql.NVarChar, email)
            .input('display_name', sql.NVarChar, display_name || username)
            .query(`
                INSERT INTO Users (username, password, email, display_name)
                VALUES (@username, @password, @email, @display_name);
                SELECT SCOPE_IDENTITY() as id;
            `);

        const user = {
            id: result.recordset[0].id,
            username,
            display_name: display_name || username,
            is_admin: false  // Add default is_admin value
        };
        
        const token = jwt.sign(user, JWT_SECRET);
        res.status(201).json({ token, user });
    } catch (err) {
        console.error('Kayıt hatası:', err);
        res.status(500).json({ error: 'Kayıt işlemi başarısız' });
    }
});

app.post('/api/auth/login', async (req, res) => {
    try {
        const { username, password } = req.body;
        
        const pool = await sql.connect(config);
        const result = await pool.request()
            .input('username', sql.NVarChar, username)
            .query('SELECT * FROM Users WHERE username = @username');

        const user = result.recordset[0];
        if (!user || !(await bcrypt.compare(password, user.password))) {
            return res.status(401).json({ error: 'Geçersiz kullanıcı adı veya şifre' });
        }

        const tokenUser = {
            id: user.id,
            username: user.username,
            display_name: user.display_name,
            is_admin: user.is_admin  // Add is_admin to token
        };

        const token = jwt.sign(tokenUser, JWT_SECRET);

        // Update last_seen and is_online
        await pool.request()
            .input('id', sql.Int, user.id)
            .query(`
                UPDATE Users 
                SET last_seen = GETDATE(), is_online = 1 
                WHERE id = @id
            `);

        res.json({ 
            token, 
            user: {
                id: user.id,
                username: user.username,
                display_name: user.display_name,
                email: user.email,
                avatar_url: 'frontend/avatar/default-avatar.png', // Use default avatar
                is_admin: user.is_admin  // Add is_admin to response
            }
        });
    } catch (err) {
        console.error('Giriş hatası:', err);
        res.status(500).json({ error: 'Giriş işlemi başarısız' });
    }
});

// Protected Message endpoints
app.get('/api/messages', authenticateToken, async (req, res) => {
    try {
        const pool = await sql.connect(config);
        const result = await pool.request()
            .query(`
                SELECT TOP 100
                    m.*,
                    u.username,
                    u.display_name,
                    u.avatar_url,
                    u.is_admin,
                    CAST(u.level as INT) as user_level,  -- Cast to ensure integer
                    u.experience,
                    u.next_level_xp
                FROM Messages m
                JOIN Users u ON m.user_id = u.id
                WHERE m.is_deleted = 0
                ORDER BY m.created_at ASC;
            `);
        
        console.log('Sample message data:', result.recordset[0]); // Debug log
        
        res.json(result.recordset);
    } catch (err) {
        console.error('Mesajları getirme hatası:', err);
        res.status(500).json({ error: 'Mesajlar alınırken bir hata oluştu' });
    }
});

app.post('/api/messages', authenticateToken, async (req, res) => {
    try {
        const user_id = req.user.id;
        const pool = await sql.connect(config);
        
        // Ban ve mute kontrolü
        const userStatus = await pool.request()
            .input('user_id', sql.Int, user_id)
            .query(`
                -- Ban kontrolü
                SELECT TOP 1 * FROM UserBans 
                WHERE user_id = @user_id AND is_active = 1
                ORDER BY ban_date DESC;

                -- Mute kontrolü
                SELECT TOP 1 * FROM UserMutes
                WHERE user_id = @user_id 
                AND is_active = 1 
                AND GETDATE() < unmute_time
                ORDER BY mute_time DESC;
            `);

        if (userStatus.recordsets[0].length > 0) {
            return res.status(403).json({ 
                error: 'Hesabınız engellendiği için mesaj gönderemezsiniz.',
                banInfo: userStatus.recordsets[0][0]
            });
        }

        if (userStatus.recordsets[1].length > 0) {
            const muteInfo = userStatus.recordsets[1][0];
            const remainingTime = new Date(muteInfo.unmute_time) - new Date();
            const remainingMinutes = Math.ceil(remainingTime / 60000);
            
            return res.status(403).json({ 
                error: `Hesabınız ${remainingMinutes} dakika boyunca susturuldu.`,
                muteInfo: muteInfo
            });
        }

        const { message, message_type = 'text' } = req.body;
        if (!message) {
            return res.status(400).json({ error: 'Mesaj gerekli' });
        }

        // First insert the message
        const insertResult = await pool.request()
            .input('user_id', sql.Int, user_id)
            .input('message', sql.NVarChar, message)
            .input('message_type', sql.NVarChar, message_type)
            .query(`
                INSERT INTO Messages (user_id, message, message_type)
                VALUES (@user_id, @message, @message_type);
                SELECT SCOPE_IDENTITY() as id;
            `);
        
        const messageId = insertResult.recordset[0].id;
        
        // Then get the complete message data
        const result = await pool.request()
            .input('messageId', sql.Int, messageId)
            .query(`
                SELECT 
                    m.*,
                    u.username,
                    u.display_name,
                    u.avatar_url
                FROM Messages m
                JOIN Users u ON m.user_id = u.id
                WHERE m.id = @messageId
            `);

        // Update user experience
        const messageLength = message.length;
        await pool.request()
            .input('userId', sql.Int, user_id)
            .input('messageLength', sql.Int, messageLength)
            .execute('UpdateUserExperience');

        // Fetch updated user stats
        const userStats = await pool.request()
            .input('userId', sql.Int, user_id)
            .query(`
                SELECT level, experience, next_level_xp
                FROM Users
                WHERE id = @userId
            `);

        res.status(201).json({
            message: result.recordset[0],
            userStats: userStats.recordset[0]
        });
    } catch (err) {
        console.error('Mesaj gönderme hatası:', err);
        res.status(500).json({ error: 'Mesaj gönderilirken bir hata oluştu' });
    }
});

app.delete('/api/messages/:id', authenticateToken, async (req, res) => {
    try {
        const messageId = req.params.id;
        const userId = req.user.id;

        const pool = await sql.connect(config);
        const result = await pool.request()
            .input('id', sql.Int, messageId)
            .input('user_id', sql.Int, userId)
            .query(`
                UPDATE Messages 
                SET is_deleted = 1 
                WHERE id = @id AND user_id = @user_id
            `);

        if (result.rowsAffected[0] === 0) {
            return res.status(404).json({ error: 'Mesaj bulunamadı veya silme yetkisi yok' });
        }

        res.json({ message: 'Mesaj başarıyla silindi' });
    } catch (err) {
        console.error('Mesaj silme hatası:', err);
        res.status(500).json({ error: 'Mesaj silinirken bir hata oluştu' });
    }
});

// Get online users count
app.get('/api/users/online', authenticateToken, async (req, res) => {
    try {
        const pool = await sql.connect(config);
        const result = await pool.request()
            .query('SELECT COUNT(*) as count FROM Users WHERE is_online = 1');
        res.json({ count: result.recordset[0].count });
    } catch (err) {
        res.status(500).json({ error: 'Çevrimiçi kullanıcı sayısı alınamadı' });
    }
});

// Update message delete endpoint
app.delete('/api/admin/messages/:id', authenticateToken, async (req, res) => {
    try {
        const user = req.user;
        if (!user.is_admin) {
            return res.status(403).json({ error: 'Yetkiniz yok' });
        }

        const pool = await sql.connect(config);
        await pool.request()
            .input('id', sql.Int, req.params.id)
            .input('admin_id', sql.Int, user.id)
            .query(`
                UPDATE Messages 
                SET message = 'Deleted by admin!',
                    is_edited = 1,
                    edited_at = GETDATE()
                WHERE id = @id;

                -- Add system message
                INSERT INTO Messages (user_id, message, message_type)
                VALUES (@admin_id, '!System: Bir mesaj admin tarafından silindi!', 'system');
            `);
        
        res.json({ message: 'Mesaj silindi' });
    } catch (err) {
        res.status(500).json({ error: 'Mesaj silinemedi' });
    }
});

// Update user settings
app.post('/api/users/settings', authenticateToken, async (req, res) => {
    try {
        const { theme, fontSize, displayName, customStatus, notifications } = req.body;
        const pool = await sql.connect(config);
        
        await pool.request()
            .input('id', sql.Int, req.user.id)
            .input('display_name', sql.NVarChar, displayName)
            .input('custom_status', sql.NVarChar, customStatus)
            .input('theme', sql.VarChar, theme)
            .input('font_size', sql.Int, fontSize)
            .input('notifications', sql.Bit, notifications)
            .query(`
                UPDATE Users 
                SET display_name = @display_name,
                    custom_status = @custom_status
                WHERE id = @id;

                IF EXISTS (SELECT 1 FROM UserSettings WHERE user_id = @id)
                BEGIN
                    UPDATE UserSettings
                    SET theme = @theme,
                        font_size = @font_size,
                        notifications_enabled = @notifications
                    WHERE user_id = @id;
                END
                ELSE
                BEGIN
                    INSERT INTO UserSettings (user_id, theme, font_size, notifications_enabled)
                    VALUES (@id, @theme, @font_size, @notifications);
                END
            `);

        res.json({ message: 'Ayarlar güncellendi' });
    } catch (err) {
        console.error('Ayarlar güncellenemedi:', err);
        res.status(500).json({ error: 'Ayarlar güncellenemedi' });
    }
});

// Update the admin commands
app.post('/api/admin/command', authenticateToken, async (req, res) => {
    try {
        const { command, params } = req.body;
        const user = req.user;

        if (!user.is_admin) {
            return res.status(403).json({ error: 'Admin yetkisi gerekli' });
        }

        const pool = await sql.connect(config);

        switch (command) {
            case '/ban':
                const banResult = await pool.request()
                    .input('username', sql.NVarChar, params.username)
                    .input('reason', sql.NVarChar, params.reason)
                    .input('admin_id', sql.Int, user.id)
                    .query(`
                        DECLARE @userId INT;
                        SELECT @userId = id FROM Users WHERE username = @username;

                        IF @userId IS NULL
                            THROW 50000, 'Kullanıcı bulunamadı', 1;

                        INSERT INTO UserBans (user_id, banned_by, reason)
                        VALUES (@userId, @admin_id, @reason);
                        
                        UPDATE Users SET is_online = 0 WHERE id = @userId;

                        -- Update all messages from banned user
                        UPDATE Messages 
                        SET message = 'User Banned!'
                        WHERE user_id = @userId;

                        -- Add system message about ban
                        INSERT INTO Messages (user_id, message, message_type)
                        VALUES (@admin_id, '!System: ' + @username + ' banlandı! Sebep: ' + @reason, 'system');
                    `);
                return res.json({ message: `${params.username} banlandı` });

            case '/unban':
                console.log('Unban command received:', params); // Debug log

                await pool.request()
                    .input('username', sql.NVarChar, params.username)
                    .input('admin_id', sql.Int, user.id)
                    .query(`
                        DECLARE @userId INT;
                        SELECT @userId = id FROM Users WHERE username = @username;

                        IF @userId IS NULL
                            THROW 50000, 'Kullanıcı bulunamadı', 1;

                        IF NOT EXISTS (SELECT 1 FROM UserBans WHERE user_id = @userId AND is_active = 1)
                            THROW 50001, 'Kullanıcı zaten banlı değil', 1;

                        UPDATE UserBans 
                        SET is_active = 0, 
                            unban_date = GETDATE()
                        WHERE user_id = @userId 
                        AND is_active = 1;

                        -- Add system message about unban
                        INSERT INTO Messages (user_id, message, message_type)
                        VALUES (@admin_id, '!System: ' + @username + ' kullanıcısının banı kaldırıldı!', 'system');
                    `);

                return res.json({ 
                    message: `${params.username} kullanıcısının banı kaldırıldı`
                });

            case '/clear':
                await pool.request()
                    .query('UPDATE Messages SET is_deleted = 1');
                return res.json({ message: 'Tüm mesajlar silindi' });

            case '/mute':
                const muteResult = await pool.request()
                    .input('username', sql.NVarChar, params.username)
                    .input('duration', sql.Int, parseInt(params.duration) || 5)
                    .input('admin_id', sql.Int, user.id)
                    .query(`
                        DECLARE @userId INT;
                        SELECT @userId = id FROM Users WHERE username = @username;

                        INSERT INTO UserMutes (user_id, muted_by, duration_minutes, unmute_time)
                        VALUES (@userId, @admin_id, @duration, DATEADD(minute, @duration, GETDATE()));

                        -- Add system message about mute
                        INSERT INTO Messages (user_id, message, message_type)
                        VALUES (@admin_id, '!System: ' + @username + ' ' + CAST(@duration as varchar) + ' dakika susturuldu!', 'system');
                    `);
                return res.json({ message: `${params.username} susturuldu` });

            case '/unmute':
                const unmuteResult = await pool.request()
                    .input('username', sql.NVarChar, params.username)
                    .input('admin_id', sql.Int, user.id)
                    .query(`
                        DECLARE @userId INT;
                        SELECT @userId = id FROM Users WHERE username = @username;

                        IF @userId IS NULL
                            THROW 50000, 'Kullanıcı bulunamadı', 1;

                        UPDATE UserMutes 
                        SET is_active = 0,
                            unmute_time = GETDATE()
                        WHERE user_id = @userId 
                        AND is_active = 1;

                        -- Add system message about unmute
                        INSERT INTO Messages (user_id, message, message_type)
                        VALUES (@admin_id, '!System: ' + @username + ' susturulması kaldırıldı!', 'system');
                    `);
                return res.json({ message: `${params.username} susturulması kaldırıldı` });

            case '/edit':
                await pool.request()
                    .input('message_id', sql.Int, params.messageId)
                    .input('new_text', sql.NVarChar, params.newText)
                    .query(`
                        UPDATE Messages 
                        SET message = @new_text, 
                            is_edited = 1, 
                            edited_at = GETDATE()
                        WHERE id = @message_id
                    `);
                return res.json({ message: 'Mesaj düzenlendi' });

            case '/announce':
                await pool.request()
                    .input('user_id', sql.Int, user.id)
                    .input('message', sql.NVarChar, params.message)
                    .query(`
                        INSERT INTO Messages (user_id, message, message_type)
                        VALUES (@user_id, @message, 'announcement');

                        SELECT SCOPE_IDENTITY() as id;
                    `);
                return res.json({ message: 'Duyuru yapıldı' });

            default:
                return res.status(400).json({ error: 'Geçersiz komut' });
        }
    } catch (err) {
        console.error('Komut hatası:', err);
        res.status(500).json({ 
            error: err.message === 'Kullanıcı bulunamadı' ? 
                'Kullanıcı bulunamadı' : 
                'Komut işlenirken hata oluştu' 
        });
    }
});

// Add new admin endpoints
app.get('/api/admin/bans', authenticateToken, async (req, res) => {
    try {
        if (!req.user.is_admin) {
            return res.status(403).json({ error: 'Admin yetkisi gerekli' });
        }

        const pool = await sql.connect(config);
        const result = await pool.request()
            .query(`
                SELECT 
                    b.*,
                    u.username,
                    u.display_name,
                    admin.username as banned_by_username
                FROM UserBans b
                JOIN Users u ON b.user_id = u.id
                JOIN Users admin ON b.banned_by = admin.id
                WHERE b.is_active = 1
                ORDER BY b.ban_date DESC
            `);
        res.json(result.recordset);
    } catch (err) {
        res.status(500).json({ error: 'Banlı kullanıcılar alınamadı' });
    }
});

app.get('/api/admin/mutes', authenticateToken, async (req, res) => {
    try {
        if (!req.user.is_admin) {
            return res.status(403).json({ error: 'Admin yetkisi gerekli' });
        }

        const pool = await sql.connect(config);
        const result = await pool.request()
            .query(`
                SELECT 
                    m.*,
                    u.username,
                    u.display_name,
                    admin.username as muted_by_username
                FROM UserMutes m
                JOIN Users u ON m.user_id = u.id
                JOIN Users admin ON m.muted_by = admin.id
                WHERE m.is_active = 1 AND m.unmute_time > GETDATE()
                ORDER BY m.mute_time DESC
            `);
        res.json(result.recordset);
    } catch (err) {
        res.status(500).json({ error: 'Susturulan kullanıcılar alınamadı' });
    }
});

app.get('/api/admin/users', authenticateToken, async (req, res) => {
    try {
        if (!req.user.is_admin) {
            return res.status(403).json({ error: 'Admin yetkisi gerekli' });
        }

        const pool = await sql.connect(config);
        const result = await pool.request()
            .query(`
                SELECT 
                    id, username, display_name, email, 
                    is_online, last_seen, created_at,
                    avatar_url, is_admin
                FROM Users
                ORDER BY created_at DESC
            `);
        res.json(result.recordset);
    } catch (err) {
        res.status(500).json({ error: 'Kullanıcı listesi alınamadı' });
    }
});

// Tepki ekleme/kaldırma endpoint'i
app.post('/api/messages/:id/react', authenticateToken, async (req, res) => {
    try {
        const { reaction } = req.body;
        const messageId = req.params.id;
        const userId = req.user.id;

        const pool = await sql.connect(config);
        
        // Önce mevcut tepkileri kontrol et
        const currentMessage = await pool.request()
            .input('messageId', sql.Int, messageId)
            .query('SELECT reactions FROM Messages WHERE id = @messageId');

        let reactions = [];
        if (currentMessage.recordset[0].reactions) {
            reactions = JSON.parse(currentMessage.recordset[0].reactions).reactions;
        }

        // Kullanıcının bu tepkisi var mı kontrol et
        const existingReaction = reactions.findIndex(r => 
            r.userId === userId && r.reaction === reaction
        );

        if (existingReaction > -1) {
            // Tepki varsa kaldır
            reactions.splice(existingReaction, 1);
        } else {
            // Tepki yoksa ekle
            reactions.push({ userId, reaction });
        }

        // Tepkileri güncelle
        await pool.request()
            .input('messageId', sql.Int, messageId)
            .input('reactions', sql.NVarChar, JSON.stringify({ reactions }))
            .query('UPDATE Messages SET reactions = @reactions WHERE id = @messageId');

        res.json({ success: true, reactions });
    } catch (err) {
        console.error('Tepki işleme hatası:', err);
        res.status(500).json({ error: 'Tepki işlenemedi' });
    }
});

// Mesaj alıntılama endpoint'i
app.post('/api/messages/quote', authenticateToken, async (req, res) => {
    try {
        const { originalMessageId, quotedText, newMessage } = req.body;
        const userId = req.user.id;

        const pool = await sql.connect(config);
        
        // Alıntılanan mesajı kontrol et
        const originalMessage = await pool.request()
            .input('messageId', sql.Int, originalMessageId)
            .query(`
                SELECT m.*, u.username, u.display_name 
                FROM Messages m
                JOIN Users u ON m.user_id = u.id
                WHERE m.id = @messageId
            `);

        if (originalMessage.recordset.length === 0) {
            return res.status(404).json({ error: 'Alıntılanacak mesaj bulunamadı' });
        }

        // Yeni mesajı ekle
        const result = await pool.request()
            .input('userId', sql.Int, userId)
            .input('message', sql.NVarChar, newMessage)
            .input('quotedText', sql.NVarChar, quotedText)
            .input('quotedMessageId', sql.Int, originalMessageId)
            .query(`
                INSERT INTO Messages (user_id, message, quoted_text, quoted_message_id)
                VALUES (@userId, @message, @quotedText, @quotedMessageId);
                
                SELECT SCOPE_IDENTITY() as id;
            `);

        res.json({ success: true, messageId: result.recordset[0].id });
    } catch (err) {
        console.error('Alıntılama hatası:', err);
        res.status(500).json({ error: 'Mesaj alıntılanamadı' });
    }
});

// Fetch tags endpoint
app.get('/api/tags', authenticateToken, async (req, res) => {
    try {
        const pool = await sql.connect(config);
        const result = await pool.request().query('SELECT * FROM Tags ORDER BY required_level ASC');
        res.json(result.recordset);
    } catch (err) {
        console.error('Tagları getirme hatası:', err);
        res.status(500).json({ error: 'Taglar alınırken bir hata oluştu' });
    }
});

// Fetch announcements endpoint
app.get('/api/announcements', authenticateToken, async (req, res) => {
    try {
        const pool = await sql.connect(config);
        const result = await pool.request().query('SELECT * FROM Announcements ORDER BY created_at DESC');
        res.json(result.recordset);
    } catch (err) {
        console.error('Duyuruları getirme hatası:', err);
        res.status(500).json({ error: 'Duyurular alınırken bir hata oluştu' });
    }
});

// Kullanıcı istatistiklerini getirme endpoint'i
app.get('/api/users/stats', authenticateToken, async (req, res) => {
    try {
        const userId = req.user.id;
        const pool = await sql.connect(config);
        const result = await pool.request()
            .input('userId', sql.Int, userId)
            .query(`
                SELECT 
                    level, 
                    experience, 
                    next_level_xp 
                FROM Users 
                WHERE id = @userId
            `);

        if (result.recordset.length === 0) {
            return res.status(404).json({ error: 'Kullanıcı bulunamadı' });
        }

        res.json(result.recordset[0]);
    } catch (err) {
        console.error('Kullanıcı istatistikleri alınamadı:', err);
        res.status(500).json({ error: 'Kullanıcı istatistikleri alınamadı' });
    }
});

// Guild endpoints
app.get('/api/guilds', authenticateToken, async (req, res) => {
    try {
        const pool = await sql.connect(config);
        const result = await pool.request()
            .input('userId', sql.Int, req.user.id)
            .query(`
                SELECT 
                    g.*,
                    (SELECT COUNT(*) FROM GuildMembers WHERE guild_id = g.id) as memberCount
                FROM Guilds g
                JOIN GuildMembers gm ON g.id = gm.guild_id
                WHERE gm.user_id = @userId
                ORDER BY g.created_at DESC
            `);
        res.json(result.recordset);
    } catch (err) {
        console.error('Guilds fetch error:', err);
        res.status(500).json({ error: 'Guilds could not be loaded' });
    }
});

app.post('/api/guilds', authenticateToken, async (req, res) => {
    try {
        const { name, description } = req.body;
        const userId = req.user.id;

        const pool = await sql.connect(config);

        // Check if user is already a member of a guild
        const memberCheck = await pool.request()
            .input('userId', sql.Int, userId)
            .query('SELECT 1 FROM GuildMembers WHERE user_id = @userId');

        if (memberCheck.recordset.length > 0) {
            return res.status(400).json({ error: 'You are already a member of a guild' });
        }

        await pool.request()
            .input('name', sql.NVarChar, name)
            .input('description', sql.NVarChar, description)
            .input('userId', sql.Int, userId)
            .execute('CreateGuild');

        res.status(201).json({ message: 'Guild created successfully' });
    } catch (err) {
        console.error('Guild creation error:', err);
        res.status(500).json({ error: 'Guild could not be created' });
    }
});

app.get('/api/guilds/:id', authenticateToken, async (req, res) => {
    try {
        const guildId = parseInt(req.params.id);
        if (isNaN(guildId)) {
            return res.status(400).json({ error: 'Invalid guild ID' });
        }

        const pool = await sql.connect(config);
        const result = await pool.request()
            .input('guildId', sql.Int, guildId)
            .query(`
                SELECT 
                    g.*,
                    u.username as creator_username,
                    (SELECT COUNT(*) FROM GuildMembers WHERE guild_id = g.id) as memberCount
                FROM Guilds g
                JOIN Users u ON g.creator_id = u.id
                WHERE g.id = @guildId
            `);

        if (result.recordset.length === 0) {
            return res.status(404).json({ error: 'Guild not found' });
        }

        res.json(result.recordset[0]);
    } catch (err) {
        console.error('Guild details fetch error:', err);
        res.status(500).json({ error: 'Guild details could not be loaded' });
    }
});

app.post('/api/guilds/:id/invite', authenticateToken, async (req, res) => {
    try {
        const { username } = req.body;
        const guildId = parseInt(req.params.id);
        if (isNaN(guildId)) {
            return res.status(400).json({ error: 'Invalid guild ID' });
        }

        const pool = await sql.connect(config);

        // Check if the user to be invited exists
        const userCheck = await pool.request()
            .input('username', sql.NVarChar, username)
            .query('SELECT id FROM Users WHERE username = @username');

        if (userCheck.recordset.length === 0) {
            return res.status(404).json({ error: 'User not found' });
        }

        const userId = userCheck.recordset[0].id;

        // Check if the user is already a member of a guild
        const memberCheck = await pool.request()
            .input('userId', sql.Int, userId)
            .query('SELECT 1 FROM GuildMembers WHERE user_id = @userId');

        if (memberCheck.recordset.length > 0) {
            return res.status(400).json({ error: 'User is already a member of a guild' });
        }

        // Add user to guild
        await pool.request()
            .input('guildId', sql.Int, guildId)
            .input('userId', sql.Int, userId)
            .query('INSERT INTO GuildMembers (guild_id, user_id) VALUES (@guildId, @userId)');

        res.json({ message: 'User invited to guild successfully' });
    } catch (err) {
        console.error('Guild invite error:', err);
        res.status(500).json({ error: 'Could not invite user to guild' });
    }
});

// Guild Messages endpoints
app.get('/api/guilds/:id/messages', authenticateToken, async (req, res) => {
    try {
        const guildId = req.params.id;
        const userId = req.user.id;

        const pool = await sql.connect(config);
        
        // First check if user is a member of the guild
        const memberCheck = await pool.request()
            .input('guildId', sql.Int, guildId)
            .input('userId', sql.Int, userId)
            .query(`
                SELECT 1 FROM GuildMembers 
                WHERE guild_id = @guildId AND user_id = @userId
            `);

        if (memberCheck.recordset.length === 0) {
            return res.status(403).json({ error: 'You are not a member of this guild' });
        }

        // Fetch guild messages
        const result = await pool.request()
            .input('guildId', sql.Int, guildId)
            .query(`
                SELECT 
                    gm.*,
                    u.username,
                    u.display_name,
                    u.avatar_url,
                    u.level as user_level
                FROM GuildMessages gm
                JOIN Users u ON gm.user_id = u.id
                WHERE gm.guild_id = @guildId
                ORDER BY gm.created_at ASC
            `);

        res.json(result.recordset);
    } catch (err) {
        console.error('Guild messages fetch error:', err);
        res.status(500).json({ error: 'Guild messages could not be loaded' });
    }
});

app.post('/api/guilds/:id/messages', authenticateToken, async (req, res) => {
    try {
        // Parse and validate guildId
        const guildId = parseInt(req.params.id);
        if (isNaN(guildId)) {
            return res.status(400).json({ error: 'Invalid guild ID' });
        }

        const userId = req.user.id;
        const { message } = req.body;

        if (!message || typeof message !== 'string') {
            return res.status(400).json({ error: 'Invalid message' });
        }

        const pool = await sql.connect(config);

        // Check if guild exists
        const guildCheck = await pool.request()
            .input('guildId', sql.Int, guildId)
            .query('SELECT 1 FROM Guilds WHERE id = @guildId');

        if (guildCheck.recordset.length === 0) {
            return res.status(404).json({ error: 'Guild not found' });
        }

        // Check guild membership
        const memberCheck = await pool.request()
            .input('guildId', sql.Int, guildId)
            .input('userId', sql.Int, userId)
            .query(`
                SELECT 1 FROM GuildMembers 
                WHERE guild_id = @guildId AND user_id = @userId
            `);

        if (memberCheck.recordset.length === 0) {
            return res.status(403).json({ error: 'You are not a member of this guild' });
        }

        // Insert the message
        const result = await pool.request()
            .input('guildId', sql.Int, guildId)
            .input('userId', sql.Int, userId)
            .input('message', sql.NVarChar, message)
            .query(`
                INSERT INTO GuildMessages (guild_id, user_id, message)
                VALUES (@guildId, @userId, @message);
                
                SELECT 
                    gm.*,
                    u.username,
                    u.display_name,
                    u.avatar_url,
                    u.level as user_level
                FROM GuildMessages gm
                JOIN Users u ON gm.user_id = u.id
                WHERE gm.id = SCOPE_IDENTITY();
            `);

        res.status(201).json(result.recordset[0]);
    } catch (err) {
        console.error('Guild message creation error:', err);
        res.status(500).json({ error: 'Message could not be sent to guild' });
    }
});

// Guild membership endpoints
app.post('/api/guilds/:id/join', authenticateToken, async (req, res) => {
    try {
        const guildId = req.params.id;
        const userId = req.user.id;

        const pool = await sql.connect(config);
        
        // Check if already a member
        const memberCheck = await pool.request()
            .input('guildId', sql.Int, guildId)
            .input('userId', sql.Int, userId)
            .query(`
                SELECT 1 FROM GuildMembers 
                WHERE guild_id = @guildId AND user_id = @userId
            `);

        if (memberCheck.recordset.length > 0) {
            return res.status(400).json({ error: 'Already a member of this guild' });
        }

        // Add user to guild
        await pool.request()
            .input('guildId', sql.Int, guildId)
            .input('userId', sql.Int, userId)
            .query(`
                INSERT INTO GuildMembers (guild_id, user_id)
                VALUES (@guildId, @userId)
            `);

        res.json({ message: 'Successfully joined guild' });
    } catch (err) {
        console.error('Guild join error:', err);
        res.status(500).json({ error: 'Could not join guild' });
    }
});

app.post('/api/guilds/:id/leave', authenticateToken, async (req, res) => {
    try {
        const guildId = parseInt(req.params.id);
        if (isNaN(guildId)) {
            return res.status(400).json({ error: 'Invalid guild ID' });
        }

        const userId = req.user.id;

        const pool = await sql.connect(config);
        
        await pool.request()
            .input('guildId', sql.Int, guildId)
            .input('userId', sql.Int, userId)
            .query(`
                DELETE FROM GuildMembers 
                WHERE guild_id = @guildId AND user_id = @userId
            `);

        res.json({ message: 'Successfully left guild' });
    } catch (err) {
        console.error('Guild leave error:', err);
        res.status(500).json({ error: 'Could not leave guild' });
    }
});

// Create a test user if it doesn't exist
async function createTestUser() {
    try {
        const pool = await sql.connect(config);
        const result = await pool.request()
            .query(`
                IF NOT EXISTS (SELECT 1 FROM Users WHERE username = 'testuser')
                BEGIN
                    INSERT INTO Users (username, password)
                    VALUES ('testuser', 'testpass123')
                END
            `);
        console.log('Test kullanıcısı kontrol edildi/oluşturuldu');
    } catch (err) {
        console.error('Test kullanıcısı oluşturma hatası:', err);
    }
}

// When the server starts, create a test user
const PORT = 3000;
app.listen(PORT, async () => {
    console.log(`Sunucu ${PORT} portunda çalışıyor`);
    await createTestUser();
});
