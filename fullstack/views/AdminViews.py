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
    def user_login_check():
        user_by_id = Users.query.filter_by(id=request.form["id"]).first().id
        user_by_login = Users.query.filter_by(login=request.form["login"]).first()
        
        if (user_by_login is None) or (user_by_id == user_by_login.id):
            return jsonify({"success": "everything ok"}), 200
        else:
            return jsonify({"success": "u're stupid donkey", "error": "Пользователь с таким логином существует"}), 400
    
    @app.route("/admin/institute/name_check", methods=["POST"])
    @login_required
    def institute_name_check():
        institute_by_id = Institute.query.filter_by(id=request.form["id"]).first().id
        institute_by_name = Institute.query.filter_by(name=request.form["name"]).first()
        if institute_by_name == None or institute_by_name.id == institute_by_id:
            return jsonify({"message": "zaebis"}), 200
        
        return jsonify({"message": "Институт с таким названием уже существует"}), 400
     
    @app.route("/admin/specialization/name_check", methods=["POST"])
    @login_required
    def spec_name_check():
        institute_by_id = Specialization.query.filter_by(id=request.form["id"]).first().id
        institute_by_name = Specialization.query.filter_by(name=request.form["name"]).first()
        if institute_by_name == None or institute_by_name.id == institute_by_id:
            return jsonify({"message": "zaebis"}), 200
        
        return jsonify({"message": "Институт с таким названием уже существует"}), 400
   
    
    @app.route("/admin")
    @login_required
    def admin_index():
        users = Users.query.all()
        institutes = Institute.query.all()
        specializations = Specialization.query.all()
        return render_template("pages/admin/index.html", users=users, institutes=institutes, specializations=specializations)

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
                                
                    print(data)
                    if data["role"] == "":
                        return jsonify({"message": data["message"]}), 400
                    
                    print(data["id"])
                    
                    roles = request.form["role"].split()
                    
                    print(roles)
                    
                    for role in roles:
                        match role:
                            case "director-opop":
                                Director_OPOP.create(Director_OPOP(user_id=data["id"], post="DOCENT"))
                                print("opop good")
                            case "director-organization":
                                Director_Practice_Organization.create(Director_Practice_Organization(user_id=data["id"], post="DOCENT"))
                                print("org good")
                            case "director-company":
                                Director_Practice_Company.create(Director_Practice_Company(user_id=data["id"], post="DOCENT"))
                                print("comp good")
                            case "director-usu":
                                Director_Practice_USU.create(Director_Practice_USU(user_id=data["id"], post="DOCENT"))
                                print("usu good")
                                
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
                    Specialization.create(Specialization(
                        name=request.form['name'],
                        specialization_code=request.form['code'],
                        director_opop_id=int(request.form['opop_id']),
                        institute_id=int(request.form['id'])
                    ))
                    return jsonify({"message": "123"}), 200
                opop_directors = Director_OPOP.query.all()
                institutes = Institute.query.all()
                opop_directors_user = []
                for opop_director in opop_directors:
                    user = Users.query.filter_by(id=opop_director.user_id).first()
                    opop_directors_user.append(user)
                return render_template("pages/admin/institute/specialization/create.html",opop_directors=opop_directors,opop_directors_user=opop_directors_user, institutes=institutes)


    @app.route("/admin/<entity>/<action>/<entity_id>", methods=["POST", "GET"])
    @login_required
    def admin_entity_action(entity, action, entity_id):
            match entity:
                case "user":
                    match action:
                        case "delete" :
                            Users.delete(user_id=entity_id)
                            return jsonify({"message": "Pidor"}), 200
                        
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
                            return jsonify({"message": "Pidor"}), 200
                        
                        case "edit":
                            old_institute = Institute.query.filter_by(id=entity_id).first()
                            
                            if request.method == "POST":
                                print("edit")
                                name = request.form["name"]
                                new_institute = Institute(name=name)
                                Institute.update(old_institute=old_institute, new_institute=new_institute)
                                return jsonify({"message": "Данные успешно обновлены"}), 200

                                
                            current_specs = Specialization.query.filter_by(institute_id=old_institute.id).all()
                            return render_template("pages/admin/institute/update.html", institute=old_institute, current_specializations=current_specs)
                        
                case "specialization":
                    match action:
                        case "delete" :
                            Specialization.delete(entity_id)
                            return jsonify({"message": "Pidor"}), 200
                        
                        case "edit":
                            old_spec = Specialization.query.filter_by(id=entity_id).first()
                            
                            if request.method == "POST":
                                name = request.form["name"]
                                code = request.form["code"]
                                institute_id = int(request.form["institute_id"])
                                opop_id = int(request.form['opop_id'])
                                
                                new_spec = Specialization(name=name, specialization_code=code, institute_id=institute_id, director_opop_id=opop_id)
                                Specialization.update(old_specialization=old_spec, new_specialization=new_spec)
                                
                                return jsonify({"message": "Специализация успешно обновлена"}), 200
                            
                            opop_directors = Director_OPOP.query.all()
                            institutes = Institute.query.all()
                            opop_directors_user = []
                            for opop_director in opop_directors:
                                user = Users.query.filter_by(id=opop_director.user_id).first()
                                opop_directors_user.append(user)
                            return render_template("pages/admin/institute/specialization/update.html", old_spec=old_spec, opop_directors=opop_directors,opop_directors_user=opop_directors_user, institutes=institutes)
