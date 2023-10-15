import requests
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder
username = os.environ['username']
password = os.environ['password']
url = "https://test.crossref.org/servlet/deposit"
file = "/Users/eshadatta/static-page-id-generator/test1.xml"
data = {'login_id':username, 'login_passwd': password, 'operation':'doMDUpload'}
files = {'fname': ('test1.xml', open(file, 'rb'))}
r = requests.post(url, files=files, data = data)
r.text

correct_result = '\n\n\n\n<html>\n<head><title>SUCCESS</title>\n</head>\n<body>\n<h2>SUCCESS</h2>\n<p>Your batch submission was successfully received.</p>\n</body>\n</html>\n'

