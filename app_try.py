import re
from flask import Flask, request
from flask.templating import render_template
from werkzeug.utils import secure_filename

import pyrebase
import os

# import firebase_admin
# from firebase_admin import credentials
import time


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'hero'


firebaseConfig = {
  "apiKey": "AIzaSyAUDh0-DJSc74VOv9mSIGULNfWxA0Jxwdo",
  "authDomain": "imageupload-19537.firebaseapp.com",
  "projectId": "imageupload-19537",
  "databaseURL": 'https://imageupload-19537.firebaseio.com',
  "storageBucket": "imageupload-19537.appspot.com",
  "messagingSenderId": "216122971515",
  "appId": "1:216122971515:web:545cf46083d59030cb19de",
  "measurementId": "G-S2PCPDGCML",
  "serviceAccount": "imageupload-19537-firebase-adminsdk-aa50y-d2df163fae.json"
}
# firebase_admin.initialize_app(cred)


firebase = pyrebase.initialize_app(firebaseConfig)
storage=firebase.storage()

# storage.child("images/image2.png").put("devchallenges.png")

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/listall")
def list_all():
    files = storage.child("images").list_files()
    for file in files:
        print(file.name)
        z=storage.child(file.name).get_url(None) 
        print(z)
        print(file)

    return("nothinn")

@app.route("/datetime")
def date_time():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    print(timestr)
    return(timestr)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload",methods=['GET','POST'])
def upload_file():
    

    if request.method=='POST':
        if 'file' not in request.files:
            print('no file part')
            return 'end'
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    return 'uploaded succesfully'




if __name__ == '__main__':
    app.run(debug=True)
