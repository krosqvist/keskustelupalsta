import db

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_conversations(user_id):
    sql = "SELECT id, title, modification_time FROM conversations WHERE user_id = ? ORDER BY id DESC"
    result = db.query(sql, [user_id])
    return result if result else ""

def find_users(search):
    sql = "SELECT id, username FROM users WHERE username LIKE ? ORDER BY username"
    return db.query(sql, [search])

def get_comments(user_id):
    sql = "SELECT id, conversation_id, comment, modification_time FROM comments WHERE user_id = ? ORDER BY id DESC"
    return db.query(sql, [user_id])