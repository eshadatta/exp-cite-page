import argparse
import os
import click
from os.path import exists
import helpers.config_file as cf
import helpers.initialize_files as i
import helpers.process_json as pjson
import helpers.static_page_id as sp

s = sp.static_page_id()
default_config_filename = s.default_config_filename
default_pid_filename = s.default_pid_json_filename
default_id_types = s.default_id_types

@click.command()
@click.option('-r', '--repo-path', help="Path to repository containing the files", required=True, type=click.Path(exists=True, dir_okay=True, file_okay=False, readable=True, writable=True))
@click.option('-d', '--domain', help='Production domain of the content, for example: https://www.crossref.org/', required=True)

def set_args(repo_path, domain):
    click.echo(repo_path)
    click.echo(domain)
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

'''
def set_args2():
    s = sp.static_page_id()
    default_config_filename = s.default_config_filename
    default_pid_filename = s.default_pid_json_filename
    default_id_types = s.default_id_types
    """CLI"""
    parser = argparse.ArgumentParser(
                    description="Generate a permanent ID for a static site generator")
    parser.add_argument('-r', '--repo-path', help='Path to repository containing the files', type=lambda s:check_path(parser,s, "dir"), required=True)
    parser.add_argument('-d', '--domain', help='Production domain of the content, for example: https://www.crossref.org/', required=True)
    parser.add_argument('-p', '--pid-file-path', default = default_pid_filename, nargs='?', type=str, help='Path to json file where containing all the information associated with the files and their permanent IDs; relative to the repository root. If the file does not exist, a new file with the specified filename will be created. An existing file will not be overwritten', required=False)
    parser.add_argument('-cf', '--config-filename', nargs='?', type=str, default = default_config_filename, help='Filename for config init, has a default filename if none is specified. An existing file will be overwritten')
    parser.add_argument('-b', '--branch', help='Path to branch where the file is located. The default is the active branch of the repository')
    parser.add_argument('-id', '--id-type', choices=default_id_types, required=True)
    parser.add_argument('-dry', '--dry-run', help='Dry run to generate a permanent ID of a specified file', action='store_true')
    id_types, _ = parser.parse_known_args()
    # adding another argparse object to process sub commands associated with a specific argument
    idtype_parser = argparse.ArgumentParser(
        description="Generate a permanent ID for a static site generator", parents=[parser], add_help=False)
    if id_types.id_type == "doi":
        idtype_parser.add_argument('--doi-prefix', required=True, help="Add doi prefix string to this argument, example: --doi-prefix 'x.xxx'")
    args = idtype_parser.parse_args()
    print(args)
    return args
'''
    
def main():

    #id_type, args = set_args()
    args = set_args()
    c = cf.ConfigFile(args.repo_path, args.pid_file_path, args.config_filename)
    # get list of markdown files
    #file_list = c.get_file_list()
    doi_prefix = getattr(args, 'doi_prefix', None)
    c.create_config(args.id_type, args.domain, doi_prefix)
    #init_files = i.InitializeFiles(args.repo_path, file_list, args.pid_file_path)
    # initializing these files with a first tag of the first version
    #files = init_files.process_files()
    #json_file = pjson.ProcessJson(args.repo_path, c.pid_file, args.doi_prefix, args.domain)
    #json_file.initialize_pid_file(files)
if __name__ == "__main__":
    set_args()
    exit()