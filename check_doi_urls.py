import argparse
import os
from os.path import exists
import json
import requests
import sys
from git import Repo

def check_path(parser, p, type="file"):
    if not(exists(p)):
        parser.error(f"{p} needs to exist")
    elif type == "file" and not(os.path.isfile(p)):
        parser.error(f"{p} needs to be a file")
    return os.path.normpath(p)

def set_args(argv):
    """CLI"""
    parser = argparse.ArgumentParser(
                    description="Check URLs")
    parser.add_argument('-r', '--repo-path', help='Path to repository containing the files', type=lambda s:check_path(parser,s, "dir"), required=True)
    parser.add_argument('-p', '--pid-file',  help='Filename for pid files that contain the urls', type=lambda s:check_path(parser,s), required=True)
   
    args = parser.parse_args(argv)
    return args

def read_pid_file(file):
    records = None
    try:
        with open(file, "r") as f:
            records = json.load(f)
    except Exception as e:
        print (f"ERROR: {e}")
    return records

def update_pid_file(records, pidfile):
    try:
        with open(pidfile, 'w') as out:
            json.dump(records, out)
    except Exception as e:
        print(e)

def check_urls(pidfile):
    records = read_pid_file(pidfile)
    bad_url_status = {}
    for r in records:
        if not(r['doi']['registered']) and r['doi']['value']:
            request = None
            doi_url = r['doi']['value']
            non_perm_url = r['url']
            try:
                request = requests.get(doi_url, allow_redirects=False)
                if request.ok: 
                    if (300 <= request.status_code <= 308):
                        location = request.headers.get('location', None)
                        if location and location == non_perm_url:
                            r['doi']['registered'] = True
                        elif location != non_perm_url:
                            bad_url_status[r['file']] = {"url": doi_url, "status": request.status_code, "reason": f"DOI pointing to {location}should equal {r['url']}"}
                        else:
                            bad_url_status[r['file']] = {"url": doi_url, "status": request.status_code, "reason": f"location must exist"}
                    else:
                        bad_url_status[r['file']] = {"url": doi_url, "status": request.status_code, "reason": f"request status code should be in the 3xx range of status codes. Please inquire"}
                else:
                    bad_url_status[r['file']] = {"url": doi_url, "status": request.status_code, "reason": request.reason}
            except Exception as e:
                print (f"Error occurred on request: {e}")
    return records, bad_url_status

# this script can be run after the files are initialized
def main(argv = None):
    args = set_args(argv)
    print("Checking DOI URLs")
    records, bad_url_status = check_urls(args.pid_file)
    update_pid_file(records, args.pid_file)
    return bad_url_status

if __name__ == "__main__":
    main()