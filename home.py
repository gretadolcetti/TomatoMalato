import os
from flask import Flask, flash, request, redirect, render_template, send_from_directory
from flask import Flask
import random
import json
import hashlib

# UPLOAD_FOLDER: where to save the uploaded files (temporarily?)
UPLOAD_FOLDER = os.path.join(".","static","uploads")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, static_url_path='/static')

# Secret key needed to use flash
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.')[-1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        if file.filename == '':
            flash('Nessun file selezionato')
            return render_template('index.html')
        
        images_hash = open(os.path.join(".","static","uploads","images_hash.json")).read()
        images_hash = json.loads(images_hash)

        img_key = hashlib.md5(file.read()).hexdigest()
        
        if file and allowed_file(file.filename):
            # Save image in the uploads folder if it is not already present
            if img_key not in images_hash:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], img_key))
                images_hash[img_key] = file.filename
                with open(os.path.join(".","static","uploads","images_hash.json"), "w") as f:
                    f.write(json.dumps(images_hash))
            risultato = random.choice(["sana", "affetta da A", "affetta da B", "affetta da C"])
            return render_template('index.html', name=os.path.join(app.config['UPLOAD_FOLDER'], file.filename), risultato=risultato)
        elif file and not allowed_file(file.filename):
            flash('Estensione non ammessa')
            return render_template('index.html')
    return render_template('index.html')