from flask import request, redirect, render_template, jsonify
from flask_login import login_required
from models import *

def init_admin_views():
    # TODO Переделать
    @app.before_request
    def create_admin():
        print("admin")
        Users.create(Users(login="admin", password="admin", firstname="Admin", lastname="Adminov", surname="Adminovich", role="admin"))
    
    @app.route("/admin/user/login_check", methods=["POST"])
    @login_required
    def login_check():
        user_by_id = Users.query.filter_by(id=request.form["id"]).first().id
        user_by_login = Users.query.filter_by(login=request.form["login"]).first()
        
        if (user_by_login is None) or (user_by_id == user_by_login.id):
            return jsonify({"success": "everything ok"}), 200
        else:
            return jsonify({"success": "u're stupid donkey", "error": "Пользователь с таким логином существует"}), 400
    
    @app.route("/admin")
    @login_required
    def admin_index():
        users = Users.query.all()
        institutes = Institute.query.all()
        return render_template("pages/admin/index.html", users=users, institutes=institutes)

    @app.route("/admin/<entity>/create", methods=["GET", "POST"])
    @login_required
    def admin_entity_create(entity):
        match entity:
            case "user":
                if request.method == "POST":
                    name = request.form["fio"].split(" ")
                
                    user = Users(lastname=name[0], firstname=name[1], surname=name[2] if len(name) == 3 else " ", \
                        login=request.form["login"], password=request.form["password"],\
                            role=request.form["role"])
                    
                    data = Users.create(user)
                    
                    if data["role"] == "":
                        return jsonify({"message": data["message"]})
                    
                    return jsonify({"message": "Пользователь был успешно создан"})
        
                return render_template("pages/admin/user/create.html")
            
            case "institute":
                if request.method == "POST":
                    name = request.form['name']
                    inst = Institute(name=name)
                    Institute.create(institute=inst)
                    return redirect("/admin")
                
                return render_template("pages/admin/institute/create.html")
            
            case "specialization":
                if request.method == "POST":
                    pass
                return render_template("pages/admin/institute/specialization/create.html")


    @app.route("/admin/<entity>/<action>/<entity_id>", methods=["POST", "GET"])
    @login_required
    def admin_entity_action(entity, action, entity_id):
            match entity:
                case "user":
                    match action:
                        case "delete" :
                            Users.delete(user_id=entity_id)
                        
                        case "edit":
                            old_user = Users.query.filter_by(id=entity_id).first()
                            
                            if request.method == "POST":
                                name = request.form["fio"].split()
                                role = request.form["role"]
                                
                                new_user = Users(
                                    login=request.form["login"],
                                    password=request.form["password"],
                                    lastname=name[0],
                                    firstname=name[1],
                                    surname= name[2] if len(name) == 3 else " ",
                                    role=role
                                    )
                                
                                Users.update(old_user_id=entity_id, new_user=new_user)
                                return jsonify({ "message": "Данные успешно обновлены" })
                            
                            return render_template("pages/admin/user/update.html", old_user=old_user)
                
                case "institute":
                    match action:
                        case "delete" :
                            Institute.delete(entity_id)
                        
                        case "edit":
                            old_institute = Institute.query.filter_by(id=entity_id).first()
                            
                            if request.method == "POST":
                                print("edit")
                                name = request.form["name"]
                                new_institute = Institute(name=name)
                                Institute.update(old_institute=old_institute, new_institute=new_institute)
                               
                            current_specs = Specialization.query.filter_by(institute_id=old_institute.id).all()
                            return render_template("pages/admin/institute/edit.html", old_institute=old_institute, current_specializations=current_specs)
                        
                case "specialization":
                    match action:
                        case "delete" :
                            Specialization.delete(entity_id)
                        
                        case "edit":
                            old_institute = Institute.query.filter_by(id=entity_id).first()
                            
                            if request.method == "POST":
                                print("edit")
                                name = request.form["name"]
                                new_institute = Institute(name=name)
                                Institute.update(old_institute=old_institute, new_institute=new_institute)
                               
                            current_specs = Specialization.query.filter_by(institute_id=old_institute.id).all()
                            return render_template("pages/admin/institute/edit.html", old_institute=old_institute, current_specializations=current_specs)