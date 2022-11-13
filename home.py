import os
from flask import Flask, flash, request, redirect, render_template, send_from_directory
from flask import Flask
import random

# UPLOAD_FOLDER: where to save the uploaded files (temporarily?)
UPLOAD_FOLDER = os.path.join(".","static","uploads")
print("UPLOAD_FOLDER: ",UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, static_url_path='/static')

# Secret key needed to use flash
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        if file.filename == '':
            flash('Nessun file selezionato')
            return render_template('index.html')
        
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            risultato = random.choice(["sana", "affetta da A", "affetta da B", "affetta da C"])
            return render_template('index.html', name=os.path.join(app.config['UPLOAD_FOLDER'], file.filename), risultato=risultato)
        elif file and not allowed_file(file.filename):
            flash('Estensione non ammessa')
            return render_template('index.html')
    return render_template('index.html')