import os
from os.path import exists
from pathlib import Path
import frontmatter
from frontmatter.default_handlers import YAMLHandler, JSONHandler, TOMLHandler

class InitializeFiles:
    def __init__(self, repo_path, content_file_paths, pid_file):
         self.repo_path = repo_path
         self.content_file_paths = content_file_paths
         self.pid_file = pid_file
         self.init_tag = 'x-version'
         self.init_version = '0.0.0'

    def write_content_file(self, file_path, markdown):
        try:
            with open(file_path, 'w') as m:
                m.write(frontmatter.dumps(markdown, handler=markdown.handler))
        except Exception as e:
            raise(f"ERROR: {e}")
        print(f"Initialized {file_path}")
        
            
    def initialize_content_file(self, file):
        try:
            markdown_file = frontmatter.load(file)
        except Exception as e:
            raise(f"ERROR: {e}")
        if not(self.init_tag in markdown_file.metadata):
            markdown_file.metadata[self.init_tag] = self.init_version
            self.write_content_file(file, markdown_file)
        
        return markdown_file
    
    def process_files(self):
        for p in self.content_file_paths:
            self.initialize_content_file(p)
    

        
        


    

