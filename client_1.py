"""CLIENT"""
import socket
import sys
from pynlp import StanfordCoreNLP
import csv

def read_blocks(size):
    """Open and read tweets from .csv file"""
    with open('dataSet.csv', encoding='ISO8859-1', newline='') as File:
        reader = csv.reader(File, delimiter = ';')
        for row in reader:
            if size == 0:
                break
            st = str(row)+'endtweet'
            if size == 1:
                st = st+' all_end '
            sock.sendall((st).encode("ISO8859-1"))
            size -= 1

def write_cmd(sock):
    """Send command to server"""
    cmd_str = input()
    if cmd_str == '':
        return
    if (cmd_str[1:5]!='STAT')&(cmd_str[1:5]!='ENTI'):
        print('Incorrect command !\nTry STAT or ENTI')
        return
    sock.sendall(bytes((cmd_str[1:5]+'endtweet').encode("utf8")))
    l = cmd_str.split('][')
    size = int(l[1][0:len(l[1])-1])+1
    read_blocks(int(size))
    return cmd_str[1:5]

def write_result(data, cmd):
    """Write result in csv file"""
    filename = cmd + 'RESULT.csv'
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for line in data:
            writer.writerow(line)
    print('Done: now you can see result in ', filename)

def handler(sock, buf, cmd):
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
    write_result(res, cmd)
    res.clear()

def read_result(sock, buf, cmd):
    """Read result from server"""
    data = ''
    try:
        data = sock.recv(1024)
    except ConnectionResetError:
        pass
    buf.append((data).decode("ISO8859-1"))
    str1 = buf[len(buf)-1]
    if str1[len(str1)-6:len(str1)]== 'allend':
        handler(sock, buf, cmd)
        buf.clear()
    return buf

buf = []
port = input('Port:')
if port == '':
    port = 30000
else:
    port = int(port)
sock = socket.socket()
sock.connect(('127.0.0.1',int(port)))
nlp = StanfordCoreNLP('http://localhost:9000')
try:
    while True:
        if len(buf) == 0:
            cmd = write_cmd(sock)
        buf = read_result(sock, buf, cmd)
except KeyboardInterrupt:
    print('\nStop working')
