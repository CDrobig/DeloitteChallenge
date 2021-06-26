from flask import Flask, request, send_file, render_template
import pandas as pd
import os
from werkzeug.utils import secure_filename
from biasChecker import checkData, generateData
import json

app = Flask(__name__)
 #test application
@app.route('/')
def hello_world():
    return render_template('index.html')

#calculate Bias Score
@app.route('/uploader', methods=['GET', 'POST'])
def file_uploader():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(+filename))

        df = pd.read_csv(+filename, delimiter=",", encoding="utf-8")
        score = checkData(df)

        return 'The Data Bias Score of you file is at: ' + str(score)

#anonymyse and synthetisize CV to create a sample of male and female version
@app.route('/CVuploader', methods=['GET', 'POST'])
def CVfile_uploader():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join("exampleCV/original/", filename))
        file = filename.split(".")[0]
        #uploads = os.path.join(current_app.root_path, app.config['./exampleCV/unbiased'])
        path = "./exampleCV/unbiased/exampleCV_unbiased.jpg"
        return send_file(path, as_attachment=True)

#use GAN for data augmentation of unbalanced data
@app.route('/gan', methods=['GET', 'POST'])
def gan():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join("/", filename))

        inputData = pd.read_csv(filename, delimiter=",", encoding="utf-8")

        generatedData = generateData(inputData)

        return send_file(generatedData, as_attachment=True)

#check document if it contais skillSet words and calculate a score based on word similarity
@app.route('/skillSet/<a>/<b>/<c>')
def createcm(a=None, b=None, c=None, d=None, e=None):
    wordList = [a, b, c]
    score = 0
    #todo: introduce word similarity
    #https://cloud.google.com/vision/docs/ocr
    f = open('exampleCVSkillSet.json')
    data = json.load(f)
    f.close()
    for (k, v) in data.items():
        for word in wordList:
            if word in str(v):
                score += 50

    #todo: export as csv
    return "Your SkillSet-Score is: " + str(score)


#read in CSV file to scan for bias
@app.route('/upload')
def upload_file():
    filename="unbalanced_data_sex.csv"
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(+filename))

    df = pd.read_csv(filename, delimiter=",", encoding="utf-8")
    score = checkData(df)

    return render_template('upload.html')


@app.route('/augmentation')
def augmentation():
    return render_template('augmentation.html')

@app.route('/twin')
def twin():
    #f = request.files['file']
    #filename = secure_filename(f.filename)
    #f.save(os.path.join("exampleCV/original/", filename))
    #file = filename.split(".")[0]
    # uploads = os.path.join(current_app.root_path, app.config['./exampleCV/unbiased'])
    path = "./exampleCV/unbiased/exampleCV_unbiased.jpg"
    send_file(path, as_attachment=True)
    return render_template('twin.html')

#read in CSV for data augmentation via GAN
@app.route('/augmentData')
def augment_data():
    return """<html>
   <body>
      <form action = "http://localhost:5000/gan" method = "POST"
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>
   </body>
</html>"""

#read in CV for anonymisazion and synthetisation
@app.route('/uploadCV')
def upload_CVfile():
    return """<html>
   <body>
      <form action = "http://127.0.0.1:5000/CVuploader" method = "POST"
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>
   </body>
</html>"""

#enter skillSet to scan document
@app.route('/getSkillSetScore')
def skillSet():
    return """<html>
   <body>
      <form action = "http://127.0.0.1:5000/skillSet" method = "POST"
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>
   </body>
</html>"""

if __name__ == '__main__':
    app.run()

