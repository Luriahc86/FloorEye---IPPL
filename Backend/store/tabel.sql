CREATE DATABASE IF NOT EXISTS floor_eye;
USE floor_eye;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin','staff') NOT NULL DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE cctv (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    stream_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE cleaning_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cctv_id INT,
    staff_id INT,
    cleanliness_status ENUM('bersih', 'kotor', 'butuh perhatian') NOT NULL,
    notes TEXT,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_cleaning_cctv 
        FOREIGN KEY (cctv_id) REFERENCES cctv(id) ON DELETE SET NULL,

    CONSTRAINT fk_cleaning_staff 
        FOREIGN KEY (staff_id) REFERENCES users(id) ON DELETE SET NULL
);


CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    staff_id INT NOT NULL,
    report_id INT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_notif_staff 
        FOREIGN KEY (staff_id) REFERENCES users(id) ON DELETE CASCADE,

    CONSTRAINT fk_notif_report 
        FOREIGN KEY (report_id) REFERENCES cleaning_reports(id) ON DELETE CASCADE
);