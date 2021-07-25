#Assignment regarding Flask App By Rupin Patel
from flask import Flask,request,render_template,redirect,flash,url_for
import os
import sys
from PIL import Image
app = Flask(__name__)
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing  import image
import numpy as np
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = '545454'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=["POST","GET"])
def start():

    filename=""
    prediction=""
    path_local=""
    r_file=""
    h_path=""

    if request.method == "POST":
        file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
            path_local = app.config['UPLOADED_PHOTOS_DEST'] + "/" + filename
            sucess=True
            r_file="static/"+filename
            model = load_model("recipe_1000.h5")
            img = image.load_img(r_file,target_size = (64,64))
            x = image.img_to_array(img)
            x = np.expand_dims(x,axis = 0)
            pred = np.argmax(model.predict(x))
            index = ["French fries","Pizza","Samosa"]
            prediction = index[pred]
            h_path="/static/"+filename


        else:
            success = False


    return render_template("index.html", file=h_path,prediction=prediction)







if __name__ == '__main__':
    app.run(debug=True)
