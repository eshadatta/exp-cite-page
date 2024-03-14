import argparse
import os
from os.path import exists
import requests
import json
import xml.etree.cElementTree as ET

def check_path(parser, p, type=None):
    if not(exists(p)):
        parser.error(f"{p} needs to exist")
    elif type == "file" and not(os.path.isfile(p)):
        parser.error(f"{p} needs to be a file")
    return os.path.normpath(p)

def set_args(argv):
    parser = argparse.ArgumentParser(
                    description="Submit files for DOI registration")
    parser.add_argument('-f', '--xml-file-name', help='Path and name for xml file to be submitted', type=lambda p:check_path(parser,p, 'file'), required=True)
    parser.add_argument('-pid', '--pid-file-name', help='Path and name for pid file to be submitted', type=lambda p:check_path(parser,p, 'file'), required=True)
    parser.add_argument('-u', '--username', help='username and role for deposit', required=True, type=str)
    parser.add_argument('-p', '--password', help='password for deposit', required=True, type=str)
    parser.add_argument('-e', '--deposit-endpoint', help='deposit endpoint', required=True)
    args = parser.parse_args(argv)
    return args

def get_doi_submission_status(pid):
    records = None
    try:
        with open(pid, 'r') as f:
            records = json.load(f)
    except Exception as e:
        print(e)
    return records

def record_submission_status(records, pid):
    try:
        with open(pid, 'w') as f:
            json.dump(records, f)
    except Exception as e:
        print(e)


def get_submitted_dois(xml):
    ns = '{http://www.crossref.org/schema/5.3.0}'
    doi_tag = f'{ns}doi'
    tree = ET.parse(xml)
    root = tree.getroot()
    ids = [i.text.split('/')[1] for i in root.iter(doi_tag)]
    return ids

def process_submitted_dois(pid, xml):
    records = get_doi_submission_status(pid)
    ids = get_submitted_dois(xml)
    doi_url_domain =  "https://doi.org/"
    for r in records: 
        if r['current_id'] in ids:
            r['doi']['submitted'] = True
            r['doi']['value'] = doi_url_domain + r['doi_prefix'] + "/" + r['current_id']
    record_submission_status(records, pid)
    
def submit_file(args):
    username = args.username
    password = args.password
    file = args.xml_file_name
    filename = os.path.basename(file)
    data = {'login_id':username, 'login_passwd': password, 'operation':'doMDUpload'}
    files = {'fname': (filename, open(file, 'rb'))}
    r = None
    doi_submitted = None
    url = args.deposit_endpoint
    try:
        r = requests.post(url, files=files, data = data)
    except Exception as e:
        print(e)
    if r:
        if 'success' in r.text:
            doi_submitted = True
            print("Submission was successful")
        else:
            print('Unsuccessful submission')
            print(r.text)
    return doi_submitted

def main(argv = None):
    args = set_args(argv)
    print("Submitting file: ", args.xml_file_name)
    doi_submitted = submit_file(args)
    if doi_submitted:
        print(f"Updating doi status in {args.pid_file_name}")
        process_submitted_dois(args.pid_file_name, args.xml_file_name)
        print("DOI status updated")
if __name__ == "__main__":
    main()