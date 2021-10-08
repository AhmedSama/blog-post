import sqlite3
from os import path

ROOT = path.dirname(path.realpath(__file__))


def make_db():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("""create table IF NOT EXISTS flowers(
        flower_id integer not null,
        flowing_id integer not null
    )""")
    conn.commit()
    conn.close()


def add(flower_id,flowing_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("insert into flowers(flower_id,flowing_id) values(?,?)",
                (flower_id, flowing_id))
    conn.commit()
    conn.close()


def get_all():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("select rowid,* from flowers")
    conn.commit()
    data = cur.fetchall()
    conn.close()
    return data


def get_by(flowing_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("select users.rowid,users.username,users.img from users join flowers on users.rowid = flowers.flower_id where flowing_id = ?", (flowing_id,))
    conn.commit()
    data = cur.fetchall()
    conn.close()
    return data


def delete(flower_id, flowing_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("delete from flowers where flower_id = ? and flowing_id = ?",
                (flower_id, flowing_id))
    conn.commit()
    conn.close()
