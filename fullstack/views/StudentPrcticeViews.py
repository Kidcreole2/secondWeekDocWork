from flask import request, render_template, redirect, url_for, flash, get_flashed_messages, jsonify
from flask_login import logout_user, current_user, login_required
from core import app, login_manager
from datetime import datetime as date
from models import *
from file_manager import allowed_file, save_file


@app.route("/studentPractice/<role>")
@login_required
def studentPractice_index(role):
    match role:
        case "student":
            student = Student.query.filter_by(user_id=current_user.id).first()
            print(student)
            student_practice = Student_Practice.query.filter_by(student_id=student.user_id  ).all()
            print(student)
            return render_template("pages/studentPactice/student.html", student_practices=student_practice)
        case "supervisor":
            roles = current_user.roles.split()
            if "director" in roles:
                director_practice_organization = Director_Practice_Organization.query.filter_by(user_id=current_user.id).first()
                student_practice_dpo = Student_Practice.query.filter_by(director_practice_organization_id=director_practice_organization.id).all()
            if "director" in roles:
                director_practice_usu = Director_Practice_USU.query.filter_by(user_id=current_user.id).first()
                student_practice_dpu = Practice.query.filter_by(director_practice_usu_id=director_practice_usu.id).all()
            if "director" in roles:
                director_practice_company = Director_Practice_Company.query.filter_by(user_id=current_user.id).first()
                student_practice_dpc = Practice.query.filter_by(director_practice_company_id=director_practice_company.id).all()
            student_practice = set(student_practice_dpo,student_practice_dpu,student_practice_dpc)
            return render_template("pages/studentPractice/supervisor.html", student_practice=student_practice)
    
@app.route("/studentPractice/update/<practice_id>")
@login_required
def studentPractice_update(practice_id): 
    if request.method == "POST":
        old_student_practice = Student_Practice.query.filter_by(id=practice_id).first()
        new_student_practice = Student_Practice(
            place_city=request.form['place_city'],
            place_address=request.form['place_address'],
            place_name=request.form['place_name'],
            place_name_short=request.form['place_name_short'],
            passed=request.form['passed'],
            overcoming_difficulties=request.form['overcoming_difficulties'],
            demonstrated_qualities=request.form['demonstrated_qualities'],
            work_volume=request.form['work_volume'],
            reason=request.form['reason'],
            remarks=request.form['remarks']
        )
        Student.update(old_student_practice,new_student_practice)
        return redirect(url_for(f"opop_practice_index/{practice_id}"))
    
    
@app.route("/studentPractice/update/<practice_id>/task/create")
@login_required
def studentPractice_update(practice_id): 
    if request.method == "POST":
        new_Task = Task(
        name=request.form['name'],
        date=request.form['date'],
        student_practice_id=practice_id
        )
        Student.create(new_Task)
        return redirect(url_for(f"opop_practice_index/{practice_id}"))
@app.route("/studentPractice/update/<practice_id>/task/<action>/<task_id>")
@login_required
def studentPractice_update(practice_id,action,task_id): 
    match action:
        case "update":
            if request.method == "POST":
                old_task = Task.query.filter_by(id=task_id).first()
                new_Task = Task(
                name=request.form['name'],
                date=request.form['date'],
                student_practice_id=practice_id
                )
                Student.update(old_task, new_Task)
                return redirect(url_for(f"opop_practice_index/{practice_id}"))
        case "delete":
            return "Fuck you"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    