import db

def add_conversation(title, category, opening, user_id):
    sql = "INSERT INTO conversations (title, category, opening, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, category, opening, user_id])

def get_conversations():
    sql = "SELECT id, title FROM conversations ORDER BY id DESC"
    return db.query(sql)

def get_conversation(conversation_id):
    sql = """SELECT c.id, c.title, c.category, c.opening, u.id user_id, u.username
          FROM conversations c, users u
          WHERE u.id = c.user_id AND
          c.id = ?"""
    return db.query(sql, [conversation_id])[0]

def update_conversation(conversation_id, title, category, opening):
    sql = """UPDATE conversations SET title = ?, category = ?, opening = ?
          WHERE id = ?"""
    db.execute(sql, [title, category, opening, conversation_id])