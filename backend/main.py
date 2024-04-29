from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
# from HTMLLogger import HTMLLogger

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"

db = SQLAlchemy()

login_manager  = LoginManager()
login_manager.init_app(app)
# logger=HTMLLogger(name="Test App", html_filename="log.html", console_log=True)



db.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route('/register', methods=["GET","POST"])
def register():
    # logger.info('reg page')
    if request.method == "POST":
        # logger.info('reg begins')
        user = Users(username=request.form.get("floatingLogin"),
                     password=request.form.get("floatingPassword"),
                     permission=request.form.get("floatingName"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("sign_up.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    print("pizda33")
    if request.method == "POST":
    # logger.info('log begin')
        print("pizda2")
        user = Users.query.filter_by(
            username=request.form.get("floatingInput")).first()
        if user.password == request.form.get("floatingPassword"):
            login_user(user)
            match user.permission:
                case "123":
                    return render_template("pages/admin.html")
                    # return redirect(url_for("register"))
                case "opop_supervisor":
                    return render_template("pages/opop_supervisor.html")
                    # return redirect(url_for("register"))
                case "piractice_supervisor":
                    return render_template("pages/piractice_supervisor.html")
                    # return redirect(url_for("register"))
            return redirect(url_for("register"))
    print("pizda")
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/", methods=["GET","POST"])
def home():
    print("pizda1")
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=True)