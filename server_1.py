"""SERVER"""
from stat_and_enti import *

def handler(buf, conn):
    tmp = []
    cmd = (buf.pop(0))
    cmd = cmd[1:5]
    counter = 1
    for i in buf:
        j = eval(i)
        tmp.append(j)
    buf.clear()
    for i in tmp:
        buf.append(' '.join(i)+'\n')
    if cmd == 'ENTI':
        enti_fun(buf, conn)
        buf.clear()
    elif cmd == 'STAT':
        stat_fun(tmp, conn)



def process_request(conn, addr):
    print("connected client:", addr)
    buf = []
    with conn:
        while True:
            tmp = ''
            data = conn.recv(1024)
            if not data:
                break
            data = data.decode("ISO8859-1")
            buf.append(data)
            tmp = ' '.join(buf)
            str1 = buf[len(buf)-1]
            if str1[len(str1)-len('all_end')-1:len(str1)-1] == 'all_end':
                buf[len(buf)-1] = buf[len(buf)-1][0:len(str1)-len(' all_end ')]
                i = tmp.find('endtweet')
                buf.clear()
                while i!=-1:
                    buf.append(tmp[0:i])
                    tmp = tmp[i+len('endtweet'):len(tmp)]
                    i = tmp.find('endtweet')
                handler(buf, conn)
                buf.clear()
        conn.close()

def worker(sock):
    try:
        while True:
            conn, addr = sock.accept()
            th = threading.Thread(target=process_request, args=(conn, addr))
            th.start()
    except KeyboardInterrupt:
        return
     
port = input('Port:')
if port == '':
    port = 30000
else:
    port = int(port)
with socket.socket() as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", port))
    sock.listen()
    try:    
        workers_count = 3
        workers_list = [multiprocessing.Process(target=worker, args=(sock,))
                        for _ in range(workers_count)]
        
        for w in workers_list:
            w.start()
        
        for w in workers_list:
            w.join()
    except KeyboardInterrupt:
        print('\nServer stops.')
