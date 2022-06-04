import os
import shutil
from flask import Flask, redirect, request, render_template, flash, send_file
from werkzeug.utils import secure_filename
import psycopg2
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
allowed_extensions = {'mp4'}
check = 0

conn = psycopg2.connect(database="webapp_db",
                        user="postgres",
                        password="1234567890",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


@app.route('/', methods=['GET'])
def index():
    return redirect("/main")


@app.route('/main', methods=['POST', 'GET'])
def page_main():
    global check
    bar_check = ''
    if request.method == 'POST':
        if request.form.get('Main'):
            return redirect("/main")
        elif request.form.get("About_Us"):
            return redirect("/about_us/")
        elif request.form.get("About_Project"):
            return redirect("/about_project/")
        elif request.form.get("Show_video"):
            if check == 0:
                if os.path.isfile('static/output.webm'):
                    return render_template("Main.html", filename='output')
                else:
                    flash('Upload video, please.', 'danger')
            else:
                flash('Video is being processed!', 'danger')
                bar_check = 'aaa'
            return render_template("Main.html", bar_check=bar_check)
            bar_check = ''

        elif request.form.get("Download_video"):
            if check == 0:
                if os.path.isfile('static/output.webm'):
                    flash('Video was sent to you.', 'success')
                    return send_file('static/output.webm', as_attachment=True)
                else:
                    flash('There is no video.', 'danger')
            else:
                flash('Video is being processed!', 'danger')
                print('nazhal')
                bar_check = 'aaa'
            return render_template("Main.html", bar_check=bar_check)
            bar_check = ''
        elif request.form.get("Download_txt"):
            if check == 0:
                if os.path.isfile('static/res.txt'):
                    flash('Txt was sent to you.', 'success')
                    return send_file('static/res.txt', as_attachment=True)
                else:
                    flash('There is no txt.', 'danger')
            else:
                flash('Video is being processed!', 'danger')
                bar_check = 'aaa'
            return render_template("Main.html", bar_check=bar_check)
            bar_check = ''
        f = request.files['file']
        if f:
            filename = secure_filename(f.filename)

            if filename.split('.')[1] not in allowed_extensions:
                flash('Error file type! Only mp4 supported', 'danger')
            else:
                if check == 0:
                    if os.path.isdir('../Yolov5_DeepSort_OSNet/runs'):
                        shutil.rmtree('../Yolov5_DeepSort_OSNet/runs')
                    f.save(os.path.join('static', filename))
                    check = 1
                    flash('Upload load successful. Wait a minute pls', 'success')
                    if os.path.isfile('static/output.webm'):
                        os.remove('static/output.webm')
                    if os.path.isfile('../Yolov5_DeepSort_OSNet/res.txt'):
                        os.remove('../Yolov5_DeepSort_OSNet/res.txt')
                    if os.path.isfile('static/res.txt'):
                        os.remove('static/res.txt')

                    os.system(f'python3 ../Yolov5_DeepSort_OSNet/track.py --source ../WebApp/static/{filename}'
                              f' --yolo_model ../weights/best_7n.pt --save-vid')
                    os.remove(f'static/{filename}')
                    os.system(f'ffmpeg -i ../Yolov5_DeepSort_OSNet/runs/track/_osnet_x0_25/{filename} -c:a copy -s '
                              f'720x480 static/output.webm')
                    if os.path.isdir('../Yolov5_DeepSort_OSNet/runs'):
                        shutil.rmtree('../Yolov5_DeepSort_OSNet/runs')
                    if os.path.isfile('../Yolov5_DeepSort_OSNet/res.txt'):
                        os.rename('../Yolov5_DeepSort_OSNet/res.txt', 'static/res.txt')
                    video = filename.split('.')[0]
                    with open('static/res.txt', 'r') as f:
                        for line in f.readlines():
                            dt = str(datetime.now())
                            clss = line.split(' ')[0]
                            num = line.split(' ')[1]
                            time = line.split(' ')[2]
                            accuracy = line.split(' ')[3].split('\n')[0]
                            cursor.execute("INSERT INTO main.info (video, datetime, class, number, time, accuracy) VALUES (%s, %s, %s, %s, %s, %s);",
                                           (video, dt, clss, num, time, accuracy))
                            conn.commit()
                    check = 0
                else:
                    flash('Video is being processed!', 'danger')
                    bar_check = 'aaa'
        else:
            flash('No file selected!', 'danger')
    return render_template("Main.html", bar_check=bar_check)
    bar_check = ''


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
    app.run(host='0.0.0.0', port=8080)
