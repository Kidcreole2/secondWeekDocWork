import docxtpl

class StudentDocument:
    
    def __init__(self, name):
        self.__name = name
        self.__document = docxtpl.DocxTemplate("./templates/student_template.docx")
    
    def __get_full_name_with_initials(full_name):
        split_name = full_name.split(" ")
        return f"{split_name[0]} {split_name[1][0]}. {split_name[2][0]}."

    def __get_table_data(self):
        contents = {
            "student_name": "Сирченко Михаил Сергеевич",
            "student_name_rp": "Сирченко Михаила Сергеевичa",
            "student_name_short": self.__get_full_name_with_initials("Сирченко Михаил Сергеевич"),
            "student_group": "1121б",
            "student_course": 2,
            "student_program": "Информатика и вычислительная техника",
            "student_institute": "Инженерная школа цифровых технологий",
            "tasks":[
                {"id":1, "date": "08.03.2023", "task_name": "Встреча с клиентом"},
                {"id":2, "date": "09.03.2023", "task_name": "Написать отчет о продажах"},
                {"id":3, "date": "10.03.2023", "task_name": "Провести мозговой штурм по новой продуктовой линейке"},
                {"id":4, "date": "13.03.2023", "task_name": "Подготовить презентацию для инвесторов"},
                {"id":5, "date": "14.03.2023", "task_name": "Проанализировать данные о конкурентах"},
                {"id":6, "date": "15.03.2023", "task_name": "Запустить новую маркетинговую кампанию"},
                {"id":7, "date": "16.03.2023", "task_name": "Провести интервью с потенциальными сотрудниками"},
                {"id":8, "date": "17.03.2023", "task_name": "Организовать мероприятие по тимбилдингу"},
                {"id":9, "date": "20.03.2023", "task_name": "Опубликовать обновление программного обеспечения"},
                {"id":10, "date": "21.03.2023", "task_name": "Создать учебные материалы для новых сотрудников"}            
            ],

            "practice_place": "Югорский государственный университет",
            "practice_start": "22.04.2024", 
            "practice_start_day": "22",
            "practice_start_month": "апреля",
            "practice_start_year": "2024",
            "practice_end": "26.04.2024", 
            "practice_end_day": "26", 
            "practice_end_month": "апреля", 
            "practice_end_year": "2024", 
            "practice_type": "ознакомительной",
            "practice_kind": "учебная",
            "practice_kind_up": "Учебная",
            "practice_kind_dp": "учебной",
            "practice_kind_dp_up": "УЧЕБНОЙ",
            "practice_address": "г. Ханты-Мансийск, ул. Чехова, 16",
            
            "usu_manager": "Змеев Д.О.",
            "usu_manager_post": "Доцент",
            "usu_manager_post_short": "Доц.",
            "company_manager": "Самарина О.В.",
            "company_manager_post_short": "Доц.",
            "company_manager_post": "Доцент",

            "year": 2024,
            "graduate": 5,
        }

        return contents

    def generateDocument(self):
        table_contents = self.__getTableData()
        self.__document.render(table_contents)
        self.__document.save("output/test.docx")

    
