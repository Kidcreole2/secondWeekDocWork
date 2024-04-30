from flask import request, render_template, redirect, url_for
from flask_login import logout_user
from core import app, login_manager
from models import Users


@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id) 

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = Users(login=request.form['login'], 
                     password=request.form['password'], 
                     firstname=request.form['firstname'], 
                     lastname=request.form['lastname'], 
                     surname=request.form['surname'], 
                     role=request.form["role"]
                     )
        Users.register(user)
        return redirect(url_for("home"))
    
    return render_template("pages/admin/register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        print(login)
        password = request.form.get("password")
        role = Users.auth_user(login, password)
        
        match role:
            case "123":
                return render_template("pages/admin/index.html")
            case "opop_supervisor":
                return render_template("pages/opop/index.html")
            case "practice_supervisor":
                return render_template("pages/Teacher/index.html")
    
    return render_template("login.html", {role: True})

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/")
def home():
    return render_template("login.html")
