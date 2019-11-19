"""HTTP CLIENT"""
from concurrent import futures
import requests
import csv
import sys

def read_blocks(size, cmd_str):
    """Open and read tweets from .csv file"""
    lst = []
    st = cmd_str+'endtweet'
    with open('dataSet.csv', encoding='ISO8859-1', newline='') as File:
        reader = csv.reader(File, delimiter = ';')
        for row in reader:
            if size == 0:
                break
            st = st+str(row)+'endtweet'
            if size == 1:
                st = st+' all_end '
            size -= 1
        r = requests.post("http://localhost:8000", data = (st).encode("ISO8859-1"))
        r = r.content.decode("ISO8859-1")
    return r

def handler(buf):
    """Make list from result and write it in csv file"""
    res = []
    buf = buf[0:len(buf)-2]
    buf = ''.join(buf)
    buf = buf.split(';')
    for i in buf:
        if i == 'endofthetwit':
            buf.pop(buf.index(i))
    for i in buf:
        res.append(i.split(','))
    write_result(res)
    res.clear()

def write_result(data,cmd):
    """Write result in csv file"""
    filename = cmd + 'RESULTHTTP.csv'
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for line in data:
            writer.writerow(line)
    print('Done: now you can see result in ',filename)


def get_request(l, cmd):
    """Request handler"""
    j = []
    for i in l:
        j.append(i)
    res = []
    buf = j[0:len(j)-len('allend')]
    buf = ''.join(buf)
    buf = buf.split(';')
    for i in buf:
        if i == 'endofthetwit':
            buf.pop(buf.index(i))
    for i in buf:
        res.append(i.split(','))
    write_result(res,cmd)

def write_cmd():
    """Read command and give such number of blocks with command to server"""
    cmd_str = input()
    if ((cmd_str[0:6]!='[STAT]')&(cmd_str[0:6]!='[ENTI]'))|(len(cmd_str)<9):
        print('No such command, please try [STAT][Number] or [ENTI][Number]')
    else:
        l = cmd_str.split('][')
        size = int(l[1][0:len(l[1])-1])+1
        r = read_blocks(size, cmd_str[1:5])
        get_request(r, cmd_str[1:5])

try:
    while True:
        #buf = []
        write_cmd()
except KeyboardInterrupt:
    print('\nStop working')
