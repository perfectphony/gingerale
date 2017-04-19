from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess


class HttpRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        cmd = "python GingerAle.py {}".format(self.path)
        print(cmd)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        out, err = proc.communicate()
        out = out + err
        self.wfile.write(out)


def wsgi(port):
    print("WSGI test server starting...")

    httpd = HTTPServer(('', port), HttpRequestHandler)
    try:
        print("WSGI test server running on port", port)
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("WSGI test server shutting down...")
        httpd.server_close()


if __name__ == "__main__":
    wsgi(port=6176)
