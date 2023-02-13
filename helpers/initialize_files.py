import os
from os.path import exists
from pathlib import Path
import frontmatter
from frontmatter.default_handlers import YAMLHandler, JSONHandler, TOMLHandler
from . import git_info

class InitializeFiles:
    def __init__(self, repo_path, content_file_paths, pid_file):
         self.repo_path = repo_path
         self.content_file_paths = content_file_paths
         self.pid_file = pid_file
         self.init_tag = 'x-version'
         self.init_version = '0.0.0'
         self.g = git_info.GitInfo(self.repo_path)

    def write_content_file(self, file_path, markdown):
        initialized = False
        try:
            with open(file_path, 'w') as m:
                m.write(frontmatter.dumps(markdown, handler=markdown.handler))
        except Exception as e:
            raise(f"ERROR: {e}")
        initialized = True
        return initialized
        
            
    def initialize_content_file(self, file):
        initialized = False
        try:
            markdown_file = frontmatter.load(file)
        except Exception as e:
            raise(f"ERROR: {e}")
        if not(self.init_tag in markdown_file.metadata):
            markdown_file.metadata[self.init_tag] = self.init_version
            initialized = self.write_content_file(file, markdown_file)
        
        return initialized
    
    def check_git_info(self, file):
        is_tracked = self.g.tracked(file)
        if not(is_tracked):
            self.g.git_add_file(file)
        committed = self.g.check_file_status(file)
        if not(committed):
                self.g.git_commit_file(file)
        [file_commit_id, git_hash] = self.g.git_commit_id(self.g.active_branch, file)
        return [file_commit_id, git_hash]

    def gen_initialized_file_info(self, file):
        [file_commit_id, git_hash] = self.check_git_info(file)
        utc_datetime = self.g.commit_date(file_commit_id)
        return [file_commit_id, git_hash, utc_datetime]

    def process_files(self):
        # currently, this will only check to see files that have x-version and need to be committed
        # also needs to check if there are initialized things that are not committed
        files = []
        file_git_info = []
        for p in self.content_file_paths:
            init = self.initialize_content_file(p)
            if init:
                files.append(p)
        
        for f in files:
            [file_commit_id, git_hash, utc_datetime] = self.gen_initialized_file_info(f)
            info = {"file_commit_id": file_commit_id, "file_hash": git_hash, "utc_commit_date": utc_datetime, "file": f.split(self.repo_path+"/")[1]}
            file_git_info.append(info)

        return file_git_info

    

        
        


    

