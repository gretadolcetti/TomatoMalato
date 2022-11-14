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
        
        uploads_folder_path = os.path.join(".","static","uploads")
        if not os.path.exists(uploads_folder_path):
            os.mkdir(uploads_folder_path)
        if not os.path.exists(os.path.join(uploads_folder_path,"images_hash.json")):
            open(os.path.join(uploads_folder_path,"images_hash.json"), 'x')
            images_hash = {}
        else:
            images_hash_file = open(os.path.join(uploads_folder_path,"images_hash.json"), 'r')
            images_hash = images_hash_file.read()
            images_hash = json.loads(images_hash)
        split_tup = os.path.splitext(file.filename)
        img_key = hashlib.md5(file.read()).hexdigest()
        img_name = img_key+split_tup[1]
        file.seek(0)

        if file and allowed_file(file.filename):
            # Save image in the uploads folder if it is not already present
            if img_key not in images_hash:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], img_name))
                images_hash[img_key] = file.filename
                with open(os.path.join(uploads_folder_path,"images_hash.json"), "w") as f:
                    f.write(json.dumps(images_hash))
            risultato = random.choice(["sana", "affetta da A", "affetta da B", "affetta da C"])
            return render_template('index.html', name=os.path.join(app.config['UPLOAD_FOLDER'], img_name), risultato=risultato)
        elif file and not allowed_file(file.filename):
            flash('Estensione non ammessa')
            return render_template('index.html')
    return render_template('index.html')