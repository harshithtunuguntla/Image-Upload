import re
from flask import Flask, request,flash, redirect, jsonify, make_response
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import secure_filename

import pyrebase
import os
import base64

import config

# import firebase_admin
# from firebase_admin import credentials
import time


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'hero'
app.secret_key = "super secret key"


firebaseConfig = {
  "apiKey": config.apiKey,
  "authDomain": config.authDomain,
  "projectId": config.projectId,
  "databaseURL": config.databaseURL,
  "storageBucket": config.storageBucket,
  "messagingSenderId": config.messagingSenderId,
  "appId": config.appId,
  "measurementId": config.measurementId,
  "serviceAccount": config.serviceAccount
}


firebase = pyrebase.initialize_app(firebaseConfig)
storage=firebase.storage()



ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_extension(filename):
    return filename.rsplit('.', 1)[1].lower()

def date_time():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    print(timestr)
    return(timestr)

metadata = '"contentType": "image/jpeg"'


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



@app.route('/upload/drop',methods=['POST','GET'])
def upp():
    if request.method == 'POST':
        print("something happp")
        img_data = request.json['data']
        img = img_data.partition(",")[2]
        img = base64.b64decode(img)
        
        raw_file_name = date_time() 
        
        filepath = "images/"+ raw_file_name

        storage.child(filepath).put(img,metadata)
        
        img_url = storage.child(filepath).get_url(None)


        # resp = {"img_url":img_url}
        # redirect(url_for('/listall'))
        # render_template('display_image.html',img_url=img_url,file_name=raw_file_name)
        resp = make_response(jsonify({"img_url": img_url,"img_name":raw_file_name}), 200)

        return resp

    return 'Nothing Happening'

@app.route("/upload",methods=['GET','POST'])
def upload_file():
    
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            
            filename = secure_filename(file.filename)

            raw_file_name = date_time() 
            
            filepath = "images/"+ raw_file_name

            storage.child(filepath).put(file,metadata)

            img_url = storage.child(filepath).get_url(None)
            # print(img_url)
            # print(filename)
            # return render_template('display_image.html',img_url=img_url,file_name=raw_file_name)
            url = "/display/" + str(raw_file_name)
            return redirect(url)
    return 'Error Occured.. (Could be because file format not supported,server not resonding.)'

# @app.route("/upload/<url>")
# def display(url):
#     img_url = url
#     file_name = "images/" + str(name)
#     img_url = storage.child(file_name).get_url(None)
#     print(img_url)
#     return redirect(img_url)




@app.route("/display/<name>")
def display(name):
    file_name = "images/" + str(name)
    img_url = storage.child(file_name).get_url(None)
    print(img_url)
    return render_template('display_image.html',img_url=img_url,file_name=name)


@app.route("/show/<name>")
def show(name):
    img_name = name
    file_name = "images/" + str(name)
    img_url = storage.child(file_name).get_url(None)
    return redirect(img_url)




if __name__ == '__main__':
    # app.run(debug=True, host= '192.168.0.xxx')
    app.run(debug=True)

