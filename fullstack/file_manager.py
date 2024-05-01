from werkzeug.utils import secure_filename
import os
from core import app
import pandas as pd

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'ods'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def file_type(filename):
    return filename.rsplit('.')[-1].lower()

def allowed_file(filename)-> bool:
    return '.' in filename and file_type(filename) in ALLOWED_EXTENSIONS

def save_file(file, data_type):
    num = len(os.listdir(app.config['UPLOAD_FOLDER']))
    ft = file_type(file.filename)
    file.filename = data_type + "_" + str(num) + "." + ft
    datafilename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], datafilename))
    match ft:
        case "csv":
            data = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], datafilename))
        case "xlsx" | "xls" | "ods":
            data = pd.read_exel(os.path.join(app.config['UPLOAD_FOLDER'], datafilename))
    d = data.loc[:, ["opop_name", "opop_post"]].to_dict(orient="records")
    opop_names_set = set()
    for i in d:
        opop_names_set.add(tuple(i.items()))
    print(opop_names_set)
    opops = []
    for opop_name in opop_names_set:
        opop = {
            "name": opop_name[0][1].split(" "),
            "login": "Samarin",
            "password": 123,
            "role": "opop",
            "post": opop_name[1][1]
        }
        opops.append(opop)

    print(opops)


def remove_cached_files():
    for file_path in os.listdir(app.config["UPLOAD_FOLDER"]):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER']), file_path)