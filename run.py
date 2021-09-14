from flask import Flask,render_template,request,redirect,url_for,session
import models,posts_db
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
        models.add(username,email,pwd)
        # make him a file for his posts with the name of his id
        data = models.select_by(username,pwd)
        id_ = data[0]
        mkdir(path.join(ROOT,"static","images","media",str(id_)))
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
        return render_template("profile.html", username=session.get("user")[1].capitalize(), posts=posts)
    return render_template("login.html")


@app.route("/ideas")
def ideas():
    if session.get("user"):
        id_ = session.get("user")[0]
        posts = posts_db.get_by(id_)
        return render_template("ideas.html", username=session.get("user")[1].capitalize(), posts=posts)
    return render_template("login.html")


@app.route("/post",methods=["POST"])
def post():
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











