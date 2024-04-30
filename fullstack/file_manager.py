from werkzeug.utils import secure_filename
import os
from core import app

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename:str)-> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    datafilename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], datafilename))
    print(datafilename)

def remove_cached_files():
    for file_path in os.listdir(app.config["UPLOAD_FOLDER"]):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER']), file_path)