from flask import request, render_template, redirect, url_for, flash, get_flashed_messages, jsonify
from flask_login import logout_user, current_user, login_required
from core import app, login_manager
from datetime import datetime as date
from models import *
from file_manager import allowed_file, save_file

def init_studentPractice_views():
    @app.route("/studentPractice/<role>")
    @login_required
    def studentPractice_index(role):
        match role:
            case "student":
                print("student")
                student_practice = Student_Practice.query.filter_by(student_id=current_user.id).all()
                return render_template("pages/studentPractice/index.html", student_practices=student_practice)
            case "supervisor":
                print("supervisor")
                roles = current_user.role.split()
                student_practice_dpc = []
                student_practices = []
                if "director-company" in roles:
                    practice_dpc = Practice.query.filter_by(director_practice_company_id=current_user.id).all()
                    for practice in practice_dpc:
                        student_practice_dpc.append(Student_Practice.query.filter_by(practice_id = practice.id).first())
                    print(student_practice_dpc)
                for practice in student_practice_dpc:
                    student_practices.append(practice)
                return render_template("pages/studentPractice/index.html", student_practices=student_practices)
        
    @app.route("/studentPractice/update/<practice_id>", methods=["POST", "GET"])
    @login_required
    def studentPractice_update_practice(practice_id): 
        print(current_user.role)
        if request.method == "POST":
            if "student" in current_user.role:
                old_student_practice = Student_Practice.query.filter_by(id=practice_id).first()
                print(request.form.to_dict())
                new_student_practice = Student_Practice(
                    student_id=old_student_practice.student_id,
                    practice_id=old_student_practice.practice_id,
                    director_practice_organization_id=old_student_practice.director_practice_organization_id,
                    kind_of_contract=old_student_practice.kind_of_contract,
                    paid=old_student_practice.paid,
                    place_city=request.form['place_city'],
                    place_address=request.form['place_address'],
                    place_name=request.form['place_name'],
                    place_name_short=request.form['place_name_short'],
                    passed=old_student_practice.passed,
                    overcoming_difficulties=old_student_practice.overcoming_difficulties,
                    demonstrated_qualities=old_student_practice.demonstrated_qualities,
                    work_volume=old_student_practice.work_volume,
                    reason=old_student_practice.reason,
                    remarks=old_student_practice.remarks
                )
                Student_Practice.update(old_student_practice.id,new_student_practice)
                return jsonify({ "message": "Данные успешно обновлены" }), 200
            else:
                old_student_practice = Student_Practice.query.filter_by(id=practice_id).first()
                if request.form['passed'] == "true":
                    passed_bool = True
                else:
                    passed_bool = False
                print(request.form.to_dict())
                print(passed_bool)
                new_student_practice = Student_Practice(
                    student_id=old_student_practice.student_id,
                    practice_id=old_student_practice.practice_id,
                    director_practice_organization_id=old_student_practice.director_practice_organization_id,
                    kind_of_contract=old_student_practice.kind_of_contract,
                    paid=old_student_practice.paid,
                    place_city=request.form['place_city'],
                    place_address=request.form['place_address'],
                    place_name=request.form['place_name'],
                    place_name_short=request.form['place_name_short'],
                    passed=passed_bool,
                    grade=int(request.form['grade']),
                    overcoming_difficulties=request.form['overcoming_difficulties'],
                    demonstrated_qualities=request.form['demonstrated_qualities'],
                    work_volume=request.form['work_volume'],
                    reason=request.form['reason'],
                    remarks=request.form['remarks']
                )
                Student_Practice.update(old_student_practice.id,new_student_practice)
                return jsonify({ "message": "Данные успешно обновлены" }), 200
        student_practice = Student_Practice.query.filter_by(id = practice_id).first()
        tasks = Task.query.filter_by(student_practice_id=practice_id).all()
        role = current_user.role
        if "student" in role:
            role = "student"
        else:
            role = "supervisor"
        return render_template("pages/studentPractice/practice/update.html", student_practice=student_practice, tasks=tasks,role=role)
        
    @app.route("/studentPractice/update/<practice_id>/task/create", methods=["POST", "GET"])
    # @login_required
    def studentPractice_create_task(practice_id): 
        if request.method == "POST":
            print(request.form.to_dict())
            new_Task = Task(
            name=request.form['name'],
            date=date.strptime(request.form['date'], "%Y-%m-%d"),
            student_practice_id=practice_id
            )
            Task.create(new_Task)
            return jsonify({ "message": "Данные успешно обновлены" }), 200
        student_practice = Student_Practice.query.filter_by(id = practice_id).first()
        urlForUpdate = f"update/{practice_id}"
        return render_template("pages/studentPractice/practice/tasks/create.html", student_practice=student_practice, role=urlForUpdate)

    @app.route("/studentPractice/update/<practice_id>/task/<action>/<task_id>", methods=["POST", "GET"])
    # @login_required
    def studentPractice_update_task(practice_id,action,task_id): 
        match action:
            case "update":
                if request.method == "POST":
                    old_task = Task.query.filter_by(id=task_id).first()
                    new_Task = Task(
                    name=request.form['name'],
                    date=date.strptime(request.form['date'], "%Y-%m-%d"),
                    student_practice_id=practice_id
                    )
                    Task.update(old_task, new_Task)
                    return jsonify({ "message": "Данные успешно обновлены" }), 200
                student_practice = Student_Practice.query.filter_by(id = practice_id).first()
                urlForUpdate = f"update/{practice_id}"
                task = Task.query.filter_by(student_practice_id=practice_id).all()
                return render_template("pages/studentPractice/practice/tasks/update.html", student_practice=student_practice, role=urlForUpdate, task=task)
            case "delete":
                return "Fuck you"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
