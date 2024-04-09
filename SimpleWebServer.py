#What we want is to write our own simple web server

#Steps
#1 - Wait for someone to connect to our web server
#2 - Parse that request
#3 - Figure out what it is that they're asking for
#4 - Fetch the data or Generate it dynamically
#5 - Format the data as HTML
#6 - Send it right back

#Since Steps 1, 2, and 6 are the same for any application
#There is a module in the Python standard library called BaseHTTPServer that does for us
#Actually for Python 3, we use the module http.server

from http.server import HTTPServer, BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    #Handle HTTP requests by returning a fixed 'page'.
    Page = '''\
<html>
<body>
    <p>
        Hello, web!
    </p>
</html>
'''
    # Handle a GET request
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(self.Page)))
        self.end_headers()
        self.wfile.write(bytes(self.Page,'utf-8'))
        #https://stackoverflow.com/questions/23264569/python-3-x-basehttpserver-or-http-server
        


#----------------------------------------------------------------------------
        
if __name__=="__main__":

    serverAddress = ('', 8080)
    server = HTTPServer(serverAddress,RequestHandler)
    server.serve_forever()

