import docxtpl
import os
from flask_login import current_user
from models import *
import pymorphy2
import io

class StudentDocument:
    
    def __init__(self, practice):
        self.__document = docxtpl.DocxTemplate("./templates/student_template.docx")
        self.__base_path = "output/"
        self.__file = io.BytesIO()
        self.__practice = practice
    
    def __get_full_name_with_initials(self, full_name:list)->str :
        return f"{full_name[0]} {full_name[1][0]}. {full_name[2][0]}."

    def __get_case_fullname(self, fullname:list, case:str)->str:
        morph = pymorphy2.MorphAnalyzer()
        lastname = morph.parse(fullname[0])[0].inflect({case}).word
        firstname = morph.parse(fullname[1])[0].inflect({case}).word
        if fullname[2] != " ":
            surname = morph.parse(fullname[2])[0].inflect({case}).word
        else:
            surname = "  "
        return f"{lastname[0].upper()+lastname[1:]} {firstname[0].upper() + firstname[1:]} {surname[0] + surname[1:]}"
    
    def __collect_student_data(self):
        name = [current_user.lastname, current_user.firstname, current_user.surname]
        group_id = Student.query.filter_by(user_id=current_user.id).first().group_id
        group = Group.query.filter_by(id=group_id).first()
        spec = Specialization.query.filter_by(id=group.specialization_id).first()
        institute = Institute.query.filter_by(id=spec.institute_id).first().name
        
        student_data = {
            "name": " ".join(name),
            "name_dp": self.__get_case_fullname(name, "datv"),
            "name_rp": self.__get_case_fullname(name, "gent"),
            "name_short": self.__get_full_name_with_initials(name),
            "group": group.name,
            "course": group.course,
            "specialisation": spec.name,
            "institute": institute
        }

        return student_data

    def __collect_tasks_data(self, student_practice):
        tasks = Task.query.filter_by(student_practice_id=student_practice.id).all()
        data_tasks = []
        id_task = 1
        for task in tasks:
            data_task = {
                "id": id_task,
                "date": task.date.srtftime("%d.%m.%Y"),
                "name": task.name,
            }
            id_task += 1
            data_tasks.append(data_task)

        return data_tasks

    def __collect_practice_data(self, student_practice):
        months = {
            1: "января",
            2: "февраля",
            3: "марта",
            4: "апреля",
            5: "мая",
            6: "июня",
            7: "июля",
            8: "августа",
            9: "сентября", 
            10: "октября",
            11: "ноября",
            12: "декабря"
        }
        practice = Practice\
            .query\
                .filter_by(id=student_practice.practice_id)\
                    .first()

        director_practice_usu = Director_Practice_USU\
            .query\
                .filter_by(user_id=practice.director_practice_usu_id)\
                    .first()
        director_practice_usu_user = Users\
            .query\
                .filter_by(id=director_practice_usu.user_id)\
                    .first()
        
        director_practice_company = Director_Practice_Company\
            .query\
                .filter_by(user_id=practice.director_practice_company_id)\
                    .first()
        director_practice_company_user = Users\
            .query\
                .filter_by(id=director_practice_company.user_id)\
                    .first()
        
        director_practice_organisation = Director_Practice_Organization\
            .query\
                .filter_by(user_id=student_practice.director_practice_organization_id)\
                    .first()
        director_practice_organisation_user = Users\
            .query\
                .filter_by(id=director_practice_organisation.user_id)\
                    .first()
        
        practice_data = {
            "kind": self.__get_practice_kind(practice.kind_of_practice),
            "type": self.__get_practice_type(practice.type_of_practice),
            "start": {
                "date":  practice.start_date.strftime("%d.%m.%Y"),
                "day":   practice.start_date.day,
                "month": months[practice.start_date.month],
                "year":  practice.start_date.year
            },
            "end": {
                "date":  practice.end_date.strftime("%d.%m.%Y"),
                "day":   practice.end_date.day,
                "month": months[practice.end_date.month],
                "year":  practice.end_date.year
            },
            "place": {
                "name": student_practice.place_name,
                "address": student_practice.place_address
            },
            "directors": {
                "usu": {
                    "short_name": self.__get_full_name_with_initials([director_practice_usu_user.lastname,
                                                                     director_practice_usu_user.firstname, 
                                                                     director_practice_usu_user.surname]
                                                                     ),
                    "post": director_practice_usu.post,
                },
                "company": {
                    "short_name": self.__get_full_name_with_initials([director_practice_company_user.lastname,
                                                                     director_practice_company_user.firstname, 
                                                                     director_practice_company_user.surname]
                                                                     ),
                    "post": director_practice_company.post,
                },
                "organisation": {
                    "short_name": self.__get_full_name_with_initials([director_practice_organisation_user.lastname,
                                                                     director_practice_organisation_user.firstname, 
                                                                     director_practice_organisation_user.surname]
                                                                     ),
                    "post": director_practice_organisation.post,
                },
            },
            "qualities": student_practice.demonstrated_qualities,
            "difficulties": student_practice.overcoming_difficulties,
            "work_volume": student_practice.work_volume,
            "remarks": student_practice.remarks,
            "rating": student_practice.grade,
            "year": practice.start_date.year
        }
        return practice_data

    def __get_practice_kind(self, practice_kind):
        match practice_kind:
            case "учебная":
                d = {
                    "name": "учебная",
                    "name_Up": "Учебная",
                    "name_dp": "учебной",
                    "name_dp_UP": "УЧЕБНОЙ"
                }
                return d
            case "производственная":
                d = {
                    "name": "производственная",
                    "name_Up": "Производственная",
                    "name_dp": "производственной",
                    "name_dp_UP": "ПРОИЗВОДСТВЕННОЙ"
                }
                return d

    def __get_practice_type(self, practice_type):
        match practice_type:
            case "ознакомительная":
                return "ознакомительной"
            case "научно-исследовательская":
                return "научно-исследовательской"
            case "производственная":
                return "производственной"
            case "технологическая":
                return "технологической"
            case "преддипломная":
                return "преддипломной"


    def __collect_data(self):
        student_data = self.__collect_student_data()
        print(self.__practice.id)
        practice = Student_Practice.query.filter_by(id=current_user.id, practice_id=self.__practice.id).first()
        tasks = self.__collect_tasks_data(practice)
        practice_data = self.__collect_practice_data(practice)
        data = {
            "student": student_data,
            "tasks": tasks,
            "practice": practice_data
        }

        return data
    
    def generate_document(self):
        table = self.__collect_data()
        self.__document.render(table)
        self.__document.save(self.__file)
        self.__file.seek(0)
        
    def get_document(self):
        self.generate_document()
