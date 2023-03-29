from .utils import join_openai_response

import logging
import openai


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')

class CodeAnalyzer:
    def __init__(self, api_key:str, model_engine:str="gpt-3.5-turbo"):
        if not isinstance(api_key, str):
            raise ValueError('API key should be str')
        
        openai.api_key = api_key
        self.model_engine = model_engine

    def find_bugs_in_code(self, code):
        prompt = f"What are the bugs in this code? Also find logical errors or issues with implementation\n\n{code}\n\nBugs:"
        messages = [{"role":"user", "content":prompt}]

        response = openai.ChatCompletion.create(
            model=self.model_engine,
            messages=messages,
        )

        return response
    
    def find_vulns_in_code(self, code):
        prompt = f"What are the vulnerabilities in this code? and how can we fix it?\n\n{code}"
        messages = [{"role":"user", "content":prompt}]

        response = openai.ChatCompletion.create(
            model=self.model_engine,
            messages=messages,
        )

        return response
    
    def analyze_code(self, file_name:str, code:str):
        logger.info(f'Analyzing code of file: {file_name}')

        bugs_response = self.find_bugs_in_code(code)
        vulns_response = self.find_vulns_in_code(code)


        # extract data 
        if bugs_response:
            bugs_response = join_openai_response(bugs_response)
        else:
            logging.warning(f'unable to join messsages for {file_name} bug response')

        if vulns_response:
            vulns_response = join_openai_response(vulns_response)
        else:
            logging.warning(f'unable to join messsages for {file_name} vulns response')

        analyzed_data = {
            "file_name": file_name,
            "bugs_response": bugs_response,
            "vulns_response": vulns_response,
        }

        return analyzed_data
