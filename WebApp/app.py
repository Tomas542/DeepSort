from flask import Flask, redirect, request, render_template


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('Main.html')


@app.route('/', methods=['POST', 'GET'])
def p_main():
    if request.method == 'POST':
        if request.form.get('Main'):
            return redirect("/")
        elif request.form.get("About_Us"):
            return redirect("/about_us/")
        elif request.form.get("About_Project"):
            return redirect("/about_project/")


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
