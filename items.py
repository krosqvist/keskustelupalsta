import db

def add_item(title, category, opening, user_id):
    sql = "INSERT INTO conversations (title, category, opening, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, category, opening, user_id])