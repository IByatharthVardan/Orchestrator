from constants import *
from utils import *
import sys
import json
import os 


def main():
    
    
    config = load_config(f'app_config.yaml')

    githubToIb = GithubToIB(config=config)

    if not githubToIb.OK:
        print('error')
        return
    successful, error = githubToIb.downloadGitRepo()
    
    if not successful:
        print(error)
        return
        
    print("Step 1 done")

    successful, error = githubToIb.createFile()
    if not successful:
        print(error)
        return
    
        
    print("Step 2 done")

    successful, error = githubToIb.uploadGitRepoToIb()
    if not successful:
        print(error)
        return
    
    print("Step 3 done")

    successful,error = githubToIb.unzipPackageAndPublish()
    if not successful:
        print(error)
        return

    print("Step 4 done ")

    print("The build is complete with every step completed")

if __name__=="__main__":
    main()

