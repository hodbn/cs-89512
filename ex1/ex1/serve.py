import http.server
import os
import socketserver

BUILD = "build"
PORT = 0
HANDLER = http.server.SimpleHTTPRequestHandler


def main():
    print("moving to output dir", BUILD)
    os.chdir(BUILD)
    with socketserver.TCPServer(("", PORT), HANDLER) as httpd:
        free_port = httpd.server_address[1]
        print("serving at port", free_port)
        url = f"http://localhost:{free_port}/"
        print("url is", url)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
