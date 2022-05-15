import os.path
import sys

from flask import Flask, redirect, request, render_template
from werkzeug.utils import secure_filename
import ffmpeg

allowed_extensions = {'mp4', 'docx'}


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return redirect("/main")


@app.route('/main', methods=['POST', 'GET'])
def page_main():
    if request.method == 'POST':
        if request.form.get('Main'):
            return redirect("/main")
        elif request.form.get("About_Us"):
            return redirect("/about_us/")
        elif request.form.get("About_Project"):
            return redirect("/about_project/")
        f = request.files['file']
        if f:
            filename = secure_filename(f.filename)
            if filename.split('.')[1] not in allowed_extensions:
                return 'Error file type'
            else:
                f.save(os.path.join('source', filename))
                os.system(f'python3 ../Yolov5_DeepSort_OSNet/track.py --source ../WebApp/source/{filename} --yolo_model ../weights/best_3n.pt --save-vid')
                os.remove(f'source/{filename}')
                os.system(f'ffmpeg -i ../Yolov5_DeepSort_OSNet/runs/track/_osnet_x0_25/{filename} -c:a copy -s hd720 output.webm')
                return render_template('Main.html', filename='source/output.webm')
    return render_template('Main.html')


@app.route('/about_us/', methods=['GET', 'POST'])
def page_about_us():
    if request.method == 'POST':
        if request.form.get('Main'):
            return redirect("/")
        elif request.form.get("About_Us"):
            return redirect("/about_us/")
        elif request.form.get("About_Project"):
            return redirect("/about_project/")
    return render_template('About_Us.html')


@app.route('/about_project/', methods=['GET', 'POST'])
def page_about_project():
    if request.method == 'POST':
        if request.form.get('Main'):
            return redirect("/")
        elif request.form.get("About_Us"):
            return redirect("/about_us/")
        elif request.form.get("About_Project"):
            return redirect("/about_project/")
    return render_template('About_Project.html')


if __name__ == '__main__':
    app.run()
