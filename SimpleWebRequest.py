#import requests
#submit a get request to get the testpage
#print out the status code: should be 200
#print content length
#finally print response.text

import requests
response = requests.get('http://aosabook.org/en/500L/web-server/testpage.html')
print ('status code:', response.status_code)
print ('content length:', response.headers['content-length'])
print (response.text)
