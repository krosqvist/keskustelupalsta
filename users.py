import db

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_conversations(user_id):
    sql = "SELECT id, title FROM conversations WHERE user_id = ? ORDER BY id DESC"
    result = db.query(sql, [user_id])
    return result if result else ""