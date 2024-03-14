import click
import functools
import yaml
import os
from os.path import exists
import helpers.static_page_id as sp
from datetime import datetime
import helpers.config_file as cf
import helpers.utilities as u
import id
import helper_url_generation.url_constructor as uc
from submit_files import create_xml_files, submit_files
import check_doi_urls
import add_doi
import time
from datetime import datetime, timedelta
from submission_workflow import crossref

def read_file(file):
    data = None
    try:
        with open(file, 'r') as y:
            data = yaml.safe_load(y)
    except Exception as e:
            raise ValueError(f"ERROR: {e}")
    return data

def run_gen_id(config, args):
    content_args = ['--content']
    for i in config['content']:
        content_args.append(i)
    id_args = content_args + ['--repo', args['repo'], '--config-filename', args['conf_file']]
    if args['batch']:
        id_args.append('-b')
    print("IN ID: ")
    id.main(id_args)
            
def generate_xml_submission(pid_file, args):
    submission_info = args['submission_info']
    default_xml_filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_submission.xml"
    data = read_file(submission_info)
    xml_file = os.path.join(args['repo'],os.path.normpath(data['submission_path']), default_xml_filename)
    xml_args = ['-p', pid_file, '-b', data['batch_id'], '-dn', data['depositor'][0]['name'],'-de', data['depositor'][1]['email'], '-re', data['registrant'], '-f', xml_file]
    xml_created = create_xml_files.main(xml_args)
    return [xml_created, xml_file]

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
@click.option('-c', '--content', type=str, multiple=True, default = ["."], help="Examples: -c filepath1 -c filepath2; relative to the repository root")
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
@click.option('-dry', '--dry-run', help='Run script upto deposit but do not deposit. Creates PIDs for files and stops', is_flag=True, show_default=True, default=False)
@click.option('-st', '--sub-type', help='Type of submission protocol', type=click.Choice(["crossref", "custom"], case_sensitive=False), default="crossref")
@click.option('--info', help='Submission information, for crossref, please enter path to the submittor information yml file', type=click.Path(exists=True, dir_okay=False, file_okay=True, readable=True))
def gen_pid(batch, dry_run, sub_type, info, **kwargs):
    kwargs['repo'] = os.path.normpath(kwargs['repo'])
    config_file = os.path.join(kwargs['repo'], kwargs['conf_file'])
    config, pid_file = check_files(config_file, kwargs['repo'])
    gen_pid_args = kwargs.copy()
    gen_pid_args.update({"batch": batch, "dry_run": dry_run, "sub_type": sub_type, "submission_info": info})
    # generate ids
    if dry_run:
        print("Running in DRY RUN mode")
        print("In DRY RUN mode, script will generate: ")
        print("1. unique identifier for each file with a x-version tag in frontmatter")
        print("2. URL based on website logic. Currently hardcoded for the Crossref website")
        print("3. If a Crossref submission, will create a xml deposit file and save it to the specified directory")
        print("4. Script will NOT deposit the file")
        print("4. Script will NOT register a DOI")
        print("4. Script will NOT add the DOI back to the file")
    run_gen_id(config, gen_pid_args)
    # if submission type is crossref, run the crossref submission workflow
    if sub_type == "crossref":
        additional_info_file = "data/team/biographies.json"
        full_path_add_info_file = os.path.join(os.path.normpath(kwargs['repo']), os.path.normpath(additional_info_file))
        cr_workflow = crossref.CrossrefSubmission(kwargs['repo'], pid_file, config_file, gen_pid_args, full_path_add_info_file, site_type="crossref")
        cr_workflow.create_crossref_workflow()

if __name__ == "__main__":
    cli()
