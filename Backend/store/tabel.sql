DROP DATABASE floor_eye;
CREATE DATABASE floor_eye;
USE floor_eye;

CREATE TABLE floor_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(20) NOT NULL,
    is_dirty BOOLEAN NOT NULL,
    confidence FLOAT NULL,
    notes TEXT NULL,
    image_path TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
