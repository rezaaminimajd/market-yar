from http.server import BaseHTTPRequestHandler, HTTPServer
import argparse, sys, requests

from socketserver import ThreadingMixIn

hostname = 'localhost'
port = 8080


def merge_two_dicts(x, y):
    return {**x, **y}


def set_header():
    headers = {
        'host': '##proxy##admin##'
    }
    return headers


class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'

    def do_HEAD(self):
        self.do_GET(body=False)
        return

    def do_GET(self, body=True):
        sent = False
        try:
            url = 'http://{}:{}{}'.format(hostname, port, self.path)
            req_header = self.parse_headers()

            print(req_header)
            print(url)
            resp = requests.get(url, headers=merge_two_dicts(req_header, set_header()), verify=False)
            sent = True

            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            msg = resp.text
            if body:
                self.wfile.write(msg.encode(encoding='UTF-8', errors='strict'))
            return
        finally:
            if not sent:
                self.send_error(404, 'error trying to proxy')

    def do_POST(self, body=True):
        sent = False
        try:
            url = 'http://{}:{}{}'.format(hostname, port, self.path)
            content_len = int(self.headers['content-length'] if self.headers['content-length'] else 0)
            post_body = self.rfile.read(content_len)
            req_header = self.parse_headers()

            resp = requests.post(url, data=post_body, headers=merge_two_dicts(req_header, set_header()), verify=False)
            sent = True

            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            if body:
                self.wfile.write(resp.content)
            return
        finally:
            if not sent:
                self.send_error(404, 'error trying to proxy')

    def parse_headers(self):
        req_header = {}
        for line in self.headers:
            line_parts = [o.strip() for o in line.split(':', 1)]
            if len(line_parts) == 2:
                req_header[line_parts[0]] = line_parts[1]
        return req_header

    def send_resp_headers(self, resp):
        respheaders = resp.headers
        print('Response Header')
        for key in respheaders:
            if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding',
                           'content-length', 'Content-Length']:
                print(key, respheaders[key])
                self.send_header(key, respheaders[key])
        self.send_header('Content-Length', str(len(resp.content)))
        self.end_headers()


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Proxy HTTP requests')
    parser.add_argument('--port', dest='port', type=int, default=8081,
                        help='serve HTTP requests on specified port (default: random)')
    parser.add_argument('--hostname', dest='hostname', type=str, default='localhost',
                        help='hostname to be processd (default: localhost)')
    args = parser.parse_args(argv)
    return args


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    global hostname
    args = parse_args(argv)
    hostname = args.hostname
    print('http server is starting on {} port {}...'.format(args.hostname, args.port))
    server_address = ('127.0.0.1', args.port)
    httpd = ThreadedHTTPServer(server_address, ProxyHTTPRequestHandler)
    print('http server is running as proxy')
    httpd.serve_forever()


if __name__ == '__main__':
    main()
