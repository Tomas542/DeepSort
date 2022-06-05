import os
from app import app
import requests
import subprocess
import time
import signal
from Add_time import Add_time


def test_server_200():
    a = subprocess.Popen('python3 -m http.server 8080', shell=True, preexec_fn=os.setsid)
    time.sleep(1)
    res = requests.get('http://localhost:8080/')
    os.killpg(os.getpgid(a.pid), signal.SIGTERM)
    assert res.status_code == 200


def test_server_404():
    a = subprocess.Popen('python3 -m http.server 8080', shell=True, preexec_fn=os.setsid)
    time.sleep(1)
    res = requests.get('http://localhost:8080/asdasd')
    os.killpg(os.getpgid(a.pid), signal.SIGTERM)
    assert res.status_code == 404


def test_ask_for_pages():
    with app.test_client() as client:
        res_main = client.get('/main')
        res_ab_us = client.get('/about_us')
        res_ab_pr = client.get('/about_project')
        assert res_main.status_code == 200
        assert res_ab_us.status_code == 308
        assert res_ab_pr.status_code == 308


def test_style():
    with app.test_client() as client:
        res = client.get('/static/style.css')
        assert res.status_code == 200


def test_show_pages():
    with app.test_client() as client:
        res_ab_us = client.post('/about_us/')
        res_ab_pr = client.post('/about_project/')
        assert res_ab_us.status_code == 200
        assert res_ab_pr.status_code == 200


def test_add_time():
    assert Add_time('WebApp/test/test1.txt', 'WebApp/test/test2.txt', 'WebApp/test/test3.txt') is None
