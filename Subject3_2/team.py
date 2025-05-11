# team.py
import os
import random
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif'}
def allowed_file(fname):
    return '.' in fname and fname.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def obfuscate_text(s, n=2):
    lst  = list(s)
    idxs = [i for i,ch in enumerate(lst) if ch.isalnum()]
    for i in random.sample(idxs, min(n,len(idxs))):
        lst[i] = '*'
    return ''.join(lst)

@app.route('/intro')
def intro():
    return render_template('intro.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/input')
def input_page():
    return render_template('input.html')

@app.route('/result', methods=['POST'])
def result_page():
    files  = request.files.getlist('image[]')
    names  = request.form.getlist('name[]')
    IDs  = request.form.getlist('ID[]')
    genders = [request.form.get(f'gender_{i}') for i in range(len(names))]
    roles  = request.form.getlist('role[]')
    majors = request.form.getlist('major[]')
    phones = request.form.getlist('phonenumber[]')
    emails = request.form.getlist('emial[]')

    def mask_phone_last2(phone):
        if len(phone) <= 2:
            return '*' * len(phone)
        return phone[:-2] + '**'

    students = []
    for f, name, ID, gender, role, major, phone, email in zip(files, names, IDs, genders, roles, majors, phones, emails):
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        else:
            fname = None

        phone_masked = mask_phone_last2(phone)

        students.append({
            'image': fname or 'profile.png',
            'name' : name,
            'ID'   : ID,
            'gender' : gender, 
            'role' : role,
            'major': major,
            'phone': phone_masked,
            'email': email
        })

    return render_template('result.html', students=students)

@app.route('/contact')
def contact_info():
    return render_template('contact.html')

@app.route('/github_qr')
def github_qr():
    return render_template('github_qr.html')

if __name__ == '__main__':
    app.run(debug=True)
