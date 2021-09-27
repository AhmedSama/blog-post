from flask import Flask,render_template,request,redirect,url_for,session,jsonify
import models,posts_db,comments,likes
from os import path,mkdir

ROOT = path.dirname(path.abspath(__file__))

app = Flask(__name__)
app.secret_key = "uysiojxoasidbh"
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        pwd = request.form.get("pwd")
        title = request.form.get("title")
        bio = request.form.get("bio")
        img = request.files.get("img")
        models.add(username, email, pwd, title, bio)
        data = models.select_by(username,pwd)
        id_ = data[0]
        img_url = "images/media/" +str(id_)+"/"+"profile_"+str(id_)+"/"+img.filename
        # make him a file for his posts with the name of his id
        mkdir(path.join(ROOT,"static","images","media",str(id_)))
        # make folder inside the user images folder to save the profile image  
        mkdir(path.join(ROOT, "static", "images",
                        "media", str(id_), "profile_"+str(id_)))
        img.save(path.join(ROOT, "static", "images",
                           "media", str(id_), "profile_"+str(id_), img.filename))
        models.update(img_url,id_)
        return render_template("login.html")
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")

        # if the user is not exist in database
        user = models.select_by(username,pwd)
        if user == None:
            return render_template("login.html")
        # if user is exists we make the session for the login
        # we have to make sure the session is not exists so he is not loged in yet!
        if session.get("user") is not None:
            session.pop("user", None)
            session["user"] = user
            return redirect(url_for("profile"))
        else:
            session["user"] = user
            return redirect(url_for("profile"))
    return render_template("login.html")


@app.route("/profile")
def profile():
    if session.get("user"):
        id_ = session.get("user")[0]

        posts = posts_db.get_by(id_)
        return render_template("profile.html", username=session.get("user")[1].capitalize(), posts=posts, title=session.get("user")[2].capitalize(), bio=session.get("user")[3], img=session.get("user")[4])
    return render_template("login.html")


@app.route("/ideas")
def ideas():
    if session.get("user"):
        id_ = session.get("user")[0]
        posts = posts_db.get_by(id_)
        return render_template("ideas.html", username=session.get("user")[1].capitalize(), posts=posts, title=session.get("user")[2].capitalize(), bio=session.get("user")[3], img=session.get("user")[4])
    return render_template("login.html")


@app.route("/all_ideas")
def all_ideas():
    if session.get("user"):
        id_ = session.get("user")[0]
        posts =posts_db.get_all()
        liked_posts = posts_db.get_posts_i_liked(id_)
        return render_template("all_ideas.html", username=session.get("user")[1].capitalize(), posts=posts, title=session.get("user")[2].capitalize(), bio=session.get("user")[3], img=session.get("user")[4], liked_posts=liked_posts)
    return render_template("login.html")



@app.route("/comments_api/<int:post_id>",methods=["POST"])
def comment_api(post_id):
    # data containes offset and limit
    data = request.get_json()
    offset = data.get("off")
    limit = data.get("lim") 
    # putting + 1 to cheack if there is any more data or not
    comments_data = comments.get_by_id_api(post_id,offset,limit+1)
    if comments_data:
        # if number of comments left is less than limit + 1 then there is no more comments
        if len(comments_data) < limit + 1:
            return jsonify({"comments": comments_data,"end":True})
        # if number of comments equal to limit + 1 then there are comments left
        elif len(comments_data) == limit + 1:
            # we remove the last comment cuz we need comments = limit number
            comments_data.pop()
            return jsonify({"comments": comments_data, "end": False})
    else:
        return jsonify({"comments": "empty"})
    

@app.route("/idea/<int:post_id>")
def idea(post_id):
    if session.get("user"):
        id_ = session.get("user")[0]
        post = posts_db.get_by_id(post_id)
        likes_number = likes.count_likes(post_id)
        if likes.get_by(post_id, id_) == []:
            liked  = False
        else:
            liked = True
        return render_template("idea.html", username=session.get("user")[1].capitalize(), post=post, title=session.get("user")[2].capitalize(), bio=session.get("user")[3], img=session.get("user")[4], likes_number=likes_number,liked=liked)
    return render_template("login.html")

# comminting feature
@app.route("/add_comment/<int:post_id>",methods=["POST"])
def add_comment(post_id):
    if session.get("user"):
        comment = request.get_json()
        comment = comment.get("the_comment")
        # TODO handling empty comments later
        if comment == "":
            return jsonify({"error":"no comment"})

        id_ = session.get("user")[0]
        user_data = models.get_by(id_)
        name = user_data[1]
        img = user_data[6]

        comments.add(comment,post_id,id_)
        return jsonify({"comment":comment,"name":name ,"img":img })
    return render_template("login.html")

# test api
@app.route("/test_api/<int:post_id>", methods=["POST"])
def test_api(post_id):
    if session.get("user"):
        data = request.get_json()
        print(data.get("the_comment"))
        the_comment = data.get("the_comment")
        send_data = {"comment": the_comment}
        return jsonify(send_data)
    return render_template("login.html")


# liking feature
@app.route("/add_like/<int:post_id>", methods=["POST"])
def add_like(post_id):
    if session.get("user"):
        id_ = session.get("user")[0]
        if likes.get_by(post_id,id_) == []:
            likes.add(post_id,id_)
            # likes_number = posts_db.get_likes_number(post_id)
            likes_number = likes.count_likes(post_id)
            posts_db.update(likes_number,post_id)
            return jsonify({"like":likes_number,"done":True})
        else:
            likes.delete(post_id, id_)
            likes_number = likes.count_likes(post_id)
            posts_db.update(likes_number, post_id)
            return jsonify({"like": likes_number, "done": False})
    return render_template("login.html")


@app.route("/post",methods=["GET","POST"])
def post():
    if request.method =="GET":
        return render_template("post.html")
    
    # here we handle the POST request
    if session.get("user"):
        title = request.form.get("title")
        content = request.form.get("content")
        img = request.files.get("img")
        id_ = session.get("user")[0]
        img.save(path.join(ROOT, "static", "images",
                           "media", str(id_), img.filename))
        img_url = "images/media/"+str(id_)+"/"+img.filename
        posts_db.add(id_, title, content,img_url)
        posts = posts_db.get_by(id_)
        return redirect(url_for("profile"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    if session.get("user"):
        session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    models.make_db()
    posts_db.make_db()
    comments.make_db()
    likes.make_db()
    app.run(debug=True)











