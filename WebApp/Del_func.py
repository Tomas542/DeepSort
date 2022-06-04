import os
import shutil


def Del():
    if os.path.isdir('../Yolov5_DeepSort_OSNet/runs'):
        shutil.rmtree('../Yolov5_DeepSort_OSNet/runs')
    if os.path.isfile('static/output.webm'):
        os.remove('static/output.webm')
    if os.path.isfile('../Yolov5_DeepSort_OSNet/res.txt'):
        os.remove('../Yolov5_DeepSort_OSNet/res.txt')
    if os.path.isfile('static/res.txt'):
        os.remove('static/res.txt')
    if os.path.isfile('static/res1.txt'):
        os.remove('static/res1.txt')
    if os.path.isfile('../Yolov5_DeepSort_OSNet/time.txt'):
        os.remove('../Yolov5_DeepSort_OSNet/time.txt')
    if os.path.isfile('../Yolov5_DeepSort_OSNet/frame.txt'):
        os.remove('../Yolov5_DeepSort_OSNet/frame.txt')
    return None
