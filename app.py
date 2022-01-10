import re
from flask import Flask, request,flash, redirect
from flask.templating import render_template
from werkzeug.utils import secure_filename

import pyrebase
import os
from io import BufferedReader
import tempfile

import numpy
import cv2

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


def date_time():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    print(timestr)
    return(timestr)



@app.route("/upload",methods=['GET','POST'])
def upload_file():
    
    if request.method == 'POST':

        try:
            upload = request.files['upload']
            storage.child("images/ytbupload.png").put(upload)
        except:
            pass

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        print(type(file))

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = date_time() +"." +str(file_extension(file.filename))
            # firebase_filename = "images/" + str(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            #Using Temp File Method
            # temp = tempfile.NamedTemporaryFile(delete=False)
            # file.save(temp.name)

            # filestr = request.files['file'].read()
            # npimg = numpy.fromstring(filestr, numpy.uint8)
            # # convert numpy array to image
            # img = cv2.imdecode(npimg, cv2.CV_LOAD_IMAGE_UNCHANGED)

            storage.putString(file, 'base64', {
            "contentType": 'image/jpeg'
             });

            storage.child

            # storage.child("images/ewlii.png").put(file)

            # Clean-up temp image
            # os.remove(temp.name)

            # storage.child("images/hsuh.png").put(file)
            # print(file)
            # imae = BufferedReader(file)

            return "work done"
    return 'edo poindi ra seenu'




if __name__ == '__main__':
    app.run(debug=True)
