from flask import Flask, request, current_app, send_from_directory, send_file
import pandas as pd
import os
from werkzeug.utils import secure_filename
from biasChecker import checkData

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/upload')
def upload_file():
    return """<html>
   <body>
      <form action = "http://localhost:5000/uploader" method = "POST"
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>
   </body>
</html>"""

@app.route('/uploader', methods=['GET', 'POST'])
def file_uploader():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join("./", filename))

        df = pd.read_csv(filename, delimiter=",", encoding="utf-8")
        checkData(df)

        return 'file uploaded successfully'

@app.route('/uploadCV')
def upload_CVfile():
    return """<html>
   <body>
      <form action = "http://localhost:5000/CVuploader" method = "POST"
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>
   </body>
</html>"""

@app.route('/CVuploader', methods=['GET', 'POST'])
def CVfile_uploader():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join("./exampleCV/original/", filename))
        file = filename.split(".")[0]
        #uploads = os.path.join(current_app.root_path, app.config['./exampleCV/unbiased'])
        path = "./exampleCV/unbiased/"+file+"_unbiased.jpeg"
        return send_file(path, as_attachment=True)




if __name__ == '__main__':
    app.run()
