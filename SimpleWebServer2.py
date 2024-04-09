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
import time


class RequestHandler(BaseHTTPRequestHandler):
    #Handle HTTP requests by returning a fixed 'page'.
    Page = '''\
<html>
<body>
    <p>
        <font size="7">
            Hello, web!
        </font>
    </p>
    <table>
        <tr> <td>Header</td> <td>Value</td> </tr>
        <tr> <td>Date and Time</td> <td>{date_time}</td> </tr>
        <tr> <td>Client Host</td> <td>{client_host}</td> </tr>
        <tr> <td>Client Port</td> <td>{client_port}</td> </tr>
        <tr> <td>Command</td> <td>{command}</td> </tr>
        <tr> <td>Path</td> <td>{path}</td> </tr>
    </table>
</body>
</html>
'''
    # Handle a GET request
    def do_GET(self):
        page = self.create_page()
        self.send_page(page)

    def create_page(self):

        values = {
            'date_time'   : self.date_time_string(),
            'client_host' : self.client_address[0],
            'client_port' : self.client_address[1],
            'command'     : self.command,
            'path'        : self.path
        }
        page = self.Page.format(**values)
        return bytes(page, 'utf-8')
        #Need to convert to bytes
        #https://stackoverflow.com/questions/23264569/python-3-x-basehttpserver-or-http-server

    def send_page(self, page):
        #
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)


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

