import json
import argparse
import os
from os.path import exists

def check_path(parser, p, type='dir'):
    path_types = ["file", "dir"]
    if type not in path_types:
        raise parser.error(f"type: {type} must be one of these: {path_types}")
    if not(exists(p)):
        parser.error(f"{p} needs to exist")
    elif type == "file" and not(os.path.isfile(p)):
        parser.error(f"{p} needs to be a file")
    elif type == "dir" and not(os.path.isdir(p)):
        parser.error(f"{p} needs to be a directory")
    return os.path.normpath(p)

def read_file(file):
    data = None
    try:
        with open(file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print("ERROR: ", e)
    return data

def set_args(argv):
    """CLI""" 
    parser = argparse.ArgumentParser(
                    description="Parses from external sources for additional deposit information. Currently, only accepts json files")
    parser.add_argument('-a', '--additional-info', required=True, type=lambda s:check_path(parser,s, "file"), help="Full path to existing json file containing additional information for deposit")
    parser.add_argument('-p', '--pid-file', nargs='?', type=lambda s:check_path(parser,s, "file"), help='Filename for config init, has a default filename if none is specified', required=True)
    args = parser.parse_args(argv)
    return args

def add_info_pid_file(records, pid):
    try:
        with open(pid, 'w') as f:
            json.dump(records, f)
    except Exception as e:
        print(e)

def get_orcid(bios, all_docs, additional_info):
    orcid_domain = "https://orcid.org/"
    listed_authors = list(bios.keys())
    unsubmitted_dois = list(filter(lambda x: not(x['doi']['submitted']), all_docs))
    for d in unsubmitted_dois:
        if "authors" in d.keys():
            for a in d['authors']:
                name = a['name']
                if name in listed_authors and 'orcid' in bios[name].keys():
                    a['ORCID'] = f"{orcid_domain}{bios[name]['orcid']}"
                elif name not in listed_authors:
                    raise ValueError(f"{name} does not exist in {additional_info}")
    return all_docs
    
def main(argv = None):
    args = set_args(argv)
    all_docs = read_file(args.pid_file)
    bios = read_file(args.additional_info)
    updated_info = get_orcid(bios, all_docs, args.additional_info)
    add_info_pid_file(updated_info, args.pid_file)
if __name__ == "__main__":
    main()
