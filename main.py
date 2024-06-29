import os

from flask import Flask, render_template, Response
from app.cat import detect_cats

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

detect_cats()

@app.route('/video_feed')
def video_feed():
    return Response(detect_cats(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
