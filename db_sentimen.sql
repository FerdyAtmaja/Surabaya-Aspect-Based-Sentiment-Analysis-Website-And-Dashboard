-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS db_sentimen;

-- Use the database
USE db_sentimen;

-- Membuat tabel aspek
CREATE TABLE aspect (
    aspect_id INT AUTO_INCREMENT PRIMARY KEY,
    aspect VARCHAR(100) NOT NULL,
    keywords TEXT
);

-- Membuat tabel sentiment_analysis
CREATE TABLE sentiment_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tanggal_keluhan DATETIME NOT NULL,
    keluhan TEXT NOT NULL,
    preprocessed_text TEXT,
    sentimen ENUM('negatif', 'netral') NOT NULL,
    aspect_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Definisi foreign key
    FOREIGN KEY (aspect_id) REFERENCES aspect(aspect_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);