def Add_time():
    with open('static/res.txt', 'r') as r, open('../Yolov5_DeepSort_OSNet/time.txt', 'r') as t, open('static/res1.txt',
                                                                                                     'w') as nr:
        rlines = r.readlines()
        tlines = t.readlines()
        for i in range(len(rlines)):
            nr.write(rlines[i].split('\n')[0] + '\t' + tlines[i].split('\t')[1])
    return None