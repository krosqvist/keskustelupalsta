import db
from datetime import datetime
from flask import g

def add_timestamp():
    now = datetime.now()
    formatted_time = now.strftime("%d.%m.%Y %H:%M:%S")
    return str(formatted_time)

def add_conversation(title, category, opening, user_id):
    sql = "INSERT INTO conversations (title, category, opening, user_id, modification_time) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [title, category, opening, user_id, add_timestamp()])
    return g.last_insert_id

def get_conversations():
    sql = "SELECT id, title FROM conversations ORDER BY id DESC"
    return db.query(sql)

def get_conversation(conversation_id):
    sql = """SELECT c.id, c.title, c.category, c.opening, c.modification_time, u.id user_id, u.username
          FROM conversations c, users u
          WHERE u.id = c.user_id AND
          c.id = ?"""
    return db.query(sql, [conversation_id])[0]

def update_conversation(conversation_id, title, category, opening):
    sql = """UPDATE conversations SET title = ?, category = ?, opening = ?, modification_time = ?
          WHERE id = ?"""
    db.execute(sql, [title, category, opening, add_timestamp(), conversation_id])

def delete_conversation(conversation_id):
    sql = "DELETE FROM conversations WHERE id = ?"
    db.execute(sql, [conversation_id])
