from flask import Flask,render_template,request,redirect,url_for,session
import models,posts_db,comments
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


@app.route("/idea/<int:post_id>")
def idea(post_id):
    if session.get("user"):
        id_ = session.get("user")[0]
        post = posts_db.get_by_id(post_id)
        post_comments = comments.get_by_id(post_id)
        return render_template("idea.html", username=session.get("user")[1].capitalize(), post=post, title=session.get("user")[2].capitalize(), bio=session.get("user")[3], img=session.get("user")[4], post_comments=post_comments)
    return render_template("login.html")


@app.route("/add_comment/<int:post_id>",methods=["POST"])
def add_comment(post_id):
    if session.get("user"):
        comment = request.form.get("comment")
        id_ = session.get("user")[0]
        comments.add(comment,post_id,id_)
        return redirect(url_for("idea",post_id=post_id))
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
    app.run(debug=True)











