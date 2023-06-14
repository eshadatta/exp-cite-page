import argparse
import os
from os.path import exists
import helpers.config_file as cf
import helpers.initialize_files as i
import helpers.process_json as pjson
import helpers.static_page_id as sp

def check_path(parser, p, type='file'):
    path_types = ["file", "dir"]
    if not(type in path_types):
        raise parser.error(f"type: {type} must be one of these: {path_types}")
    if not(exists(p)):
        parser.error(f"{p} needs to exist")
    elif type == "file" and not(os.path.isfile(p)):
        parser.error(f"{p} needs to be a file")
    elif type == "dir" and not(os.path.isdir(p)):
        parser.error(f"{p} needs to be a directory")
    return os.path.normpath(p)

def set_args():
    s = sp.static_page_id()
    default_filename = s.default_config_filename
    """CLI"""
    parser = argparse.ArgumentParser(
                    description="Generate a permanent ID for a static site generator")
    # if json file does not exist, one will be created
    parser.add_argument('-p', '--pid-file-path', help='Path to json file where containing all the information associated with the files and their permanent IDs; relative to the repository root. If the file does not exist, a new file with the specified filename will be created', required=True)
    parser.add_argument('-cf', '--config-filename', nargs='?', type=str, default = default_filename, help='Filename for config init, has a default filename if none is specified')
    parser.add_argument('-b', '--branch', help='Path to branch where the file is located. The default is the active branch of the repository')
    parser.add_argument('-d', '--domain', help='Production domain of the content, for example: https://www.crossref.org/', required=True)
    #parser.add_argument('-sd', '--staging-domain', help='Staging domain of the content, for example: https://www.crossref.org/', required=True)
    #parser.add_argument('-ld', '--local-domain', help='Localhost domain of the content, for example: https://www.crossref.org/', required=True)
    parser.add_argument('-doi', '--doi', action='store_true', required=True, help='Identifier type, in this case doi')
    parser.add_argument('-dry', '--dry-run', help='Dry run to generate a permanent ID of a specified file', action='store_true')
    id_types, _ = parser.parse_known_args()
    idtype_parser = argparse.ArgumentParser(
        description="Generate a permanent ID for a static site generator", parents=[parser], add_help=False)
    idtype_parser.add_argument('--doi-prefix', required=id_types.doi, help="Add doi prefix string to this argument, example: --doi-prefix 'x.xxx'")
    args = idtype_parser.parse_args()
    return args
    
def main():
    set_args()
    exit()
    args = set_args()
    print(args.content)
    c = cf.ConfigFile(args.repo_path, args.content, args.pid_file_path, args.config_filename)
    # get list of markdown files
    file_list = c.get_file_list()
    c.create_config(args.doi_prefix, args.domain)
    init_files = i.InitializeFiles(args.repo_path, file_list, args.pid_file_path)
    # initializing these files with a first tag of the first version
    files = init_files.process_files()
    json_file = pjson.ProcessJson(args.repo_path, c.pid_file, args.doi_prefix, args.domain)
    json_file.initialize_pid_file(files)
if __name__ == "__main__":
    main()