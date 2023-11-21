# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer

import json
from datetime import datetime

hostName = "0.0.0.0"
serverPort = 1234

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/home":
            with open("test.html", "rb") as fp:
                html = fp.read().decode('utf-8', 'ignore')
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(html, "utf-8"))

        if self.path == "/data":
            feeding_time = []
            with open('log.txt') as f:
                for line in f:
                    try:
                        feeding_time.append(json.loads(line))
                    except:
                        pass

            time_json = json.dumps(feeding_time)
            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.send_header("Content-Length", len(time_json))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes(time_json, "utf-8"))

        if self.path =="/time":
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


    def do_POST(self):
        # if self.path == "/data":
            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            post_data = self.rfile.read(content_length)  # <--- Gets the data itself
            data_json = json.loads(post_data)
            print(data_json['start'])
            # feeding_times = []
            # with open('log.txt') as f:
            #     for line in f:
            #         try:
            #             feeding_times.append(json.loads(line))
            #         except:
            #             pass
            # for feeding_time in feeding_times:
            #     if feeding_time["start"] == data_json['start']:
            #         print("match")
            #     with open("log.txt", "a") as f:
            #     f.write("\n" + post_data.decode("utf-8"))

            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()

            with open('log.txt', 'r') as file:
                lines = file.readlines()
            existing_start = False
                # Check each line against the criteria and modify if needed
            for i, line in enumerate(lines):
                entry = json.loads(line)  # Assuming each line contains a JSON object
                if entry["start"] == data_json['start']:
                    # Modify the entry as needed
                    entry["end"] = data_json['end']
                    lines[i] = json.dumps(entry) + "\n"
                    existing_start = True

                # Write the modified lines back to the file
            if existing_start:
                with open('log.txt', 'w') as file:
                    file.writelines(lines)
            else:
                with open("log.txt", "a") as f:
                    f.write(post_data.decode("utf-8") + "\n")

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

