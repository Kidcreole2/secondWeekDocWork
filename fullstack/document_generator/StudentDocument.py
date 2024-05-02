import docxtpl
from flask_login import current_user
from models import *

class StudentDocument:
    
    def __init__(self, name):
        self.__document = docxtpl.DocxTemplate("./templates/student_template.docx")
    


    def __get_full_name_with_initials(full_name:list):
        return f"{full_name[0]} {full_name[1][0]}. {full_name[2][0]}."

    def __collect_student_data(self):
        name = [current_user.lastname, current_user.firstname, current_user.surname]
        group_id = Student.query.filter_by(user_id=current_user.id).first().group_id
        group = Group.query.filter_by(id=group_id).first()
        spec = Specialization.query.filter_by(id=group.specialization_id).first()
        institute = Institute.query.filter_by(id=spec.institute_id).first().name
        
        student_data = {
            "name": " ".join(name),
            "name_rp": current_user.name_rp,
            "name_short": self.__get_full_name_with_initials(name),
            "group_name": group.name,
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
                .filter_by(id=practice.directior_practice_usu_id)\
                    .first()
        director_practice_usu_user = Users\
            .query\
                .filter_by(id=director_practice_usu.user_id)\
                    .first()
        
        director_practice_company = Director_Practice_Company\
            .query\
                .filter_by(id=practice.directior_practice_company_id)\
                    .first()
        director_practice_company_user = Users\
            .query\
                .filter_by(id=director_practice_company.user_id)\
                    .first()
        
        director_practice_organisation = Director_Practice_Organization\
            .query\
                .filter_by(id=student_practice.directior_practice_organization_id)\
                    .first()
        director_practice_organisation_user = Users\
            .query\
                .filter_by(id=director_practice_organisation.user_id)\
                    .first()
        
        practice_data = {
            "practice_kind": self.__get_practice_kind(practice.kind_of_practice),
            "practice_type": self.__get_practice_type(practice.type_of_practice),
            "practice_start": {
                "date":  practice.start_date.strftime("%d.%m.%Y"),
                "day":   practice.start_date.day,
                "month": months[practice.start_date.month],
                "year":  practice.start_date.year
            },
            "practice_end": {
                "date":  practice.end_date.strftime("%d.%m.%Y"),
                "day":   practice.end_date.day,
                "month": months[practice.end_date.month],
                "year":  practice.end_date.year
            },
            "practice_place": {
                "name": practice.place_name,
                "address": practice.place_address
            },
            "directors": {
                "usu": {
                    "short_name": self.__get_full_name_with_initials(director_practice_usu_user.lastname, 
                                                                     director_practice_usu_user.firstname, 
                                                                     director_practice_usu_user.surname
                                                                     ),
                    "post": director_practice_usu.post,
                },
                "company": {
                    "short_name": self.__get_full_name_with_initials(director_practice_company_user.lastname, 
                                                                     director_practice_company_user.firstname, 
                                                                     director_practice_company_user.surname
                                                                     ),
                    "post": director_practice_company.post,
                },
                "organisation": {
                    "short_name": self.__get_full_name_with_initials(director_practice_organisation_user.lastname, 
                                                                     director_practice_organisation_user.firstname, 
                                                                     director_practice_organisation_user.surname
                                                                     ),
                    "post": director_practice_organisation.post,
                },
            },
            "qualities": student_practice.demonstrated_qualities,
            "difficulties": student_practice.overcoming_difficulties,
            "work_volume": student_practice.work_volume,
            "remarks": student_practice.remarks,
            "rating": student_practice.rating,
            "year": practice.start_date.year
        }        

    def __get_practice_kind(practice_kind):
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

    def __get_practice_type(practice_type):
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
        datas = []
        student_data = self.__collect_student_data()
        practices = Student_Practice.query.filter_by(id=current_user.id).all()
        for practice in practices:
            tasks = self.__collect_tasks_data(practice)
            practice_data = self.__collect_practice_data(practice)
            data = {
                "student": student_data,
                "tasks": tasks,
                "practice": practice_data
            }
            datas.append(data)
            
        return datas
    
    def generateDocument(self):
        table_contents = self.__getTableData()
        self.__document.render(table_contents)
        self.__document.save("output/test.docx")

    
