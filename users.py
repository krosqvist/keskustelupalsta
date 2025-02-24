import db

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_conversations(user_id):
    sql = "SELECT id, title, modification_time FROM conversations WHERE user_id = ? ORDER BY id DESC LIMIT 50"
    result = db.query(sql, [user_id])
    if not result:
        result = ""

    sql = "SELECT COUNT(*) FROM conversations WHERE user_id = ? ORDER BY id DESC"
    conversation_count = db.query(sql, [user_id])
    if not conversation_count or conversation_count[0][0] is None:
        conversation_count = 0
    else:
        conversation_count = conversation_count[0][0]
    return result, conversation_count

def user_count():
    sql = "SELECT COUNT(*) FROM users"
    return db.query(sql)[0][0]

def find_users(search, page, page_size):
    sql = "SELECT id, username FROM users WHERE username LIKE ? ORDER BY username LIMIT ? OFFSET ?"
    limit = page_size
    offset = page_size * (page - 1)
    results = db.query(sql, [search, limit, offset])

    sql_count = "SELECT COUNT(*) FROM users WHERE username LIKE ? ORDER BY username"
    user_count = db.query(sql_count, [search])[0][0]
    return results, user_count

def get_comments(user_id):
    sql = "SELECT id, conversation_id, comment, modification_time FROM comments WHERE user_id = ? ORDER BY id DESC LIMIT 50"
    result = db.query(sql, [user_id])

    sql = "SELECT COUNT(*) FROM comments WHERE user_id = ? ORDER BY id DESC"
    comment_count = db.query(sql, [user_id])
    if not comment_count or comment_count[0][0] is None:
        comment_count = 0
    else:
        comment_count = comment_count[0][0]

    return result, comment_count