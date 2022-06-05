def Add_time(f1, f2, f3):
    with open(f1, 'r') as r, open(f2, 'r') as t, open(f3,
                                                                                                     'w') as nr:
        rlines = r.readlines()
        tlines = t.readlines()
        for i in range(len(rlines)):
            nr.write(rlines[i].split('\n')[0] + '\t' + tlines[i].split('\t')[1])
    return None
