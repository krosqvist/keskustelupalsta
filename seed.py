import random
import sqlite3

db = sqlite3.connect("database.db")
cursor = db.cursor()

cursor.execute("DELETE FROM users")
cursor.execute("DELETE FROM conversations")
cursor.execute("DELETE FROM conversation_classes")
cursor.execute("DELETE FROM comments")

total_users = 10**4
total_conversations = 10**6
total_comments = 10**7

for i in range(1, total_users + 1):
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                   (f"user{i}", f"hash{i}"))

for i in range(1, total_conversations + 1):
    user_id = random.randint(1, total_users)
    cursor.execute("INSERT INTO conversations (title, opening, user_id, modification_time) VALUES (?, ?, ?, datetime('now'))",
                   (f"Conversation {i}", f"Opening message {i}", user_id))

cursor.execute("SELECT id FROM conversations")
conversation_ids = [row[0] for row in cursor.fetchall()]

for i in range(1, total_comments + 1):
    user_id = random.randint(1, total_users)
    conversation_id = random.choice(conversation_ids)
    cursor.execute("INSERT INTO comments (conversation_id, user_id, comment, modification_time) VALUES (?, ?, ?, datetime('now'))",
                   (conversation_id, user_id, f"Comment {i}"))
    
db.commit()
db.close()