import helper_url_generation.url_constructor as uc
from submit_files import create_xml_files, submit_files
import add_deposit_information
import check_doi_urls
import add_doi
import time
from datetime import datetime, timedelta
import yaml
import os
import json

class CrossrefSubmission:
    def __init__(self, repo, pid_file, config_filename, gen_pid_args, add_info_file, site_type="crossref"):
        self.site_types = ["crossref", "other"]
        self.repo = repo
        self.pid_file = pid_file
        self.config_filename = config_filename
        self.gen_pid_args = gen_pid_args
        self.add_info_file = add_info_file
        if site_type in self.site_types:
            self.site_type = site_type
        else:
            raise ValueError(f"Invalid website type choice: {site_type} entered. Valid website type choices are: {self.site_types}")
        
    def read_submission_file(self, file):
        data = None
        try:
            with open(file, 'r') as y:
                data = yaml.safe_load(y)
        except Exception as e:
                raise ValueError(f"ERROR: {e}")
        return data

    def read_pid_file(self):
        data = None
        try:
            with open(self.pid_file, 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(e)
        return data
    
    def url_gen(self):
        url_gen = ['--repo', self.repo, '--config-filename', self.config_filename]
        uc.main(url_gen)

    def add_additional_deposit_info(self):
        add_info_args = ['-p', self.pid_file, '-a', self.add_info_file]
        add_deposit_information.main(add_info_args)
        
    def generate_xml_submission(self):
        submission_info = self.gen_pid_args['submission_info']
        default_xml_filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_submission.xml"
        data = self.read_submission_file(submission_info)
        xml_file = os.path.join(self.repo,os.path.normpath(data['submission_path']), default_xml_filename)
        xml_args = ['-p', self.pid_file, '-b', data['batch_id'], '-dn', data['depositor'][0]['name'],'-de', data['depositor'][1]['email'], '-re', data['registrant'], '-f', xml_file]
        xml_created = create_xml_files.main(xml_args)
        return [xml_created, xml_file] 
    
    def submit_file(self, xml_file):
        env_vars = {'username': None, 'password': None, 'deposit_endpoint': None}
        err_msg = []
        for k in env_vars.keys():
            env_vars[k] = os.environ.get(k, None)
            if not(env_vars[k]):
                err_msg.append(k)
        if err_msg:
            raise NameError(f"Please declare the following variables as environment variables to allow for further processing: {err_msg}")
            
        submit_args = ['-f', xml_file, '-pid', self.pid_file, '-u', env_vars['username'], '-p', env_vars['password'], '-e', env_vars['deposit_endpoint']]
        submit_files.main(submit_args)
    
    def check_doi_status(self, start_time, time_length, sleep_seconds=30):
        print("Checking doi registration status")
        time.sleep(sleep_seconds)
        current_time=datetime.now()
        check_doi_args = ['--repo', self.repo, '-p', self.pid_file]
        status = check_doi_urls.main(check_doi_args)
        if (current_time < time_length) and status:
            self.check_doi_status(start_time, time_length)
        elif not(status):
            return status
        elif current_time >= time_length:
            return status

    def check_dois(self):
        start = datetime.now()
        end = start + timedelta(minutes=10)
        status = self.check_doi_status(start, end)
        return status
    
    def add_dois(self):
        add_doi_args = ['--repo', self.repo, '-f', self.pid_file]
        add_doi.main(add_doi_args)
    
    def check_for_null_urls(self):
        data = self.read_pid_file()
        no_urls = list(filter(lambda x: not(x['url']), data))
        return no_urls
    
    def create_crossref_workflow(self):
        self.add_additional_deposit_info()
        if self.site_type == "crossref":
            self.url_gen()
        dry_run = self.gen_pid_args['dry_run']
        no_urls = self.check_for_null_urls()
        if no_urls:
            raise ValueError(f"Submission process can not proceed. Please generate urls in {self.pid_file} for the following records: {no_urls}")
        else:
            xml_created, xml_file = self.generate_xml_submission()
        if dry_run:
            print(f"DRY RUN ended. Please check {self.pid_file} for information on the versioned files and {xml_file} for the xml deposit file")
        elif not(dry_run):
            if xml_created:
                self.submit_file(xml_file)
            doi_status = self.check_dois()
            if doi_status:
                print("Few records are not yet registered")
                print(doi_status)
            self.add_dois()
        


