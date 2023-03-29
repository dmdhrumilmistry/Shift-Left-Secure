from git.repo import Repo
from os.path import isdir

import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')


class GitDirectoryNotFound(Exception):
    pass

class GitHandler:
    def __init__(self, repo_dir:str) -> None:
        '''
        initialize git repo directory for getting project information
        '''

        if not isdir(repo_dir):
            msg = f"{repo_dir} directory not found."
            logger.exception(msg)
            raise GitDirectoryNotFound(msg)
        
        self._repo_dir = repo_dir
        self._repo = Repo(repo_dir)



    def get_diff(self, commit_hash:str=None):
        '''
        get git difference between previous 
        '''
        hcommit = self._repo.head.commit
        # diffs = hcommit.diff(commit_hash)

        # for diff in diffs:
        #     # If the diff is not for a file, skip it
        #     if not diff.a_blob:
        #         continue
            
        #     # Get the file path and contents
        #     file_path = diff.a_blob.path
        #     file_contents = diff.a_blob.data_stream.read().decode('utf-8')
            
        #     # Print the file path and contents
        #     print('---', file_path, '---')
        #     # print(file_contents)
        #     for hunk in diff.hunks:
        #         # Iterate over the lines in the hunk and print the changed ones
        #         for line in hunk.lines:
        #             if line.startswith('+') or line.startswith('-'):
        #                 print(line.strip())

        # 
        # changed_files = [item.a_path for item in hcommit.diff(None)]
        # print(changed_files)
        
        for item in hcommit.diff(None):
            # Get the file path and diff text
            path = item.a_path
            diff_text = item.diff

            # Print the file path
            print(f'Changes for file: {path}')

            # Print the diff text
            print(diff_text)

