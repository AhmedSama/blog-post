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


def alter():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("ALTER TABLE posts ADD likes_number INT NOT NULL DEFAULT 0")
    conn.commit()
    conn.close()




def get_all():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("select rowid,* from posts order by likes_number desc")
    conn.commit()
    data = cur.fetchall()
    conn.close()
    return data

def get_likes_number(post_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute(
        "select likes_number from posts where rowid = ?",(post_id,))
    conn.commit()
    data = cur.fetchone()
    conn.close()
    return data[0]

def delete(id_):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("delete from posts where rowid = ?",(id_,))
    conn.commit()
    conn.close()

def update(likes_number,post_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("update posts set likes_number = ? where rowid = ?",
                (likes_number, post_id))
    conn.commit()
    conn.close()



def get_by(user_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("select rowid,* from posts where user_id=? order by rowid desc", (user_id,))
    conn.commit()
    data = cur.fetchall()
    conn.close()
    return data


def get_by_id(post_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute(
        "select rowid,* from posts where rowid=?", (post_id,))
    conn.commit()
    data = cur.fetchone()
    conn.close()
    return data
