CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    title TEXT,
    category TEXT,
    opening TEXT,
    user_id INTEGER REFERENCES users
);