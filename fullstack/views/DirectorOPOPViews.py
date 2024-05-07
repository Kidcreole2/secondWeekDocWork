from flask import request, render_template, redirect, url_for, jsonify
from flask_login import current_user
from core import app 
from datetime import datetime as date
from models import *

def init_opop_views():
    
# ==OPOP Index==

    @app.route("/opop")
    # @login_required
    def opop_index():
        # Create list of group and practices
        groups = []
        practices = []
        specializations = Specialization.query.filter_by(director_opop_id = current_user.id).all()
        for specialization in specializations:
            groups = groups.append(Group.query.filter_by(specialization_id = specialization.id).all())
        for group in groups:
            practices = practices.append(Practice_Group.query.filter_by(group_id=group.id).all())
        return render_template("pages/opop/index.html", groups=groups,practices=practices)

    @app.route("/opop/practice_name/check", method=["POST"])
    def practice_name_check():
        if Practice.query.filter_by(name=request.form["name"]).first() is not None:
            return jsonify({"error": "Практика с таким именем существует"}), 400
        else:
            return jsonify({"error": ""}), 200

# ==OPOP group,practice create==

    @app.route("/opop/<entity>/create", methods=["GET", "POST"])
    # @login_required
    def opop_entity_create(entity):
        match entity:
            case "group":
                opop_director = Director_OPOP.query.filter_by(user_id=current_user.id).first()
                spezializations = Specialization.query.filter_by(opop_director_id=opop_director.id).all()
                
                if request.method == "POST":
                    new_group = Group(
                    name=request.form['name'],
                    specialization_id=request.form['specialization_id'],
                    course=request.form['course'],
                    form=request.form['form']
                    )
                    Group.create(new_group)
                    return redirect("/opop")
                
                return render_template("pages/opop/group/create.html", spezializations=spezializations)
            
            case "practice":
                if request.method == "POST":
                    new_practice = Practice(
                        name=request.form['name'],
                        start_date=date.strptime(request.form['start_date'], "%Y-%m-%d"),
                        end_date=date.strptime(request.form['end_date'], "%Y-%m-%d"),
                        type_of_practice=request.form['type_of_practice'],
                        kind_of_practice=request.form['kind_of_practice'],
                        order=request.form['order'],
                        recomendations=request.form['recomendations'],
                        started=False
                    )
                    print(request.form)
                    practice_id = Practice.create(new_practice)
                    groups = request.form["groups"].split()
                    for group in groups:
                        group_id = int(group)
                        practice_group = Practice_Group(
                            practice_id=practice_id,
                            group_id=group_id
                        )
                        Practice_Group.create(practice_group)
                    
                    return jsonify({"message": "Практика была успешно создана"})
        
                groups = Group.query.order_by(Group.name).all()
                directors_practice_usu = Director_Practice_USU.query.all()
                directors_practice_company = Director_Practice_Company.query.all()
                return render_template("pages/opop/practice/create.html",groups=groups,directors_practice_usu=directors_practice_usu,directors_practice_company=directors_practice_company)

# ==OPOP group,practice update,delete==

    @app.route("/opop/<entity>/<action>/<entity_id>", methods=["GET", "POST"])
    # @login_required
    def opop_entity_action(entity,action,entity_id):
        match entity:
            case"group":
                match action:
                    case "update":
                        old_group = Group.query.filter_by(id=entity_id).first()
                        if request.method == "POST":
                            new_group = Group(
                                name=request.form['name'],
                                specialization_id=request.form['specialization_id'],
                                course=request.form['course'],
                                form=request.form['form']
                            )
                            Group.update(old_group,new_group)
                            return redirect(url_for("opop_index"))
                        student_users = Student.query.order_by(Student.id).all()
                        return render_template("pages/opop/group/update.html", student_users=student_users,group=old_group)
                    case "delete":
                        Group.delete(id_group=entity_id)
                    
            case"practice":
                match action:
                    case "update":
                        if request.method == "POST":
                            old_practice = Practice.query.filter_by(id=entity_id).first()
                            new_practice = Practice(
                                name=request.form['name'],
                                start_date=date.strptime(request.form['start_date'], "%Y-%m-%d"),
                                end_date=date.strptime(request.form['end_date'], "%Y-%m-%d"),
                                type_of_practice=request.form['type_of_practice'],
                                kind_of_practice=request.form['kind_of_practice'],
                                order=request.form['order'],
                                recomendations=request.form['recomendations'],
                                started=False
                            )
                            Practice.update(old_practice,new_practice)
                            data = request.form.to_dict()
                            data_keys = data.keys()
                            for checkbox in data_keys:
                                if "check_" in checkbox and request.form[checkbox]:
                                    practice_id = Practice.create(new_practice)
                                    group_id = int(checkbox.split("_")[1])
                                    new_practice_group = Practice_Group(
                                        practice_id=practice_id,
                                        group_id=group_id
                                    )
                                    Practice_Group.create(new_practice_group)
                            return redirect(url_for(request.url))
                        return render_template("pages/opop/practice/update.html", practice_id=practice_id)
                    case "delete":
                        Practice.delete(id_practice=entity_id)
                
# ==OPOP student create==

    @app.route("/opop/group/update/<entity_id>/create", methods=["GET", "POST"])
    # @login_required
    def opop_student_create(entity_id):
        if request.method == "POST":
            new_student_user = Users(
                login=Users.login_generation(), 
                password=Users.password_generation(), 
                firstname=request.form['firstname'], 
                lastname=request.form['lastname'], 
                surname=request.form['surname'], 
                role="student"
            )
            user_id = Users.create(new_student_user)
            new_student = Student(
                group_id=entity_id,
                user_id=user_id["id"]
            )
            Student.create(new_student)
            return redirect(url_for("opop_index"))
        return render_template("pages/opop/group/student/create.html")

# ==OPOP student update,delete==
   
    @app.route("/opop/group/update/<entity_id>/<action>/<student_user_id>", methods=["GET", "POST"])
    # @login_required
    def opop_student_action(action,entity_id,student_user_id):
        match action:
            case "update":
                if request.method == "POST":
                    new_group = Group.query.filter_by(name=entity_id).first()
                    old_student_user = Users.query.filter_by(id=student_user_id).first()
                    old_student = Student.query.filter_by(user_id=student_user_id).first()
                    new_student_user = Users(
                        login=request.form['login'], 
                        password=request.form['password'], 
                        firstname=request.form['firstname'], 
                        lastname=request.form['lastname'], 
                        surname=request.form['surname'], 
                        role=request.form["role"]
                    )
                    Users.update(old_student_user,new_student_user)
                    new_student = Student(
                        group_id=new_group.id,
                        user_id=student_user_id
                    )
                    Student.update(old_student,new_student)
                    return redirect(url_for("opop_index"))
                return render_template("pages/opop/group/student/update.html")
            case "delete":
                return "Fuck you"