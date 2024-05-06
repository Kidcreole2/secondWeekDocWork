from flask import request, redirect, render_template
from flask_login import login_required
from models import *

def init_admin_views():
    # TODO Переделать
    @app.before_request
    def create_admin():
        print("admin")
        Users.create(Users(login="admin", password="admin", firstname="Admin", lastname="Adminov", surname="Adminovich", role="admin"))
    
    @app.route("/admin")
    @login_required
    def admin_index():
        users = Users.query.all()
        institutes = Institute.query.all()
        return render_template("pages/admin/index.html", users=users, institutes=institutes)

    @app.route("/admin/<entity>/create", methods=["GET", "POST"])
    @login_required
    def admin_entity_create(entity):
        if request.method == "POST":
            match entity:
                case "user":
                    name = request.form["fio"].split(" ")
                    form = request.form.to_dict()
                    role = " ".join([key for key in form.keys() if form[key] == "on"])
                    
                    print(role)
                    user = Users(lastname=name[0], firstname=name[1], surname=name[2], \
                        login=request.form["login"], password=request.form["password"],\
                            role=role)
                    Users.create(user)
                    
                case "institute":
                    # create_institute()
                    print("institute")

            return redirect("/admin")

        match entity:
            case "user":
                return render_template("pages/admin/user/create.html")
            case "institute":    
                return render_template("pages/admin/institute/create.html")

    @app.route("/admin/<entity>/<action>/<entity_id>", methods=["POST", "GET"])
    @login_required
    def admin_entity_action(entity, action, entity_id):
        if request.method == "POST":
            match entity:
                case "user":
                    match action:
                        case "delete" :
                            print("deleted")
                            # Users.delete(entity_id)
                        case "edit":
                            print("edit")
                            # edit_user()
                case "institute":
                    match action:
                        case "delete" :
                            print("deleted")
                            # Institute.delete(entity_id)
                        case "edit":
                            print("edit")
                            # edit_institute()
    
        match entity:
            case "user":
                match action:
                    case "edit":
                        user = Users.query.filter_by(id=entity_id).first()
                        return render_template("pages/admin/user/edit.html", old_user=user)
            case "institute":
                match action:
                    case "edit":
                        return render_template("pages/admin/institute/edit.html")
