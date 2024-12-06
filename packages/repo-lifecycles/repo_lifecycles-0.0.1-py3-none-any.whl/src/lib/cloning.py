import git 
import os
import shutil

def temp_clone(vcs_link, temp_location):
    os.makedirs(temp_location)
    repo_path = temp_location
    repo = git.Repo.clone_from(vcs_link, repo_path)
    print(f'Successfully Cloned {vcs_link}')
    return repo, repo_path

def delete_clone(temp_location):
    if os.path.exists(temp_location):
        shutil.rmtree(temp_location)
        print(f'{temp_location} has been deleted.')
        return 0
    else:
        print('No clone at location')
        return 1