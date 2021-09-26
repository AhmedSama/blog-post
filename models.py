import sqlite3
from os import path

ROOT = path.dirname(path.realpath(__file__))

def make_db():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("""create table IF NOT EXISTS users(
        username varchar(30) not null,
        email varchar(30) not null,
        pwd varchar(60) not null,
        title varchar(30) not null,
        bio text not null,
        img varchar(60)
    )""")
    conn.commit()
    conn.close()

def add(username,email,pwd,title,bio):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("insert into users(username,email,pwd,title,bio) values(?,?,?,?,?)",
                (username, email, pwd, title, bio))
    conn.commit()
    conn.close()


def get_all():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("select rowid,* from users")
    conn.commit()
    data = cur.fetchall()
    conn.close()
    return data

def get_by(id_):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("select rowid,* from users where rowid=?",(id_,))
    conn.commit()
    data = cur.fetchone()
    conn.close()
    return data

def select_by(username,pwd):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute(
        "select rowid,username,title,bio,img from users where username=? and pwd=?", (username, pwd))
    conn.commit()
    data = cur.fetchone()
    conn.close()
    return data

def update(img_url,id_):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("update users set img = ? where rowid = ?", (img_url, id_))
    conn.commit()
    conn.close()









