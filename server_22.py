"""HTTP SERVER"""
from sys import getsizeof
from http.server import HTTPServer, BaseHTTPRequestHandler, ThreadingHTTPServer
from stat_and_enti2 import *


class RequestHeandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.data_string = ''
    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        tmp = []
        content_length = int(self.headers['Content-Length'])
        self.data_string = self.rfile.read(content_length)
        tmp = read(tmp, self.data_string)
        self._set_headers()
        tmp = handler(tmp)
        string = ''
        for res in tmp:
            string += res
        self.wfile.write((string.encode("ISO8859-1")))

def read(buf, string):
    string = string.decode("ISO8859-1")
    buf.append(string)
    return buf

def handler(buf):
    tmp = ''.join(buf)
    str1 = buf[len(buf)-1]
    if str1[len(str1)-len('all_end')-1:len(str1)-1] == 'all_end':
        buf[len(buf)-1] = buf[len(buf)-1][0:len(str1)-len(' all_end ')-1]
        i = tmp.find('endtweet')
        buf.clear()
        while i!=-1:
            buf.append(tmp[0:i])
            tmp = tmp[i+len('endtweet'):len(tmp)]
            i = tmp.find('endtweet')
    cmd = buf.pop(0)
    lst = []
    for i in buf:
        j = eval(i)
        lst.append(j)
    for i in lst:
        buf.append(' '.join(i)+'\n')
    if cmd == 'ENTI':
        res = enti_fun(buf)
    elif cmd == 'STAT':
        res = stat_fun(lst)
    return res

def run(server_class=ThreadingHTTPServer, handler_class=RequestHeandler, addr="localhost", port=8000):
    try:
        server_address = (addr, port)
        httpd = server_class(server_address, handler_class)
        print('Press ctrl-C to stop')
        print(f"Starting httpd server on {addr}:{port}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
        print('\nStop server.')
run()
