import sqlite3
from os import path

ROOT = path.dirname(path.realpath(__file__))

def make_db():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("""create table posts(
        user_id integer not null,
        title varchar(30) not null,
        content text not null,
        image varchar(60) not null
    )""")
    conn.commit()
    conn.close()

def add(user_id, title, content, image):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("insert into posts(user_id, title, content, image) values(?,?,?,?)",
                (user_id, title, content, image))
    conn.commit()
    conn.close()


def get_all():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("select rowid,* from posts")
    conn.commit()
    data = cur.fetchall()
    conn.close()
    return data


def delete(id_):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("delete from posts where rowid = ?",(id_,))
    conn.commit()
    data = cur.fetchall()
    conn.close()
    return data


def get_by(user_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("select rowid,* from posts where user_id=?", (user_id,))
    conn.commit()
    data = cur.fetchall()
    conn.close()
    return data

