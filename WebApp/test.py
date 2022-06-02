import os

import requests
import subprocess
import time
import signal


def test_server_200():
    a = subprocess.Popen('python3 -m http.server 8080', shell=True, preexec_fn=os.setsid)
    time.sleep(1)
    res = requests.get('http://localhost:8080/')
    os.killpg(os.getpgid(a.pid), signal.SIGTERM)
    assert res.status_code == 200


def test_server_404():
    a = subprocess.Popen('python3 -m http.server 8080', shell=True, preexec_fn=os.setsid)
    time.sleep(1)
    res = requests.get('http://localhost:8080/main')
    os.killpg(os.getpgid(a.pid), signal.SIGTERM)
    assert res.status_code == 404
