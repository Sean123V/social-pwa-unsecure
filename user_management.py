import sqlite3 as sql
import time
import random
import os
import bcrypt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "database_files", "database.db")
LOG_PATH = os.path.join(BASE_DIR, "visitor_log.txt")


def insertUser(username, password, DoB, bio=""):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    con = sql.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (username, password, dateOfBirth, bio) VALUES (?,?,?,?)",
        (username, hashed, DoB, bio),
    )
    con.commit()
    con.close()


def retrieveUsers(username, password):
    con = sql.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_row = cur.fetchone()
    con.close()

    if user_row is None:
        return False

    stored_password = user_row[2]
    if isinstance(stored_password, str):
        stored_password = stored_password.encode("utf-8")

    return bcrypt.checkpw(password.encode("utf-8"), stored_password)


def insertPost(author, content):
    con = sql.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("INSERT INTO posts (author, content) VALUES (?,?)", (author, content))
    con.commit()
    con.close()


def getPosts():
    con = sql.connect(DB_PATH)
    cur = con.cursor()
    data = cur.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    con.close()
    return data


def getUserProfile(username):
    con = sql.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT id, username, dateOfBirth, bio, role FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    con.close()
    return row


def getMessages(username):
    con = sql.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM messages WHERE recipient = ? ORDER BY id DESC", (username,))
    rows = cur.fetchall()
    con.close()
    return rows


def sendMessage(sender, recipient, body):
    con = sql.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("INSERT INTO messages (sender, recipient, body) VALUES (?,?,?)", (sender, recipient, body))
    con.commit()
    con.close()


def getVisitorCount():
    try:
        with open(LOG_PATH, "r") as f:
            return int(f.read().strip() or 0)
    except Exception:
        return 0


