import docxtpl
import pandas as pd
from models import *
import os
import io
import datetime
from flask_login import current_user
import zipfile
import pprint

class GroupDocument:
    
    def __init__(self, practice):
        self.__practice = practice
        self.__document = docxtpl.DocxTemplate("./document_generator/templates/group_template.docx")
        self.__data_files = dict()

    def __get_full_name_with_initials(self, full_name):
        return f"{full_name[0]} {full_name[1][0]}. {full_name[2][0]}."
    
    def __get_practice_kind(self, practice_kind):
        match practice_kind:
            case "учебная":
                d = {
                    "name": "учебная",
                    "name_dp": "учебной",
                }
                return d
            case "производственная":
                d = {
                    "name": "производственная",
                    "name_dp": "производственной",
                }
                return d

    def __get_practice_type(self, practice_type):
        match practice_type:
            case "ознакомительная":
                d = {
                    "name":"ознакомительная",
                    "name_dp":"ознакомительной"
                }
                return d
            case "научно-исследовательская":
                d = {
                    "name":"научно-исследовательская",
                    "name_dp":"научно-исследовательской"
                }
                return d
            case "производственная":
                d = {
                    "name":"производственная",
                    "name_dp":"производственной"
                }
                return d
            case "технологическая":
                d = {
                    "name":"технологическая",
                    "name_dp":"технологической"
                }
                return d
            case "преддипломная":
                d = {
                    "name":"преддипломная",
                    "name_dp":"преддипломной"
                }
                return d
    
    def __collect_practice_data(self):
        usu_director_user = Users.query.filter_by(id=self.__practice.director_practice_usu_id).first()
        institute_id = Specialization.query.filter_by(director_opop_id=current_user.id).first().institute_id
        institute_name = Institute.query.filter_by(id=institute_id).first().name
        practice_data = {
            "kind": self.__get_practice_kind(self.__practice.kind_of_practice),
            "type": self.__get_practice_type(self.__practice.type_of_practice),
            "institute": institute_name,
            "year": self.__practice.start_date.year,
            "start_date": self.__practice.start_date.strftime("%d.%m.%Y"),
            "end_date": self.__practice.end_date.strftime("%d.%m.%Y"),
            "usu_name_short": self.__get_full_name_with_initials([
                usu_director_user.lastname,
                usu_director_user.firstname,
                usu_director_user.surname
            ]),
            "opop_name_short": self.__get_full_name_with_initials([
                current_user.lastname,
                current_user.firstname,
                current_user.surname
            ]),
            "order": self.__practice.order,
            "recommendation": self.__practice.recomendations
        }
        
        return practice_data
    def _collect_students_data(self, passed, group_id):
        data = Student_Practice.query.filter_by(practice_id=self.__practice.id, passed=passed).all()
        students = []
        for failed in data:
            student = Student.query \
                .filter_by(user_id=failed.student_id, group_id=group_id).first()

            student_user = Users.query.filter_by(id=student.user_id).first()
            students.append(student_user)
        return students
    def _collect_success_students_data(self, group):
        success_students = self._collect_students_data(passed=True, group_id=group.id)
        success_students_data = []
        counter = 1
        for success_student in success_students:
            practice_data = Student_Practice.query\
                .filter_by(student_id=success_student.id, practice_id=self.__practice.id).first()
            
            directior_practice_organisation = Director_Practice_Organization.query\
                .filter_by(user_id=practice_data.director_practice_organization_id).first()
            directior_practice_organisation_user = Users.query.filter_by(id=directior_practice_organisation.user_id).first()
            
            success_student_data = {
                "id": counter,
                "fullname": f"{success_student.lastname} {success_student.firstname} {success_student.surname}",
                "city":  practice_data.place_city,
                "place": practice_data.place_name_short,
                "offer": practice_data.kind_of_contract,
                "paid":  practice_data.paid,
                "director_organization": f"{directior_practice_organisation_user.lastname} {directior_practice_organisation_user.firstname[0]}. {directior_practice_organisation_user.surname[0]}."
            }
            counter += 1
            success_students_data.append(success_student_data)
        
        return success_students_data
    
    def _collect_failed_students_data(self, group):
        failed_students = self._collect_students_data(passed=False, group_id=group.id)
        failed_students_data = []
        counter = 1
        for failed_student in failed_students:
            reason = Student_Practice.query.filter_by(student_id=failed_student.id, practice_id=self.__practice.id).first().reason

            failed_student_data = {
                "id": counter,
                "fullname": f"{failed_student.lastname} {failed_student.firstname} {failed_student.surname}",
                "reason": reason
            }
            failed_students_data.append(failed_student_data)
            counter += 1
        
        return failed_students_data
     
    def _collect_group_data(self, group):
        spec = Specialization.query.filter_by(id=group.specialization_id).first()
        success = self._collect_success_students_data(group)
        failed = self._collect_failed_students_data(group)
        group_data = {
            "course": group.course,
            "name": group.name,
            "form": group.form,
            "code": spec.specialization_code,
            "spec_name": spec.name,
            "success_students_number": len(success),
            "success_students": success,
            "failed_students_number": len(failed),
            "failed_students": failed
        }
        
        return group_data
            
    def _collect_data(self):
        practice_data = self.__collect_practice_data()
        specialisations = Specialization.query.filter_by(director_opop_id=current_user.id).all()
        practice_groups = Practice_Group.query.filter_by(practice_id=self.__practice.id).all()
        groups = []
        for practice_group in practice_groups:
            group = Group.query.filter_by(id=practice_group.group_id).first()
            for specialisation in specialisations:
                if group.specialization_id == specialisation.id:
                    groups.append(group)
        document_data = []
        for group in groups:
            group_data = self._collect_group_data(group)
            data = {
                "practice": practice_data,
                "group": group_data
            }
            document_data.append(data)
        return document_data
        
    def generate_document(self):
        table_contents = self._collect_data()
        pprint.pprint(table_contents)
        for table in table_contents:
            self.__document.render(table)
            name = datetime.date.today().strftime("%d.%m.%Y.docx")
            data = io.BytesIO()
            self.__document.save(data)
            data.seek(0)
            self.__data_files[name] = data

    def get_documents(self):
        self.generate_document()
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a" , zipfile.ZIP_DEFLATED, False) as zip_file:
            for filename, data in self.__data_files.items():
                zip_file.writestr(filename, data.getvalue())
        return zip_buffer