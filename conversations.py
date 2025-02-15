import db
from datetime import datetime

def add_timestamp():
    now = datetime.now()
    formatted_time = now.strftime("%d.%m.%Y %H:%M:%S")
    return str(formatted_time)

def add_conversation(title, opening, user_id, classes):
    sql = "INSERT INTO conversations (title, opening, user_id, modification_time) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, opening, user_id, add_timestamp()])

    conversation_id = db.last_insert_id()
    print("conversation_id when creating", conversation_id)
    sql = "INSERT INTO conversation_classes (conversation_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [conversation_id, title, value])

    return conversation_id

def get_classes(conversation_id):
    sql = "SELECT title, value FROM conversation_classes WHERE conversation_id = ?"
    return db.query(sql, [conversation_id])

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)
    return classes

def get_conversations():
    sql = "SELECT id, title FROM conversations ORDER BY id DESC"
    return db.query(sql)

def get_conversation(conversation_id):
    sql = """SELECT c.id, c.title, c.opening, c.modification_time, u.id user_id, u.username
          FROM conversations c, users u
          WHERE u.id = c.user_id AND
          c.id = ?"""
    result = db.query(sql, [conversation_id])
    return result[0] if result else None

def update_conversation(conversation_id, title, opening, classes):
    sql = """UPDATE conversations SET title = ?, opening = ?, modification_time = ?
          WHERE id = ?"""
    db.execute(sql, [title, opening, add_timestamp(), conversation_id])

    before_delete = db.query("SELECT * FROM conversation_classes WHERE conversation_id = ?", [conversation_id])
    print(f"Rows before DELETE: {before_delete}")

    sql = "DELETE FROM conversation_classes WHERE conversation_id = ?"
    db.execute(sql, [conversation_id])

    after_delete = db.query("SELECT * FROM conversation_classes WHERE conversation_id = ?", [conversation_id])
    print(f"Rows after DELETE: {after_delete}")

    sql = "INSERT INTO conversation_classes (conversation_id, title, value) VALUES (?, ?, ?)"
    print("conversation_id when updating", conversation_id)
    #sql = "UPDATE conversation_classes SET value = ? WHERE conversation_id = ? AND title = ?"
    for class_title, class_value in classes:
        print(f"Inserting: ({conversation_id}, {class_title}, {class_value})")
        db.execute(sql, [conversation_id, class_title, class_value])

def delete_conversation(conversation_id):
    sql = "DELETE FROM conversation_classes WHERE conversation_id = ?"
    db.execute(sql, [conversation_id])
    sql = "DELETE FROM conversations WHERE id = ?"
    db.execute(sql, [conversation_id])

def find_conversations(params):
    if len(params) == 1:
        sql = "SELECT id, title FROM conversations WHERE title LIKE ? ORDER BY id DESC"
    else:
        sql = "SELECT id, title FROM conversations WHERE title LIKE ? AND category = ? ORDER BY id DESC"
    return db.query(sql, params)

def add_comment(comment, conversation_id, user_id):
    sql = "INSERT INTO comments (comment, conversation_id, user_id, modification_time) VALUES (?, ?, ?, ?)"
    db.execute(sql, [comment, conversation_id, user_id, add_timestamp()])

def get_comments(conversation_id):
    sql = """SELECT c.comment, c.modification_time, c.user_id, u.username
          FROM comments c, users u
          WHERE c.conversation_id = ? AND c.user_id = u.id
          ORDER BY c.id"""
    return db.query(sql, [conversation_id])