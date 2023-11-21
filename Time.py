# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import cv2
import json
from datetime import datetime



hostName = "0.0.0.0"
serverPort = 1233
vid = cv2.VideoCapture(0)

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        current_dateTime = datetime.today().strftime('%Y/%m/%d %H:%M:%S')
        time = {}
        time['time'] = str(current_dateTime)
        time_json = json.dumps(time)
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.send_header("Content-Length", len(time_json))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(bytes(time_json, "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

