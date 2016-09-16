#  coding: utf-8 
import SocketServer, os.path, inspect

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Justin Wong
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        #nitty gritty parsing & variable initialization
        getfile = self.data.split()[1]
        filename = inspect.stack()[0][1]
        directory = os.path.dirname(os.path.abspath(filename)) + "/www"
        filepath = directory + getfile
        status = "status"

        #checks if the path is a file
        if os.path.isfile(filepath):
            #checks for .html extension
            if(getfile.split('.')[1]).lower() == "html":
                mtype = "text/html"
                status = "HTTP/1.1 200 OK\r\n" + "Content-Type: " + mtype + "\r\n\r\n" + open(filepath).read()
               
            #checks for .css extension
            elif(getfile.split('.')[1]).lower() == "css":
                mtype = "text/css"
                status = "HTTP/1.1 200 OK\r\n" + "Content-Type: " + mtype + "\r\n\r\n" + open(filepath).read()

            #deals with security in regards to nonexistent paths
            else:
                mtype = "text/plain"
                status = "HTTP/1.1 404 Not Found\r\n" + "Content-Type: " + mtype + "\r\n\r\n"

        #checks if the path is a directory and opens "index.html" if it exists
        elif os.path.isdir(filepath) and os.path.isfile(filepath + "/index.html"):
            mtype = "text/html"                
            status = "HTTP/1.1 200 OK\r\n" + "Content-Type: " + mtype + "\r\n\r\n" + open(filepath + "index.html").read()     

        #catches things that don't exist
        else:
            mtype = "text/plain"
            status = "HTTP/1.1 404 Not Found\r\n" + "Content-Type: " + mtype + "\r\n\r\n"

        #print ("Got a request of: %s\n" % self.data)/index.html
        self.request.sendall(status)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()