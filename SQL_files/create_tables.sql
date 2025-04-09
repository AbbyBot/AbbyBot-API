DROP TABLE IF EXISTS bot_info;

CREATE TABLE bot_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    bot_id BIGINT NOT NULL,
    bot_name VARCHAR(255) NOT NULL,
    discriminator VARCHAR(10),
    avatar_url VARCHAR(500),
    banner_url VARCHAR(500),
    version VARCHAR(10) NOT NULL,
    server_count INT DEFAULT 0,
    status VARCHAR(10) DEFAULT 'offline', 
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO bot_info (bot_id, bot_name, discriminator, avatar_url, banner_url, version, server_count, status) 
VALUES (123456789012345678, 'Bot-Name', '1234', 'https://example.com/avatar.png', 'https://example.com/banner.png', '1.0.0', 10, 'offline');