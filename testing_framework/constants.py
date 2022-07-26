from cgitb import text
from email import header
import json
from tokenize import Number
from typing import Any, Dict, Text
import requests
import yaml
from yaml.loader import SafeLoader


def errorMessage(message) -> Text:
    return f'Test Runner Failed with the following response \n{message} \n :('

def ibApiArgs(ib_token,api_args) -> Dict[Text,Text]:

    return {
        'Authorization': 'Bearer {0}'.format(ib_token),
        'Instabase-API-Args': json.dumps(api_args)
    }

def gitApiArgs(git_token) -> Dict[Text,Text]:
    return {
        "Authorization" : f'token {git_token}',
        "Accept": 'application/vnd.github.v3+json'
    }

def runRequest(GET,headers, url,data = ''):

    print(f'url : {url}')
    print(f'headers : {headers}')
    if GET:
        if data != '':
            response = requests.get(url, headers=headers,data = data)
        else:
            response = requests.get(url,headers = headers)
        return (response.status_code, response.content)    
    
    if data != '':
        response = requests.post(url, headers=headers,data = data)
    else:
        response = requests.post(url,headers = headers)
    
    return (response.status_code, response.content)

     

def load_config(config_file_loc):
    with open(config_file_loc) as f:
        data = yaml.load(f, Loader = SafeLoader)
    return data


def flowApiArgs(input_dir,flow_path):
    return dict(
        input_dir = input_dir,
        ibflow_path = flow_path,
        output_has_run_id = False,
        delete_out_dir = True,
        log_to_timeline = True,
        enable_ibdoc = False,
        compile_and_run_as_binary = True
    )



    