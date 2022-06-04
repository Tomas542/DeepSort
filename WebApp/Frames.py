import os


def frames():
    while True:
        if os.path.isfile('../Yolov5_DeepSort_OSNet/frame.txt'):
            with open('../Yolov5_DeepSort_OSNet/frame.txt') as f:
                line = f.readline()
                line = line.split(' ')
                frame_now = line[0]
                frame_all = line[1]
                result = (int(frame_now)/int(frame_all))
                return result
