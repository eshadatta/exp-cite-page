import argparse
import os
from os.path import exists
import json
import requests
import sys

def check_path(parser, p):
    if not(exists(p)):
        parser.error(f"{p} needs to exist")
    elif type == "file" and not(os.path.isfile(p)):
        parser.error(f"{p} needs to be a file")
    return os.path.normpath(p)

def set_args():
    """CLI"""
    parser = argparse.ArgumentParser(
                    description="Check URLs")
    parser.add_argument('-p', '--pid-file',  help='Filename for pid files that contain the urls', type=lambda s:check_path(parser,s), required=True)
   
    args = parser.parse_args()
    return args

def read_pid_file(file):
    records = None
    try:
        with open(file, "r") as f:
            records = json.load(f)
    except Exception as e:
        raise (f"ERROR: {e}")
    return records

def check_urls(pidfile):
    records = read_pid_file(pidfile)
    bad_url_status = {}
    for r in records:
        request = None
        if r['url']:
            try:
                request = requests.get(r['url'])
                if not(request.ok):
                    bad_url_status[r['file']] = {"url": r['url'], "status": request.status_code, "reason": request.reason}
            except Exception as e:
                raise (f"Error occurred on request: {e}")
    return bad_url_status


# this script can be run after the files are initialized
def main():
    args = set_args()
    bad_url_status = check_urls(args.pid_file)
    if bad_url_status:
        print(f"ERRORS Found: ")
        for file, info in bad_url_status.items():
            print(f"For {file}: {info}")
            sys.exit(1)

if __name__ == "__main__":
    main()