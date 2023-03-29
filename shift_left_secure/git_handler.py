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
        diffs = []

        diff_str = self._repo.git.diff('--no-renames', '-U0')
        
        # Split the diff string into lines
        diff_lines = diff_str.split('\n')


        # Initialize variables for the current file path and changed lines
        file_path = None
        changed_lines = []

        # Iterate over the lines in the diff and print the changed ones
        for line in diff_lines:
            if line.startswith('diff --git'):
                # If this is the start of a new file diff, print the changed lines for the previous file (if any)
                if file_path is not None:
                    # pass
                    # print('---', file_path, '---')
                    # for changed_line in changed_lines:
                        # print(changed_line)
                
                    diffs.append({
                        "file_path": file_path,
                        "changed_lines": changed_lines
                    })

                # Initialize variables for the new file diff
                file_path = line.split(' b/')[-1]
                changed_lines = []

            elif line.startswith('++'):
                pass

            elif line.startswith('+'):
                # If this is a changed line, add it to the list of changed lines for the current file
                changed_lines.append(line.strip().removeprefix('+'))
        
        # Print the changed lines for the last file
        if file_path is not None:
             diffs.append({
                "file_path": file_path,
                "changed_lines": changed_lines
            })
             
            # print('---', file_path, '---')
            # for changed_line in changed_lines:
                # print(changed_line)

        return diffs