-- Create or update Users table
IF OBJECT_ID('Users', 'U') IS NULL
BEGIN
    CREATE TABLE Users (
        id INT IDENTITY(1,1) PRIMARY KEY,
        username NVARCHAR(50) NOT NULL,
        password NVARCHAR(255) NOT NULL,
        display_name NVARCHAR(100),
        email NVARCHAR(100),
        avatar_url NVARCHAR(255),
        last_seen DATETIME,
        is_online BIT DEFAULT 0,
        created_at DATETIME DEFAULT GETDATE(),
        is_admin BIT DEFAULT 0,
        theme_preference NVARCHAR(20) DEFAULT 'light',
        notification_enabled BIT DEFAULT 1,
        level INT DEFAULT 1,
        experience INT DEFAULT 0,
        next_level_xp INT DEFAULT 100,
        CONSTRAINT UQ_Users_Username UNIQUE (username),
        CONSTRAINT UQ_Users_Email UNIQUE (email)
    );
END
ELSE
BEGIN
    IF COL_LENGTH('Users', 'theme_preference') IS NULL
        ALTER TABLE Users ADD theme_preference NVARCHAR(20) DEFAULT 'light';
    IF COL_LENGTH('Users', 'notification_enabled') IS NULL
        ALTER TABLE Users ADD notification_enabled BIT DEFAULT 1;
    IF COL_LENGTH('Users', 'level') IS NULL
        ALTER TABLE Users ADD level INT DEFAULT 1;
    IF COL_LENGTH('Users', 'experience') IS NULL
        ALTER TABLE Users ADD experience INT DEFAULT 0;
    IF COL_LENGTH('Users', 'next_level_xp') IS NULL
        ALTER TABLE Users ADD next_level_xp INT DEFAULT 100;
END
GO

-- Create or update Messages table
IF OBJECT_ID('Messages', 'U') IS NULL
BEGIN
    CREATE TABLE Messages (
        id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT,
        message NVARCHAR(MAX) NOT NULL,
        message_type NVARCHAR(20) DEFAULT 'text',
        is_edited BIT DEFAULT 0,
        is_deleted BIT DEFAULT 0,
        created_at DATETIME DEFAULT GETDATE(),
        edited_at DATETIME,
        reactions NVARCHAR(MAX),
        quoted_text NVARCHAR(MAX),
        quoted_message_id INT,
        CONSTRAINT FK_Messages_Users FOREIGN KEY (user_id) REFERENCES Users(id),
        CONSTRAINT FK_Messages_QuotedMessage FOREIGN KEY (quoted_message_id) REFERENCES Messages(id)
    );
END
ELSE
BEGIN
    IF COL_LENGTH('Messages', 'reactions') IS NULL
        ALTER TABLE Messages ADD reactions NVARCHAR(MAX);
    IF COL_LENGTH('Messages', 'quoted_text') IS NULL
        ALTER TABLE Messages ADD quoted_text NVARCHAR(MAX);
    IF COL_LENGTH('Messages', 'quoted_message_id') IS NULL
        ALTER TABLE Messages ADD quoted_message_id INT;
END
GO

-- Create or update AdminCommands table
IF OBJECT_ID('AdminCommands', 'U') IS NULL
BEGIN
    CREATE TABLE AdminCommands (
        id INT IDENTITY(1,1) PRIMARY KEY,
        command_name NVARCHAR(50) NOT NULL,
        description NVARCHAR(255),
        created_at DATETIME DEFAULT GETDATE()
    );
END
GO

-- Create or update UserBans table
IF OBJECT_ID('UserBans', 'U') IS NULL
BEGIN
    CREATE TABLE UserBans (
        id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT,
        banned_by INT,
        reason NVARCHAR(255),
        ban_date DATETIME DEFAULT GETDATE(),
        unban_date DATETIME,
        is_active BIT DEFAULT 1,
        CONSTRAINT FK_UserBans_Users FOREIGN KEY (user_id) REFERENCES Users(id),
        CONSTRAINT FK_UserBans_Admin FOREIGN KEY (banned_by) REFERENCES Users(id)
    );
END
GO

-- Create or update UserMutes table
IF OBJECT_ID('UserMutes', 'U') IS NULL
BEGIN
    CREATE TABLE UserMutes (
        id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT,
        muted_by INT,
        duration_minutes INT,
        mute_time DATETIME DEFAULT GETDATE(),
        unmute_time DATETIME,
        is_active BIT DEFAULT 1,
        CONSTRAINT FK_UserMutes_Users FOREIGN KEY (user_id) REFERENCES Users(id),
        CONSTRAINT FK_UserMutes_Admin FOREIGN KEY (muted_by) REFERENCES Users(id)
    );
END
GO

-- Create or update UserSettings table
IF OBJECT_ID('UserSettings', 'U') IS NULL
BEGIN
    CREATE TABLE UserSettings (
        user_id INT PRIMARY KEY,
        theme NVARCHAR(20) DEFAULT 'light',
        notifications_enabled BIT DEFAULT 1,
        display_name_color NVARCHAR(20) DEFAULT '#000000',
        custom_status NVARCHAR(100),
        CONSTRAINT FK_UserSettings_Users FOREIGN KEY (user_id) REFERENCES Users(id)
    );
