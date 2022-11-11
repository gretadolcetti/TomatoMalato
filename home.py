import os
from flask import Flask, flash, request, redirect, render_template, send_from_directory
from flask import Flask
from flask.ext.hashing import Hashing



UPLOAD_FOLDER = '.\image'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
hashing = Hashing(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        filename_hash = hashing.hash_value(file, salt='abcd')

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_hash))
            return render_template('index.html', name='/image/'+filename_hash)
    return render_template('index.html')

@app.route('/image/<string:image>')
def send_report(image):
    print(image)
    return send_from_directory('image', image)