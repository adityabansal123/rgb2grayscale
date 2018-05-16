import os
import numpy as np
import cv2
from flask import Flask, request, redirect, url_for,send_from_directory, render_template
from werkzeug import secure_filename

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	cap = cv2.VideoCapture(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
	height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
	fourcc = cv2.VideoWriter_fourcc(*"XVID")
    	out = cv2.VideoWriter(os.path.join(app.config['UPLOAD_FOLDER'], 'gray '+filename), fourcc, 20.0, (int(width), int(height)))
	while(True):
	    ret, frame = cap.read()
	    if ret == True:
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		out.write(gray)
	    else:
		break
	cap.release()
	out.release()
	return redirect(url_for('uploaded_file', filename=filename))
    return render_template('index.html') 

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'gray '+filename)


if __name__ == '__main__':
    app.run(debug=True)
