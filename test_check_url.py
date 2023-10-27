import os
import requests
import sys

def test_submission():
    file = "website-repo/xml_submission/20231009115857_submission.xml"
    username = os.environ['username']
    password = os.environ['password']
    deposit = os.environ['deposit']
    filename = os.path.basename(file)
    files = {'fname': (filename, open(file, 'rb'))}
    data = {'login_id':username, 'login_passwd': password, 'operation':'doMDUpload'}
    r = None
    try:
        r = requests.post(deposit, files=files, data = data)
    except Exception as e:
        print("ERROR: ", e)
    else:
        print(r.text)

def check_url():
    r = None
    try:
        r = requests.get("https://api.ror.org/organizations/ror.org/056x7d368")
    except Exception as e:
        print("ERROR: ", e)
    else:
        print(r.text)

def main():
    arg = int(sys.argv[1])
    print(type(arg))
    if arg == 1:
        check_url()
    elif arg == 2:
        test_submission()

if __name__ == "__main__":
    main()