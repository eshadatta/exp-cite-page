import click
import functools
import yaml
import sys
import re
import os
from os.path import exists
import helpers.static_page_id as sp
from datetime import datetime
import helpers.git_info as g
import helpers.config_file as cf
import helpers.utilities as u
import warnings
import id
import helper_url_generation.url_constructor as uc
from submit_files import create_xml_files, submit_files
import check_doi_urls
import add_doi
import time

def read_file(file):
    data = None
    try:
        with open(file, 'r') as y:
            data = yaml.safe_load(y)
    except Exception as e:
            raise ValueError(f"ERROR: {e}")
    return data

def add_dois(repo, pid_file):
    add_doi_args = ['--repo', repo, '-f', pid_file]
    add_doi.main(add_doi_args)

def check_dois(repo, pid_file):
    check_doi_args = ['--repo', repo, '-p', pid_file]
    status = check_doi_urls.main(check_doi_args)
    return status

def run_gen_id(config, args):
    content_args = ['--content']
    for i in config['content']:
        content_args.append(i)
    id_args = content_args + ['--repo', args['repo'], '--config-filename', args['conf_file']]
    if args['batch']:
        id_args.append('-b')
    id.main(id_args)

def submit_file(xml_file, pid_file, run_local):
    env_vars = {'username': None, 'password': None, 'deposit_endpoint': None}
    if run_local:
        err_msg = []
        for k in env_vars.keys():
            env_vars[k] = os.environ.get(k, None)
            print(f"Key: {k}, Value: {env_vars[k]}")
            if not(env_vars[k]):
                err_msg.append(k)
        if err_msg:
            raise NameError(f"Please declare the following variables as environment variables to allow for further processing: {err_msg}")
        
        submit_args = ['-f', xml_file, '-pid', pid_file, '-u', env_vars['username'], '-p', env_vars['password'], '-e', env_vars['deposit_endpoint']]
        print(submit_args)
        submit_files.main(submit_args)
            
def generate_xml_submission(pid_file, args):
    submission_info = args['submission_info']
    default_xml_filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_submission.xml"
    data = read_file(submission_info)
    xml_file = os.path.join(args['repo'],os.path.normpath(data['submission_path']), default_xml_filename)
    xml_args = ['-p', pid_file, '-b', data['batch_id'], '-dn', data['depositor'][0]['name'],'-de', data['depositor'][1]['email'], '-re', data['registrant'], '-f', xml_file]
    create_xml_files.main(xml_args)
    return xml_file

def process_config_pid_files(args):
    c = cf.ConfigFile(args['repo'], args['pid_file'], args['conf_file'], args['content'])
    c.create_config_yaml(args)
    c.create_pid_file()
   
def check_files(config_file, repo):
    if not(exists(config_file)):
        raise ValueError(f"{config_file} must exist for future processing. Please re-initialize script")
    config = u.read_all_config(config_file)
    pid_file = os.path.join(repo, config['pid_file'])
    if not(exists(pid_file)):
        raise ValueError(f"{pid_file} must exist for future processing. Please re-initialize script")
    return config, pid_file

@click.group()
def cli():
    pass

def common_options(f):
    options = [
        click.option("-r", "--repo", required=True, help='Path to repository containing the files', type=click.Path(exists=True, dir_okay=True, file_okay=False)),
        click.option("-cf", "--conf-file", help="Name of config yml file. This file will be saved and should exist at the root of the repository", default="config.yml", type=str)
    ]
    return functools.reduce(lambda x, opt: opt(x), options, f)

@cli.command()
@common_options
@click.option('-c', '--content', type=str, required=True, multiple=True, help="Examples: -c filepath1 -c filepath2; relative to the repository root")
@click.option('-d', '--domain', help='Production domain of the content, for example: https://www.crossref.org/', required=True, type=str)
@click.option('--doi-prefix', required=True, help="Add doi prefix string to this argument, example: --doi-prefix 'x.xxx'")
@click.option('--id-type', default="doi")
@click.option('-p', '--pid-file', default="pid.json", type=str, help="Json file that keeps track of the files, stored relative to the root of the repository")
def init(content, domain, doi_prefix, id_type, pid_file, **kwargs):
    kwargs['repo'] = os.path.normpath(kwargs['repo'])
    content_paths = list(map(lambda x: os.path.join(kwargs['repo'], os.path.normpath(x)), content))
    msg = [p for p in content_paths if not(exists(p))]
    if msg:
        raise ValueError(f"Paths provided: {msg} do not exist. Cannot process further")
    init_args = kwargs.copy()
    init_args.update({"content": list(content), "pid_file": pid_file, "domain": domain, "id_type": id_type, "doi_prefix": doi_prefix})
    process_config_pid_files(init_args)

@cli.command()
@common_options
@click.option('-b', '--batch', is_flag=True, show_default=True, default=False)
@click.option("-l", "--run-local", help="Running locally or in CI", is_flag=True, show_default=True, default=False)
@click.option('-st', '--sub-type', help='Type of submission protocol', type=click.Choice(["crossref", "custom"], case_sensitive=False), default="crossref")
@click.option('--info', help='Submission information, for crossref, please enter path to the submittor information yml file', type=click.Path(exists=True, dir_okay=False, file_okay=True, readable=True))
def gen_pid(batch, run_local, sub_type, info, **kwargs):
    kwargs['repo'] = os.path.normpath(kwargs['repo'])
    config_file = os.path.join(kwargs['repo'], kwargs['conf_file'])
    config, pid_file = check_files(config_file, kwargs['repo'])
    gen_pid_args = kwargs.copy()
    gen_pid_args.update({"batch": batch, "sub_type": sub_type, "submission_info": info})
    # generate ids
    run_gen_id(config, gen_pid_args)
    # if submission type is crossref, run the crossref submission workflow
    if sub_type == "crossref":
        url_gen = ['--repo', kwargs['repo'], '--config-filename', config_file]
        uc.main(url_gen)
        xml_file = generate_xml_submission(pid_file, gen_pid_args)
        submit_file(xml_file, pid_file, run_local)
        time.sleep(600)
        doi_status = check_dois(kwargs['repo'], pid_file)
        if doi_status:
            print(doi_status)
        add_dois(kwargs['repo'], pid_file)

if __name__ == "__main__":
    cli()
