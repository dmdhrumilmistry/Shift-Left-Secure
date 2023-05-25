from json import dumps
from textwrap import dedent
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')

def join_diffs(diffs:list):
    for file_change_data in diffs:
        changed_lines = '\n'.join(file_change_data.get('changed_lines',[]))
        file_change_data['changed_lines'] = changed_lines

    return diffs

def join_openai_response(response:dict):
    choices = response.get('choices')
    if not choices:
        return False
    
    message = ''
    for choice in choices:
        message += choice.get('message', {'content':''}).get('content','')

    return message

def json_to_file(file_path:str, data:dict or list):
    '''
    dumps json data to a file
    '''
    if not file_path.endswith('.json'):
        file_path += '.json'
    
    try:
        with open(file_path, 'w') as f:
            f.write(dumps(data))
            logger.info(f'responses stored in file: {file_path}')

    except Exception as e:
        logger.exception(e)

    return True

def analyzed_data_to_console(analyzed_data:list):
    if not isinstance(analyzed_data, list):
        logger.warning('analyzed_data should be a list')
        return 

    for code_analysis in analyzed_data:
        file_name = code_analysis.get('file_name')
        bugs_response = code_analysis.get('bugs_response')
        vulns_response = code_analysis.get('vulns_response')

        print('FILE NAME:\t', file_name,'\n')
        print('BUGS:\n',bugs_response, '\n')
        print('VULNS:\n', vulns_response, '\n')
        print('-'*20)

def filter_gh_file_data(lines:list, file_name:str):
    final_code = []
    section = 0
    for line in lines:
        if line.startswith("---") or line.startswith("+++"):
            continue
        elif line.startswith("@@"):
            section += 1
            final_code.append(f'\n>> Interpret below code as section {section} inside {file_name} file.')
        elif line.startswith("-"):
            continue
        elif line.startswith("+"):
            final_code.append(line[1:])
        else:
            final_code.append(line)
        
    return '\n'.join(final_code)


def analyzed_code_snippet_to_description(response:dict):
    '''
    converts analyzed code dict/json to github description
    '''
    return dedent(f'''## :file_folder: {response.get('file_name')}
    Bugs and Vulnerabilities can be found in below section along with their fixes.

    
    ### :bug: Bugs

    {response.get('bugs_response')}


    ### :lock: Vulns

    {response.get('vulns_response')}


    '''.strip())


def create_gh_description(analyzed_code_snippets:str):
    '''
    create github description from analyzed code snippets response from openai api
    '''
    description = ''
    for analyzed_code_snippet in analyzed_code_snippets:
        description += analyzed_code_snippet_to_description(analyzed_code_snippet)

    return description