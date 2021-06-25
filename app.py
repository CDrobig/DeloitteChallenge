from flask import Flask, request
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
        #unbalancedColumns(df)
        checkData(df)

        return 'file uploaded successfully'




if __name__ == '__main__':
    app.run()
