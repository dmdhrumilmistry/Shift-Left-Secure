from json import dumps


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

# def json_to_file(file_name:str):
#     '''
#     dumps json data to 
#     '''