import os
from flask import Flask, redirect, request, render_template, flash
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
allowed_extensions = {'mp4'}


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
        elif request.form.get("Show_video"):
            if os.path.isfile(f'static/output.webm'):
                return render_template("Main.html", filename='output')
            else:
                flash('Upload video, please.', 'danger')
                return redirect("/main")
        elif request.form.get("Delete_video"):
            if os.path.isfile('static/output.webm'):
                os.remove('static/output.webm')
                flash('Video was deleted.', 'success')
                return redirect("/main")
            else:
                flash('There is no video.', 'danger')
                return redirect("/main")


        f = request.files['file']
        if f:
            filename = secure_filename(f.filename)

            if filename.split('.')[1] not in allowed_extensions:
                flash('Error file type!', 'danger')
            else:
                f.save(os.path.join('static', filename))
                flash('Upload load successful. Wait a minute pls', 'success')
                os.system(f'python3 ../Yolov5_DeepSort_OSNet/track.py --source ../WebApp/static/{filename} --yolo_model ../weights/best_3n.pt --save-vid')
                os.remove(f'static/{filename}')
                os.system(f'ffmpeg -i ../Yolov5_DeepSort_OSNet/runs/track/_osnet_x0_25/{filename} -c:a copy -s 720x480 static/output.webm')
                os.remove(f'../Yolov5_DeepSort_OSNet/runs/track/_osnet_x0_25/{filename}')
                os.rmdir(f'../Yolov5_DeepSort_OSNet/runs/track/_osnet_x0_25')

        else:
            flash('No file selected!', 'danger')

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
