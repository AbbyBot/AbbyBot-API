CREATE TABLE bot_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    bot_id BIGINT NOT NULL,
    bot_name VARCHAR(255) NOT NULL,
    discriminator VARCHAR(10),
    avatar_url VARCHAR(500),
    banner_url VARCHAR(500),
    version VARCHAR(10) NOT NULL,
    server_count INT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
