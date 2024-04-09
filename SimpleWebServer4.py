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

#Listing Directories
#Display a listing of a directory's contents when the path in the URL is a directory rather than a file
#Check for a file named index.html
#If not present, then display the directory's contents

from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import os

#https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python
#To declare a custom exception
class ServerException(Exception):
    pass

#The 5 different diffrent Cases
class case_no_file(object):
    #File or directory does not exist
    def test(self, handler):
        return not os.path.exists(handler.full_path)
    
    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))
    
class case_existing_file(object):
    #File exists
    def test(self, handler):
        return os.path.isfile(handler.full_path)
    
    def act(self, handler):
        handler.handle_file(handler.full_path)
    
class case_always_fail(object):
    #Base case if nothing else worked
    def test(self, handler):
        return True
    
    def act(self, handler):
        raise ServerException("Unknown object '{0}'".format(handler.path))

class case_directory_index_file(object):
    #Case where index file is in the directory
    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')
    
    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               os.path.isfile(self.index_path(handler))
    
    def act(self, handler):
        handler.handle_file(self.index_path(handler))


class case_directory_no_index_file(object):
    #Index file is not in the directory

    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')
    
    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               not os.path.isfile(self.index_path(handler))

    def act(self, handler):
        handler.list_dir(handler.full_path)

#Sixth file
class case_cgi_file(object):
    '''Something runnable.'''

    def test(self, handler):
        return os.path.isfile(handler.full_path) and \
               handler.full_path.endswith('.py')

    def act(self, handler):
        handler.run_cgi(handler.full_path)

class RequestHandler(BaseHTTPRequestHandler):

    #If the requested path maps to a file, that file is served.
    #If anything goes wrong, an error page is constructed. 

    Cases = [case_no_file(),
             case_existing_file(),
             case_directory_index_file(),
             case_always_fail()]
    
    
    # How to display a directory listing.
    Listing_Page = '''\
        <html>
        <body>
        <ul>
        {0}
        </ul>
        </body>
        </html>
        '''
    
    #We should have ideally included this in the act section of the case section but since we wrote ourselves into a corner, this will do
    #List in the listing page
    def list_dir(self, full_path):
        try:
            entries = os.listdir(full_path)
            bullets = ['<li>{0}</li>'.format(e) \
                       for e in entries if not e.startswith('')]
            page = self.Listing_Page.format('\n'.join(bullets))
            self.send_content(page)
        except OSError as msg:
            msg = "'{0}' cannot be listed: {1}".format(self.path, msg)
            self.handle_error(msg)

    #Idea is simple
    #1. Run the program in a subprocess.
    #2. Capture whatever that subprocess sends to standard output.
    #3. Send that back to the client that made the request.
    def run_cgi(self, full_path):
        cmd = "python " + full_path
        child_stdin, child_stdout = os.popen2(cmd)
        child_stdin.close()
        data = child_stdout.read()
        child_stdout.close()
        self.send_content(data)
    
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
            self.full_path = os.getcwd() + self.path
            
            #Handle it
            for case in self.Cases:
                handler = case()
                if handler.test(self):
                    handler.act(self)
                    break
        
        #Stays the same, just error-handling
        except Exception as msg:
            self.handle_error(msg)


    def handle_file(self):
        #Check if user entered correctly
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