END
GO

-- Create or update Tags table
IF OBJECT_ID('Tags', 'U') IS NULL
BEGIN
    CREATE TABLE Tags (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(50) NOT NULL,
        required_level INT NOT NULL,
        color_hex NVARCHAR(7) NOT NULL
    );
END
GO

-- Insert default tags if not exists
IF NOT EXISTS (SELECT 1 FROM Tags)
BEGIN
    INSERT INTO Tags (name, required_level, color_hex) VALUES
    ('Çaylak', 1, '#808080'),
    ('Acemi', 5, '#32CD32'),
    ('Meraklı', 10, '#4169E1'),
    ('Tutkulu', 15, '#9370DB'),
    ('Uzman', 20, '#FFD700'),
    ('Üstat', 25, '#FF4500'),
    ('Efsane', 30, '#8B0000'),
    ('Şampiyon', 35, '#4B0082'),
    ('Kahraman', 40, '#FF1493'),
    ('Efsanevi', 45, '#FF0000'),
    ('Destansı', 50, '#8B4513'),
    ('İmparator', 55, '#DAA520'),
    ('Tanrısal', 60, '#00FFFF'),
    ('Kozmik', 65, '#9400D3'),
    ('Mitolojik', 70, '#FF00FF'),
    ('Galaktik', 75, '#1E90FF'),
    ('Evrensel', 80, '#FF8C00'),
    ('Ultra', 85, '#FF0000'),
    ('Mega', 90, '#7CFC00'),
    ('Nihai', 100, '#FFD700');
END
GO

-- Create or update Announcements table
IF OBJECT_ID('Announcements', 'U') IS NULL
BEGIN
    CREATE TABLE Announcements (
        id INT IDENTITY(1,1) PRIMARY KEY,
        message NVARCHAR(MAX) NOT NULL,
        created_at DATETIME DEFAULT GETDATE()
    );
END
GO

-- Insert default admin commands if not exists
IF NOT EXISTS (SELECT 1 FROM AdminCommands)
BEGIN
    INSERT INTO AdminCommands (command_name, description) VALUES
    ('/clear', 'Tüm mesajları temizler'),
    ('/ban', 'Kullanıcıyı banlar'),
    ('/unban', 'Kullanıcının banını kaldırır'),
    ('/mute', 'Kullanıcıyı susturur'),
    ('/unmute', 'Kullanıcının susturmasını kaldırır'),
    ('/edit', 'Son mesajı düzenler'),
    ('/delete', 'Belirtilen mesajı siler'),
    ('/announce', 'Duyuru yapar');
END
GO

-- Drop existing procedure if it exists
IF OBJECT_ID('UpdateUserExperience', 'P') IS NOT NULL
    DROP PROCEDURE UpdateUserExperience;
GO

-- Experience update procedure
CREATE PROCEDURE UpdateUserExperience
    @userId INT,
    @messageLength INT
AS
BEGIN
    DECLARE @currentXP INT, @currentLevel INT, @nextLevelXP INT;
    
    -- Her karakter için 1 XP, her kelime için 5 XP ekle
    SET @messageLength = @messageLength + (LEN(@messageLength) - LEN(REPLACE(@messageLength, ' ', '')) * 5);
    
    -- Mevcut değerleri al
    SELECT @currentXP = experience, @currentLevel = level, @nextLevelXP = next_level_xp
    FROM Users WHERE id = @userId;
    
    -- XP'yi güncelle
    SET @currentXP = @currentXP + @messageLength;
    
    -- Level kontrolü
    WHILE @currentXP >= @nextLevelXP
    BEGIN
        SET @currentLevel = @currentLevel + 1;
        SET @currentXP = @currentXP - @nextLevelXP;
        SET @nextLevelXP = @nextLevelXP * 1.5; -- Her level için %50 daha fazla XP gerekir
    END
    
    -- Kullanıcıyı güncelle
    UPDATE Users 
    SET experience = @currentXP,
        level = @currentLevel,
        next_level_xp = @nextLevelXP
    WHERE id = @userId;
END
GO

-- Drop existing trigger if it exists
IF OBJECT_ID('TR_Messages_XP', 'TR') IS NOT NULL
    DROP TRIGGER TR_Messages_XP;
GO

-- Create XP Update Trigger
CREATE TRIGGER TR_Messages_XP
ON Messages
AFTER INSERT
AS
BEGIN
    DECLARE @userId INT, @messageLength INT;
    
    SELECT @userId = user_id, 
           @messageLength = LEN(message)
    FROM inserted;
    
    -- Base XP calculation (1 XP per character + 5 XP per word)
    DECLARE @baseXP INT = @messageLength;
    DECLARE @wordCount INT = LEN(@messageLength) - LEN(REPLACE(@messageLength, ' ', '')) + 1;
    SET @baseXP = @baseXP + (@wordCount * 5);

    -- Update user XP and check for level up
    EXEC UpdateUserExperience @userId, @baseXP;
END
GO
