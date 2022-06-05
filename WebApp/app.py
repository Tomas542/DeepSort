import os
import shutil
from flask import Flask, redirect, request, render_template, flash, send_file
from werkzeug.utils import secure_filename
import psycopg2
from time import sleep
from Del_func import Del
from Add_time import Add_time
from Frames import frames


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
allowed_extensions = {'mp4'}
check = 0

conn = psycopg2.connect(database="webapp_db",
                        user="postgres",
                        password="123",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()
Del()


@app.route('/', methods=['GET'])
def index():
    return redirect("/main")


@app.route('/main', methods=['GET', 'POST'])
def page_main():
    global check
    percent = 0
    bar_check = ''
    if request.method == 'POST':
        if request.form.get('Main'):
            return redirect("/main")
        elif request.form.get("About_Us"):
            return redirect("/about_us/")
        elif request.form.get("About_Project"):
            return redirect("/about_project/")
        elif request.form.get("Show_video"):
            bar_check = ''
            if check == 0:
                if os.path.isfile('static/output.webm'):
                    return render_template("Main.html", filename='output')
                else:
                    flash('Upload video, please.', 'danger')
            else:
                flash('Video is being processed!', 'danger')
                bar_check = 'aaa'
                percent = frames()
            return render_template("Main.html", bar_check=bar_check, percent=percent)


        elif request.form.get("Download_video"):
            bar_check = ''
            if check == 0:
                if os.path.isfile('static/output.webm'):
                    return send_file('static/output.webm', as_attachment=True)
                else:
                    flash('There is no video.', 'danger')
            else:
                flash('Video is being processed!', 'danger')
                bar_check = 'aaa'
                percent = frames()
            return render_template("Main.html", bar_check=bar_check, percent=percent)

        elif request.form.get("Download_txt"):
            bar_check = ''
            if check == 0:
                if os.path.isfile('static/res.txt'):
                    return send_file('static/res.txt', as_attachment=True)
                else:
                    flash('There is no txt.', 'danger')
            else:
                flash('Video is being processed!', 'danger')
                bar_check = 'aaa'
                percent = frames()
            return render_template("Main.html", bar_check=bar_check, percent=percent)
        f = request.files['file']
        if f:
            bar_check = ''
            filename = secure_filename(f.filename)

            if filename.split('.')[1] not in allowed_extensions:
                flash('Error file type! Only mp4 supported', 'danger')
            else:
                if check == 0:

                    f.save(os.path.join('static', filename))
                    check = 1
                    flash('Upload load successful. Wait a minute pls', 'success')

                    Del()

                    os.system(f'python3 ../Yolov5_DeepSort_OSNet/track.py --source ../WebApp/static/{filename}'
                              f' --yolo_model ../weights/best_7n.pt --save-vid')
                    os.remove(f'static/{filename}')
                    os.system(f'ffmpeg -i ../Yolov5_DeepSort_OSNet/runs/track/_osnet_x0_25/{filename} -c:a copy -s '
                              f'720x480 static/output.webm')

                    if os.path.isdir('../Yolov5_DeepSort_OSNet/runs'):
                        shutil.rmtree('../Yolov5_DeepSort_OSNet/runs')
                    if os.path.isfile('../Yolov5_DeepSort_OSNet/res.txt'):
                        os.rename('../Yolov5_DeepSort_OSNet/res.txt', 'static/res.txt')
                    while True:
                        if os.path.isfile('static/res.txt'):
                            break
                        else:
                            sleep(0.5)
                    video = filename.split('.')[0]

                    Add_time('static/res.txt', '../Yolov5_DeepSort_OSNet/time.txt', 'static/res1.txt')

                    os.rename('static/res1.txt', 'static/res.txt')

                    with open('static/res.txt', 'r') as f:
                        for line in f.readlines():
                            clss = line.split('\t')[0]
                            num = line.split('\t')[1]
                            time = line.split('\t')[2]
                            accuracy = line.split('\t')[3]
                            time_f = line.split('\t')[4]
                            time_l = line.split('\t')[5].split('\n')[0]
                            cursor.execute(
                                "INSERT INTO main.info (video, time_found, time_lost, class, number, time, accuracy) "
                                "VALUES (%s, %s, %s, %s, %s, %s, %s);",
                                (video, time_f, time_l, clss, num, time, accuracy))
                            conn.commit()

                    check = 0
                else:
                    flash('Video is being processed!', 'danger')
                    bar_check = 'aaa'
                    percent = frames()
        else:
            flash('No file selected!', 'danger')
    return render_template("Main.html", bar_check=bar_check, percent=percent)


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
