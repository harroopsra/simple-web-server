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

#Serving Static Pages
#The obvious next step is to start serving pages from the disk instead of
# generating them on the fly. We'll start by rewriting do_GET:


from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import os

#https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python
#Hopefully I got this right
class ServerException(Exception):
    pass

class RequestHandler(BaseHTTPRequestHandler):
    #Handle HTTP requests by returning a fixed 'page'.

    Error_Page = """\
    <html>
    <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
    </body>
    </html>
    """

    # Handle a GET request
    def do_GET(self):
        try:
            # Figure out what exactly is being requested
            full_path = os.getcwd() + self.path

            #https://docs.python.org/3/tutorial/errors.html
            #https://docs.python.org/3/library/exceptions.html
            #https://docs.python.org/3/reference/simple_stmts.html#raise
            #To understand proper usage of "raise" and "Exception"

            # It doesn't exist...
            if not os.path.exists(full_path):
                raise ServerException("'{0}' not found".format(self.path))
            #https://stackoverflow.com/questions/273192/how-do-i-create-a-directory-and-any-missing-parent-directories

            #...it's a file...
            elif os.path.isfile(full_path):
                self.handle_file(full_path)
            
            #...it's something we don't handle
            else:
                raise ServerException("Unknown object '{0}'".format(self.path))

        except Exception as msg:
            self.handle_error(msg)


    def handle_file(self):
        #
        try:
            with open('full_path', 'rb') as reader:
                content = reader.read()
            self.send_content(content)
        
        except IOError as msg:
            msg = f"'{self.path}' cannot be read: {msg}"
            self.handle_error(msg)

    #Send actual content
    def send_content(self, content, status = 200):
        #
        content = bytes(content, 'utf-8')#Convert string to bytes before sending it out
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    # Handle unknown objects
    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content, status = 404)
#----------------------------------------------------------------------------
        
if __name__=="__main__":

    hostName = "localhost"
    hostPort = 8080

    serverAddress = (hostName, hostPort)
    server = HTTPServer(serverAddress,RequestHandler)

    try:
        print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    
    server.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))

