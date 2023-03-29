from json import dumps
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

def json_to_file(file_path:str, data:dict):
    '''
    dumps json data to a file
    '''
    if not isinstance(data, dict):
        return False
    
    if not file_path.endswith('.json'):
        file_path += '.json'
    
    try:
        with open(file_path, 'w') as f:
            f.write(dumps(data))
            logger.info(f'responses stored in file: {file_path}')

    except Exception as e:
        logger.exception(e)

    return True