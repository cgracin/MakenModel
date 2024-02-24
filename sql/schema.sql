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
    paint_id INTEGER,
    unique_paint_identifier VARCHAR(256),
    PRIMARY KEY (brand, paint_id)
);

-- User_Paints table
CREATE TABLE user_paints(
    username VARCHAR(256),
    paint_id VARCHAR(256),
    FOREIGN KEY (username) REFERENCES User(username) ON DELETE CASCADE,
    FOREIGN KEY (paint_id) REFERENCES Paints(paint_id) ON DELETE CASCADE,
    PRIMARY KEY (username, paint_id)
);
