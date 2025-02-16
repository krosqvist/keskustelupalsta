import db
from datetime import datetime

def add_timestamp():
    now = datetime.now()
    formatted_time = now.strftime("%d.%m.%Y %H:%M:%S")
    return str(formatted_time)

def add_conversation(title, opening, user_id, classes, image):
    print(image)
    sql = "INSERT INTO conversations (title, opening, user_id, image, modification_time) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [title, opening, user_id, image, add_timestamp()])

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
    sql = """SELECT c.id, c.title, c.opening, c.modification_time, c.image, u.id user_id, u.username
          FROM conversations c, users u
          WHERE u.id = c.user_id AND
          c.id = ?"""
    result = db.query(sql, [conversation_id])
    return result[0] if result else None

def update_conversation(conversation_id, title, opening, classes, image):
    sql = """UPDATE conversations SET title = ?, opening = ?, image = ?, modification_time = ?
          WHERE id = ?"""
    db.execute(sql, [title, opening, image, add_timestamp(), conversation_id])

    sql = "DELETE FROM conversation_classes WHERE conversation_id = ?"
    db.execute(sql, [conversation_id])

    sql = "INSERT INTO conversation_classes (conversation_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        print(f"Inserting: ({conversation_id}, {class_title}, {class_value})")
        db.execute(sql, [conversation_id, class_title, class_value])

def delete_conversation(conversation_id):
    sql = "DELETE FROM conversation_classes WHERE conversation_id = ?"
    db.execute(sql, [conversation_id])
    sql = "DELETE FROM comments WHERE conversation_id = ?"
    db.execute(sql, [conversation_id])
    sql = "DELETE FROM conversations WHERE id = ?"
    db.execute(sql, [conversation_id])

def find_conversations(search):
    sql = "SELECT id, title FROM conversations WHERE title LIKE ? OR opening LIKE ? ORDER BY id DESC"
    return db.query(sql, [search, search])

def add_comment(comment, conversation_id, user_id):
    sql = "INSERT INTO comments (comment, conversation_id, user_id, modification_time) VALUES (?, ?, ?, ?)"
    db.execute(sql, [comment, conversation_id, user_id, add_timestamp()])

def get_comments(conversation_id):
    sql = """SELECT c.id, c.comment, c.modification_time, c.user_id, u.username
          FROM comments c, users u
          WHERE c.conversation_id = ? AND c.user_id = u.id
          ORDER BY c.id"""
    return db.query(sql, [conversation_id])

def check_comment(comment_id):
    sql = "SELECT id, conversation_id, user_id FROM comments WHERE id = ?"
    result = db.query(sql, [comment_id])
    return result[0] if result else None

def delete_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])

def get_image(conversation_id):
    sql = "SELECT image FROM conversations WHERE id = ?"
    result = db.query(sql, [conversation_id])
    return result[0][0]