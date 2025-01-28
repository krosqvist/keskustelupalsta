import db

def add_conversation(title, category, opening, user_id):
    sql = "INSERT INTO conversations (title, category, opening, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, category, opening, user_id])

def get_conversations():
    sql = "SELECT id, title FROM conversations ORDER BY id DESC"
    return db.query(sql)

def get_conversation(conversation_id):
    sql = """SELECT c.title, c.category, c.opening, u.username
          FROM conversations c, users u
          WHERE u.id = c.user_id AND
          c.id = ?"""
    return db.query(sql, [conversation_id])[0]