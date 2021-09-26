import sqlite3
from os import path

ROOT = path.dirname(path.realpath(__file__))


def make_db():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("""create table IF NOT EXISTS likes(
        post_id integer not null,
        user_id integer not null
    )""")
    conn.commit()
    conn.close()


def add(post_id, user_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("insert into likes( post_id, user_id) values(?,?)",
                (post_id, user_id))
    conn.commit()
    conn.close()


def get_all():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute(
        "select likes.user_id,posts.content  from posts inner join likes on posts.rowid=likes.post_id ")
    conn.commit()
    data = cur.fetchall()
    conn.close()
    return data


def delete(post_id, user_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute(
        "delete from likes where post_id = ? and user_id = ?", (post_id, user_id))
    conn.commit()
    conn.close()



def count_likes(post_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("select count(post_id) from likes where post_id = ?", (post_id,))
    conn.commit()
    data = cur.fetchone()
    conn.close()
    return data[0]

def get_by(post_id,user_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute(
        "select * from likes where post_id=? and user_id = ?", (post_id,user_id))
    conn.commit()
    data = cur.fetchall()
    conn.close()
    return data









