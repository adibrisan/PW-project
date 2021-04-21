from flask import Flask, redirect, url_for, render_template,request,session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os
from flask_ckeditor import *

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.secret_key="hello"
app.permanent_session_lifetime = timedelta(days=10)
app.config["SQLALCHEMY_DATABASE_URI"] ='mysql://root:''@localhost/pw'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
ckeditor = CKEditor(app)

class Data(db.Model):
    __searchable__ = ['id','name','owned','drivers','year']
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    owned = db.Column(db.String(1000))
    drivers = db.Column(db.String(1000))
    year = db.Column(db.String(1000))
    cale = db.Column(db.String(1000))
    description = db.Column(db.String(1000))

    def __init__(self,name,owned,drivers,year,cale,description):
        self.name = name
        self.owned = owned
        self.drivers = drivers
        self.year = year
        self.cale = cale
        self.description = description

@app.route("/addphoto", methods=["POST","GET"])
def addphoto():
    target = os.path.join(APP_ROOT,'static/')

    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target,filename])
        file.save(destination)
    return render_template("addphoto.html")

@app.route('/upload')
def upload():
    target = os.path.join(APP_ROOT, 'static')
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)

@app.route("/admin",methods = ["POST", "GET"])
def insert():
        if request.method == "GET":
            users = Data.query.all()
            user = Data(name='',owned='',drivers='',year='',cale='',description='')
            pagename = 'admin'
            return render_template('admin.html',pagename=pagename,users=users,user=user)
        else:
            name = request.form["name"]
            owned = request.form["owned"]
            drivers = request.form["drivers"]
            year = request.form["year"]
            description = request.form.get("ckeditor")
            upload()
            for file in request.files.getlist("file"):
                filename = file.filename
            user = Data(name=name,owned=owned,drivers=drivers,year=year,cale=filename,description=description)
            db.session.add(user)
            db.session.commit()
            flash("F1 added !")
            return redirect(url_for("admin"))

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Data.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    flash("F1 deleted !")
    return redirect(url_for("admin"))

@app.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
    user = Data.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.owned = request.form["owned"]
        user.drivers = request.form["drivers"]
        user.year = request.form["year"]
        user.description = request.form.get("ckeditor")
        upload()
        for file in request.files.getlist("file"):
            user.cale = file.filename

        db.session.commit()
        flash("F1 car updated !")
        return redirect(url_for('admin'))
    else:
        pagename = 'updateAdmin'
        users = Data.query.all()
        flash("F1 car updated !")

        return render_template('admin.html',pagename=pagename, user=user, users=users)



@app.route("/general",methods=["POST", "GET"])
def general():
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        password = request.form["password"]
        session["password"] = password
        if "admin" == username and "admin" == password:
            return render_template("general.html")
        else:
            flash("Invalid credentials !!!")
            return render_template("index.html")
    else:
        if "password" in session:
            return render_template("general.html")
    return render_template("index.html")

@app.route("/")
def home():
    if "password" in session:
        return render_template("general.html")
    else:
        return render_template("index.html")

@app.route("/news")
def collection():
    return render_template("news.html")

@app.route("/logout")
def logout():
    session.pop("password", None)
    return render_template("index.html")


@app.route("/invalid")
def invalid():
    return render_template("invalid.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/compilation")
def comp():
    return render_template("compilation.html")

@app.route("/collection")
def collect():
    all_data= Data.query.all()
    return render_template("collection.html", cars=all_data)

@app.route("/visitor")
def vis():
    return render_template("visitor.html")

@app.route("/editor")
def editor():
    return render_template("editor.html")

@app.route("/abvisitor")
def abvisitor():
    return render_template("abvisitor.html")

@app.route("/afisare/<name>", methods =['GET','POST'])
def afisare(name):
    my_data=Data.query.get(name)
    return render_template("afisare.html", mydata=my_data)

@app.route("/galleryvisitor")
def galleryvisitor():
    all_data= Data.query.all()
    return render_template("galleryvisitor.html", cars=all_data)



if __name__ == "__main__":
    app.run(debug=True)
    ckeditor.init_app(app)
