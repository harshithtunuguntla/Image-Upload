import re
from flask import Flask, request,flash, redirect
from flask.templating import render_template
from werkzeug.utils import secure_filename

import pyrebase
import os
from io import BufferedReader
import tempfile


# import firebase_admin
# from firebase_admin import credentials
import time


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'hero'
app.secret_key = "super secret key"


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

ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_extension(filename):
    return filename.rsplit('.', 1)[1].lower()










# storage.child("images/downloaded.png").put("chair.png")


metadata = " 'contentType': 'image/png'"


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/upload",methods=['GET','POST'])
def upload_the_file():
    
    if request.method == 'POST':

        if 'file' in request.files:
            print("File detected")
            image = request.files['file']
            storage.child("images/new_image.png").put(image,metadata)
        return "File Uploaded"

    return "File not uploaded"




if __name__ == '__main__':
    app.run(debug=True)
