from asyncio import run
from dotenv import load_dotenv
from github import Github
from sys import exit
from os import environ
from .chatgpt_api import CodeAnalyzer 
from .utils import filter_gh_file_data, create_gh_description


import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')


class PReviewer(CodeAnalyzer):
    def __init__(self, gh_access_token:str, repo:str, open_api_key: str, model_engine: str = "gpt-3.5-turbo"):
        super().__init__(open_api_key, model_engine)
        
        self._gh_access_token = gh_access_token
        self._repo = repo
        
    
    def review_pr(self, pr_num:int):
        # Authenticate with GitHub
        g = Github(self._gh_access_token)

        # # Get the repository and pull request [username/repo-name]
        repo = g.get_repo(self._repo)
        pr = repo.get_pull(pr_num)

        files_list = pr.get_files()

        code_snippets = []
        for file in files_list:
            file_name = file.filename
            code_snippets.append({
                'file_path':file_name,
                'changed_lines': filter_gh_file_data(file.patch.splitlines(), file_name)
            })
       
        analyzed_code_snippets = run(self.analyze_git_changes(code_snippets))
        logger.info('Analyzed PR commits.')
        
        description = create_gh_description(analyzed_code_snippets)

        # Update the pull request description
        pr.edit(body=description)
        logger.info('Updated Bugs and Vulns in PR description.')




if __name__ == '__main__':
    load_dotenv()

    # Replace with your GitHub access token
    OPEN_API_KEY = environ.get('OPENAI_API_KEY')
    ACCESS_TOKEN = environ.get('GH_ACCESS_TOKEN')
    REPO = environ.get('GH_REPO')
    PR_NUMBER = int(environ.get('GH_PR_NUMBER','-1'))

    should_exit = True
    if not OPEN_API_KEY:
        logger.error('OPEN_API_KEY env variable was not configured.')
    elif not ACCESS_TOKEN:
        logger.error('GH_ACCESS_TOKEN env variable was not configured.')
    elif not REPO:
        logger.error('GITHUB_REPO env variable was not configured.')
    elif PR_NUMBER == -1:
        logger.error('PR_NUMBER env variable was not configured.')
    else:
        should_exit = False
        logger.info('ENV vars found.')

    if should_exit:
        exit(-1)

    reviewer = PReviewer(ACCESS_TOKEN, REPO, OPEN_API_KEY)

    reviewer.review_pr(PR_NUMBER)
