# import the necessary packages
from flask import Flask, render_template,redirect,url_for,request,session,Response
from werkzeug.utils import secure_filename
from supportFile import predict
import os
import shutil
import cv2

app=Flask(__name__,template_folder="templates")

app.secret_key='1234'
app.config["CACHE_TYPE"]="null"
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

@app.route('/',methods=['GET','POST'])
def landing():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')
           
@app.route('/info',methods=['GET','POST'])
def info():
    return render_template('index.html')

@app.route('/Image',methods=['GET','POST'])
def image():
    if request.method=='POST':
        if request.form['sub']=='Upload':
            savepath=r'upload/'
            photo=request.files['photo']
            address=os.path.join(savepath,secure_filename(photo.filename))
            photo.save(address)
            shutil.copy(address, 'static/images/test_image.jpg')
            os.remove(address)
            return render_template('<img src="{}">'.format(url_for('static',filename='static/images/test_image.jpg')))
        elif request.form['sub']=='Test':
            result=predict()
            return render_template('Image.html',result=result)
    return render_template('Image.html')        

#No caching at all for API endpoints
@app.after_request
def add_header(response):
    response.headers['Cache-Control']='no-store,no-cache,must-revalidate,post-check-0,max-age-0'
    response.headers['Pragma']='no-cache'
    response.headers['Expires']='-1'
    return response


if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True,threaded=True)

