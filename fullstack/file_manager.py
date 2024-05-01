from werkzeug.utils import secure_filename
import os
from core import app
import pandas as pd
from models import load_specialisation_data

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
    
    opop_data = data.loc[:, ["opop_name", "opop_post"]].to_dict(orient="records")
    opop_names = set()
    for i in opop_data:
        opop_names.add(tuple(i.items()))
    opop_names = list(opop_names)
    print(opop_names)
    opop_names_dicts = []
    for opop_name in opop_names:
        opop_name = list(opop_name)
        d = dict()
        for key, value in opop_name:
            d.setdefault(key, []).append(value)
        opop_names_dicts.append(d)
    print(opop_names_dicts)
    opops = []

    for opop_name in opop_names_dicts:
        opop = {
            "name": opop_name["opop_name"][0].split(' '),
            "login": "Samarin",
            "password": 123,
            "role": "opop",
            "post": opop_name["opop_post"]
        }
        opops.append(opop)

    institute_data = data.loc[:, ["institute"]].to_dict("list")
    instute_names = set(institute_data["institute"])
    institutes = []
    for institute_name in instute_names:
        institute = {
            "name": institute_name
        }
        institutes.append(institute)

    specialisations_data = data.loc[:, ["opop_name","institute", "specialisation", "specialisation_code"]].to_dict("records")
    # print(specialisations_data)
    specs = set()
    
    for i in specialisations_data:
        specs.add(tuple(i.items()))
    print(specs)
    
    specis = []
    for spec in specs:
        spec = list(spec)
        d = dict()
        for key, value in spec:
            d.setdefault(key, []).append(value)
        specis.append(d)
    
    print(specis)   
    
    specialisations = []

    for spec in specis:
        specialisation = {
            "opop": spec["opop_name"][0],
            "name": spec["specialisation"][0],
            "code": spec["specialisation_code"][0],
            "institute": spec["institute"][0]
        }
        specialisations.append(specialisation)
    print(specialisations)   

    load_specialisation_data(opops, institutes, specialisations)

def remove_cached_files():
    for file_path in os.listdir(app.config["UPLOAD_FOLDER"]):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER']), file_path)