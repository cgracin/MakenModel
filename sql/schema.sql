PRAGMA foreign_keys = ON;

-- User table
CREATE TABLE users(
    username VARCHAR(256) PRIMARY KEY,
    password VARCHAR(40),
    email VARCHAR(48),
    profile_pic_filename VARCHAR(256),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Paints table
CREATE TABLE paints(
    brand VARCHAR(50),
    unique_paint_identifier INTEGER PRIMARY KEY AUTOINCREMENT,
    paint_code VARCHAR(256),
    background_color VARCHAR(12),
    shine_type VARCHAR(20),
    paint_type VARCHAR(20),
    FOREIGN KEY (brand) REFERENCES brands(brand)
);

-- Brands table
CREATE TABLE brands(
    brand VARCHAR(50),
    num_paints INTEGER,
    unique_brand_identifier INTEGER PRIMARY KEY AUTOINCREMENT
);

-- User_Paints table
CREATE TABLE user_paints(
    username VARCHAR(256),
    unique_paint_identifier INTEGER,
    FOREIGN KEY (username) REFERENCES User(username) ON DELETE CASCADE,
    FOREIGN KEY (unique_paint_identifier) REFERENCES Paints(unique_paint_identifier) ON DELETE CASCADE,
    PRIMARY KEY (username, unique_paint_identifier)
);
