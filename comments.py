import sqlite3
from os import path

ROOT = path.dirname(path.realpath(__file__))


def make_db():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("""create table IF NOT EXISTS comments(
        content text not null,
        post_id integer not null,
        user_id integer not null
    )""")
    conn.commit()
    conn.close()


def add(content, post_id, user_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("insert into comments(content, post_id, user_id) values(?,?,?)",
                (content, post_id, user_id))
    conn.commit()
    conn.close()


def get_all():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("select rowid,* from comments")
    conn.commit()
    data = cur.fetchall()
    conn.close()
    return data

def get_comments_number(post_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("select count(*) from comments where post_id = ?",(post_id,))
    conn.commit()
    data = cur.fetchone()
    conn.close()
    return data[0]

def delete(id_):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("delete from comments where rowid = ?", (id_,))
    conn.commit()
    conn.close()


def get_by_id(post_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute(
        "select comments.content,users.username,users.img from comments join users on users.rowid = comments.user_id where comments.post_id=? order by comments.rowid desc", (post_id,))
    conn.commit()
    data = cur.fetchall()
    conn.close()
    return data

def get_by_id_api(post_id, offset, limit):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    # limit ?,?",(offset,limit)
    cur.execute(
        "select comments.content,users.username,users.img from comments join users on users.rowid = comments.user_id where comments.post_id=? order by comments.rowid desc limit ?,?", (post_id, offset, limit))
    conn.commit()
    data = cur.fetchall()
    conn.close()
    return data
