import docxtpl
import pandas as pd

class GroupDocument:
    
    def __init__(self, name):
        self.__name = name
        self.__document = docxtpl.DocxTemplate("./templates/group_template.docx")
    
    def __get_full_name_with_initials(full_name):
        split_name = full_name.split(" ")
        return f"{split_name[0]} {split_name[1][0]}. {split_name[2][0]}."
    
    def __get_success_students(self):
        df = pd.read_csv("./test-students-data/1121b_students_success.csv")
        return df.to_dict(orient="records")
    
    def __get_fail_students(self):
        df = pd.read_csv("./test-students-data/1121b_students_fail.csv")
        return df.to_dict(orient="records")

    def __get_table_data(self):
        success_students = self.__get_success_students()
        fail_students = self.__get_fail_students()
        contents = {
            "group": "1121б",
            "program_code": "09.08.01",
            "program": "Информатика и вычислительная техника",
            "institute": "Инженерная школа цифровых технологий",

            "practice_start": "22.04.2024", 
            "practice_end": "26.04.2024", 
            "practice_type": "ознакомительной",
            "practice_type_ip": "ознакомительная",
            "practice_kind": "учебной",
            "practice_kind_ip": "учебная",
            "practice_address": "г. Ханты-Мансийск, ул. Чехова, 16",
            
            "students_number_success": len(success_students),
            "students_success": success_students,
            "students_number_fail": len(fail_students[:5]),
            "students_fail": fail_students[:5],
            
            "usu_manager": "Пидор Грязный",
            "opop_manager": "Самарин В.А.",
            
            "recommendation": "нет",
            "report_number": "2-222",
            "report_date": "06.03.2024",
            "course": 2,
            "year": 2024,
        }

        return contents

    def generateDocument(self):
        table_contents = self.__get_table_data()
        self.__document.render(table_contents)
        self.__document.save("output/test.docx")
