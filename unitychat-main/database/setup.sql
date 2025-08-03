USE master
GO

IF EXISTS (SELECT * FROM sys.databases WHERE name = 'ChatApp')
    DROP DATABASE ChatApp
GO

CREATE DATABASE ChatApp;
GO

USE ChatApp;
GO

-- Drop existing tables if they exist
IF OBJECT_ID('Messages', 'U') IS NOT NULL DROP TABLE Messages;
IF OBJECT_ID('Users', 'U') IS NOT NULL DROP TABLE Users;
IF OBJECT_ID('AdminCommands', 'U') IS NOT NULL DROP TABLE AdminCommands;
IF OBJECT_ID('UserBans', 'U') IS NOT NULL DROP TABLE UserBans;
IF OBJECT_ID('Tags', 'U') IS NOT NULL DROP TABLE Tags;
IF OBJECT_ID('Announcements', 'U') IS NOT NULL DROP TABLE Announcements;
GO

-- Create Users table
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
GO

-- Create Messages table
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
GO

-- Create AdminCommands table
CREATE TABLE AdminCommands (
    id INT IDENTITY(1,1) PRIMARY KEY,
    command_name NVARCHAR(50) NOT NULL,
    description NVARCHAR(255),
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- Create UserBans table
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
GO

-- Create UserMutes table
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
GO

-- Create Settings table
CREATE TABLE UserSettings (
    user_id INT PRIMARY KEY,
    theme VARCHAR(20) DEFAULT 'light',
    notifications_enabled BIT DEFAULT 1,
    display_name_color VARCHAR(20) DEFAULT '#000000',
    custom_status NVARCHAR(100),
    CONSTRAINT FK_UserSettings_Users FOREIGN KEY (user_id) REFERENCES Users(id)
);
GO

-- Create Tags table
CREATE TABLE Tags (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(50) NOT NULL,
    required_level INT NOT NULL,
    color_hex NVARCHAR(7) NOT NULL
);
GO

-- Insert default tags
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
GO

-- Create first admin user
INSERT INTO Users (username, password, email, display_name, is_admin)
VALUES ('admin', '$2b$10$xxxxxxxxxxx', 'admin@unitychat.com', 'Admin', 1);
GO

-- Insert default admin commands
INSERT INTO AdminCommands (command_name, description) VALUES
('/clear', 'Tüm mesajları temizler'),
('/ban', 'Kullanıcıyı banlar'),
('/unban', 'Kullanıcının banını kaldırır'),
('/mute', 'Kullanıcıyı susturur'),
('/unmute', 'Kullanıcının susturmasını kaldırır'),
('/edit', 'Son mesajı düzenler'),
('/delete', 'Belirtilen mesajı siler'),
('/announce', 'Duyuru yapar');
GO

-- Create Announcements table
CREATE TABLE Announcements (
    id INT IDENTITY(1,1) PRIMARY KEY,
    message NVARCHAR(MAX) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- Create Guilds table
CREATE TABLE Guilds (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    description NVARCHAR(255),
    creator_id INT,
    created_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_Guilds_Creator FOREIGN KEY (creator_id) REFERENCES Users(id)
);
GO

-- Create GuildMembers table
CREATE TABLE GuildMembers (
    id INT IDENTITY(1,1) PRIMARY KEY,
    guild_id INT,
    user_id INT,
    joined_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_GuildMembers_Guilds FOREIGN KEY (guild_id) REFERENCES Guilds(id),
    CONSTRAINT FK_GuildMembers_Users FOREIGN KEY (user_id) REFERENCES Users(id)
);
GO

-- Create GuildMessages table
CREATE TABLE GuildMessages (
    id INT IDENTITY(1,1) PRIMARY KEY,
    guild_id INT,
    user_id INT,
    message NVARCHAR(MAX) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_GuildMessages_Guilds FOREIGN KEY (guild_id) REFERENCES Guilds(id),
    CONSTRAINT FK_GuildMessages_Users FOREIGN KEY (user_id) REFERENCES Users(id)
);
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

-- Create stored procedure to create a guild
CREATE PROCEDURE CreateGuild
    @name NVARCHAR(100),
    @description NVARCHAR(255),
    @userId INT
AS
BEGIN
    DECLARE @guildId INT;

    -- Insert new guild
    INSERT INTO Guilds (name, description, creator_id)
    VALUES (@name, @description, @userId);

    SET @guildId = SCOPE_IDENTITY();

    -- Add creator as guild member
    INSERT INTO GuildMembers (guild_id, user_id)
    VALUES (@guildId, @userId);
END
GO

-- Create Guilds table if it doesn't exist
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Guilds' AND xtype='U')
CREATE TABLE Guilds (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETDATE()
);

-- Create GuildMembers table if it doesn't exist
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='GuildMembers' AND xtype='U')
CREATE TABLE GuildMembers (
    guild_id INT,
    user_id INT,
    joined_at DATETIME DEFAULT GETDATE(),
    PRIMARY KEY (guild_id, user_id),
    FOREIGN KEY (guild_id) REFERENCES Guilds(id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Insert a sample guild if it doesn't exist
IF NOT EXISTS (SELECT * FROM Guilds WHERE id = 1)
INSERT INTO Guilds (name, description) VALUES ('Sample Guild', 'This is a sample guild for testing purposes.');

-- Insert a sample guild member if it doesn't exist
IF NOT EXISTS (SELECT * FROM GuildMembers WHERE guild_id = 1 AND user_id = 1)
INSERT INTO GuildMembers (guild_id, user_id) VALUES (1, 1);
GO
