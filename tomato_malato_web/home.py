import os
from flask import Flask, flash, request, render_template, send_from_directory, redirect, url_for
from flask import Flask
import random
import json
import hashlib
from flask_login import *
import torch
from torchvision import transforms
from PIL import Image


# UPLOAD_FOLDER: where to save the uploaded files (temporarily?)
UPLOAD_FOLDER = os.path.join(".","static","uploads")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, static_url_path='/static')

# Secret key needed to use flash
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {'tomato@malato.it': {'password': 'password'}}

class User(UserMixin):
    pass

def predict_image(image_path):
    # Load the model
    model = torch.load("../Dataset/resnet18_model.pt")
    model.eval()

    transform = transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(125),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # Load the image
    img = Image.open(image_path)
    # Apply the transformations
    img = transform(img)
    # Create a batch of 1
    img = torch.unsqueeze(img, 0)

    class_names = ["Bacterial_spot",
                     "Early_blight",
                     "Late_blight",
                     "Leaf_Mold",
                     "Septoria_leaf_spot",
                     "Spider_mites Two-spotted_spider_mite",
                     "Target_Spot",
                     "Tomato_Yellow_Leaf_Curl_Virus",
                     "Tomato_mosaic_virus",
                     "healthy"]
    # Predict
    prediction = model(img)
    _, preds = torch.max(prediction, 1)

    return class_names[preds]

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    if email in users and request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        login_user(user)
        return redirect('/home')

    return render_template('login.html', res='bad')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.')[-1].lower() in ALLOWED_EXTENSIONS


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/home', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        if file.filename == '':
            flash('Nessun file selezionato')
            return render_template('upload.html')

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
            risultato = predict_image(os.path.join(app.config['UPLOAD_FOLDER'], img_name))
            return render_template('upload.html', name=os.path.join(app.config['UPLOAD_FOLDER'], img_name), risultato=risultato)
        elif file and not allowed_file(file.filename):
            flash('Estensione non ammessa')
            return render_template('upload.html')
    else:
         return render_template('upload.html')