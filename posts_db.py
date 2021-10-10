import sqlite3
from os import path

ROOT = path.dirname(path.realpath(__file__))

def make_db():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("""create table IF NOT EXISTS posts(
        user_id integer not null,
        title varchar(30) not null,
        content text not null,
        image varchar(60) not null,
        likes_number INT NOT NULL default 0,
        comments_number int not null default 0
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


def get_all_with_comments_number():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    # show the post and make the comments in one col together seperated by comma(,)
    cur.execute("""SELECT posts.title,posts.likes_number from posts""")
    # show all posts with one comment
    # cur.execute("""SELECT posts.rowid, posts.title,comments.user_id,comments.content
    #             FROM posts
    #              JOIN comments  ON posts.rowid = comments.post_id
    #             GROUP BY posts.rowid""")
    conn.commit()
    data = cur.fetchall()
    conn.close()
    return data


def get_one_with_comments_number(post_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    # show the post and make the comments in one col together seperated by comma(,)
    cur.execute("""SELECT posts.title,count(comments.content)
                FROM posts
                LEFT JOIN comments  ON posts.rowid = comments.post_id
               where posts.rowid = ? GROUP BY posts.rowid  """,(post_id,))
    # show all posts with one comment
    # cur.execute("""SELECT posts.rowid, posts.title,comments.user_id,comments.content
    #             FROM posts
    #              JOIN comments  ON posts.rowid = comments.post_id
    #             GROUP BY posts.rowid""")
    conn.commit()
    data = cur.fetchall()
    conn.close()
    return data
# print(get_all_with_comments())




def get_all():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    # cur.execute("select rowid,* from posts order by likes_number desc")
    cur.execute("select users.rowid,users.username,users.img,posts.rowid,posts.title,posts.content,posts.image,posts.likes_number,posts.user_id,posts.comments_number from users join posts on users.rowid = posts.user_id order by likes_number desc")
    conn.commit()
    data = cur.fetchall()
    conn.close()
    return data

def get_posts_i_liked(user_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    # cur.execute("select rowid,* from posts order by likes_number desc")
    cur.execute("select post_id from likes where likes.user_id = ?",(user_id,))
    conn.commit()
    data = cur.fetchall()
    # change the list from [(1,),(2,),(3,)]...etc to [1,2,3]
    def reduce(n):
        return n[0]
    data = map(reduce, data)
    conn.close()
    return list(data)



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

def update_comments(comments_number,post_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("update posts set comments_number = ? where rowid = ?",
                (comments_number, post_id))
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
        "select users.rowid,users.username,users.img,posts.rowid,posts.title,posts.content,posts.image,posts.likes_number,posts.comments_number from users join posts on users.rowid = posts.user_id where posts.rowid=?", (post_id,))
    conn.commit()
    data = cur.fetchone()
    conn.close()
    return data

