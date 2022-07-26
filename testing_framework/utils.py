from cProfile import run
from ctypes import sizeof
from distutils.log import error
from email import header
from importlib.resources import path
import requests
import json
from typing import Text, Any

from constants import *

class GithubToIB:

    def __validateConfig(self,config : Dict) -> bool:
        self.config = {}
        try:
            self.config['name'] = config['name']
            self.config['flow_path'] = config['flow_path']
            self.config['binary'] = config['binary']
            self.config['input'] = config['input']
            self.config['ib_token'] = config['ib_token']
            self.config['ib_environment'] = config['ib_environment']
            self.config['ib_base_api'] = config['ib_base_api']
            self.config['ib_path'] = config['ib_path']
            self.config['git_repo'] = config['git_repo']
            self.config['git_token'] = config['git_token']
            self.config['branch'] = config['branch']
            self.config['git_repo_owner'] = config['git_owner']
            self.config['ib_base'] = config['ib_base']
        except:
            return False
        

        finally:
            return True

    
    def __init__(self,config) -> None:
        if self.__validateConfig(config=config):
            self.OK = True
        else:
            self.OK = False

        print(self.config)
        self.EXT = 'zip'
        self.__file_content = ''
    



    def downloadGitRepo(self):
        
        headers = gitApiArgs(self.config['git_token'])

        url = f'https://api.github.com/repos/{self.config["git_repo_owner"]}/{self.config["git_repo"]}/{self.EXT}ball/{self.config["branch"]}'
        (status_code, content) = runRequest(GET = True,headers=headers,url=url)

        if status_code !=200:
            error_message = f'Downloading Git Repo Failed, \n {content}'

            return False, errorMessage(message = error_message)
        
        print('Git repo Successfully downloaded #1')
        self.__file_content = content
        return True,''



    def uploadGitRepoToIb(self):

        url = self.config['ib_base_api'] + self.config['ib_path']+'git_Repo.zip'


        api_args = dict(
            type='file',
            cursor=-1,
            if_exists='overwrite',
            mime_type='pdf'
            )

        headers = ibApiArgs(ib_token=self.config['ib_token'],api_args = api_args)
        (status_code, content) = runRequest(GET = False, url = url, headers=headers,data = self.__file_content)

        if status_code!=200:
            error_message = f'Uploading to IB Failed, \n {content}'

            return False, errorMessage(message= error_message)
        

        self.__path_on_ib = self.config['ib_path'] + '/git_Repo.zip'
        return True,''




    def createFile(self):
        
        url = self.config['ib_base_api'] + self.config['ib_path'] + 'git_Repo.zip'
        
        api_args = dict(
            type='file'
        )


        headers = ibApiArgs(ib_token=self.config['ib_token'],api_args=api_args)

        (status_code, content) = runRequest(GET = False, url=url, headers = headers)


        if status_code!=200:
            error_message = f'Creating and Saving of the File Failed \n{content}'

            return False, errorMessage(message= error_message)

        return True, ''
        


    def __ls(self, url,foldername):

        api_args = dict(
            type='folder',
            get_content=True,
            get_metadata=False,
            start_page_token=foldername
        )


        (status_code, content) = runRequest(GET = True, url = url, headers = ibApiArgs(ib_token=self.config['ib_token'], api_args =api_args))
        if status_code!=200:
            return None
        

        return content



    def unzipPackageAndPublish(self):
        url = self.config['ib_base_api'] + self.config['ib_path']+'unzip'


        data_dict = dict(
            zip_file = 'git_Repo.zip',
            destination = self.config['ib_path'] + 'unzip'
        )

        api_args = dict(
            type = 'folder'
        )
        
        ## Unzipping the Git Repo

        (status_code,content) = runRequest(GET = False,headers = ibApiArgs( self.config['ib_token'],api_args=api_args ), url = url, data = json.dumps(data_dict))

        if status_code !=200:
            error_message = f'Error in unzipping File on IB \n {content}'

            return False, errorMessage(message = error_message)
        


        ##Listing out the Files in the Repo

        file_names = self.__ls(url = self.config['ib_base_api'] + self.config['ib_path'] + '/unzip', foldername = '')
        if not file_names:
            return False, error_message( message = 'Error in File System Calls  ')


        file_names = json.loads(file_names)
        file = file_names['nodes'][0]

        url = self.config['ib_base'] + 'solution/create'

        body = {
            'content_folder':file['full_path'],
            'output_folder': self.config['ib_path'] + 'unzip'
        }

        headers = dict(
            Authorization =  f'Bearer {self.config["ib_token"]}'
        )


        (status_code, content) = runRequest(GET = False, url=url, headers = headers,data=json.dumps(body))

        if status_code!=200:
            error_message = f'Error in Packaging Solution \n{content}'

            return False, errorMessage(message = error_message)

        
        content = json.loads(content)

        body = dict(
            ibsolution_path = content['output_path']
        )


        url = self.config['ib_base'] + 'marketplace/publish'
        (status_code, content) = runRequest(GET = False, url = url, headers=headers, data = json.dumps(body))

        if status_code>299 or status_code<200:
            error_message = f'Error in Publishing the Solution to Marketplace \n{content}'

            return False, errorMessage(message=error_message)
        
        return True,''


        












