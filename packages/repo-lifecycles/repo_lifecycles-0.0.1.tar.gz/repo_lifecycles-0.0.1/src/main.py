import argparse
import sys
import os
import datetime
import pandas as pd
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib')))
from lib import cloning, commit_analysis
from lib import primary_language as pl

def repo_lifecycle(vcs_link, clone_location, from_date, to_date, to_save=False, to_csv=True):
    """
    Parameters:
        vcs_link (str): Version control system link of the repository.
        from_date (datetime): The start date for commit analysis.
        to_date (datetime): The end date for commit analysis.
        to_save (boolean): whether to save the project repository at the to_date; default FALSE
        to_csv (boolean): whether to save the commit information in a csv; default TRUE
    """
    try:
        #download the repository
        temp_repo, temp_repo_path = cloning.temp_clone(vcs_link, clone_location)
        project_name = vcs_link.split('/')[-1]
        project_owner = vcs_link.split('/')[-2]

        # collect data on prior commits
        commits_array = commit_analysis.commit_analysis(temp_repo, from_date, to_date)
        commits_df = pd.DataFrame.from_records(commits_array)
        if to_csv:
            commits_df.to_csv(f"{project_owner}_{project_name}_{from_date.strftime('%Y-%m-%d')}_to_{to_date.strftime('%Y-%m-%d')}.csv", index=False)

        if to_save:
            _commit = commits_df.iloc[0].to_dict()
            temp_repo_path = checkout_version(project_owner, project_name, _commit, temp_repo, temp_repo_path)
            print(temp_repo_path)

            # program/code analysis of the project at a specific point in time
            language_breakdown = pl.language_sizes(temp_repo_path) #breakdown is in terms of LoC
            print(language_breakdown)
            # TODO: here goes the linter/analysis implementation 
    except Exception as e:
        print(f"An error occurred: {e}")
    #clean up
    finally:
        if not to_save:
            delete = cloning.delete_clone(temp_repo_path)

def checkout_version(project_owner, project_name, commit, repo, repo_path):
    #update the repo with the correct checkout
    subprocess.run(['git', 'checkout', commit['commit_hash']], cwd=repo_path, check=True)
    new_repo_path = f"{commit['commit_date'].strftime('%Y-%m-%d')}_{project_owner}_{project_name}_{commit['commit_hash']}"
    os.rename(repo_path, new_repo_path)
    return new_repo_path

if __name__ == "__main__":
    #setting the defaults for the test run
    location = "tmp/"
    parser = argparse.ArgumentParser(description="repository search")
    parser.add_argument("repolink", help="The repository hosting")
    args = parser.parse_args()
    cst = datetime.timezone(datetime.timedelta(hours=-6))
    from_date = datetime.datetime(2024, 11, 10, 1, 52, 32, tzinfo=cst)
    to_date = datetime.datetime(2024, 11, 20, 1, 52, 32, tzinfo=cst)
    #getting the information for the search
    repo_lifecycle(args.repolink, location, from_date, to_date)