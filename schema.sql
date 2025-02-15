CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    title TEXT,
    opening TEXT,
    user_id INTEGER REFERENCES users,
    modification_time TEXT
);

CREATE TABLE conversation_classes (
    id INTEGER PRIMARY KEY,
    conversation_id INTEGER,
    title TEXT,
    value TEXT,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations,
    user_id INTEGER REFERENCES users,
    comment TEXT,
    modification_time TEXT
);