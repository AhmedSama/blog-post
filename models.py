import sqlite3

def make_db():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("""create table users(
        username varchar(30) not null,
        email varchar(30) not null,
        pwd varchar(60) not null
    )""")
    conn.commit()
    conn.close()


def add(username,email,pwd):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("insert into users(username,email,pwd) values(?,?,?)",
                (username, email, pwd))
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
        "select rowid,* from users where username=? and pwd=?", (username, pwd))
    conn.commit()
    data = cur.fetchone()
    conn.close()
    return data

print(select_by("ahmed","12342"))








