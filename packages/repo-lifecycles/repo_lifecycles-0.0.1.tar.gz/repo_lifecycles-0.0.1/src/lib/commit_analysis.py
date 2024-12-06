import git 
import os
import shutil
import primary_language

# parses through commits in reverse chronological order, hence the flipping of the terms for the arguments
def commit_analysis(repo, cutoff_date, start_date):
    print("Analyzing Commits...")
    commits_info = []
    for commit in repo.iter_commits():
        # if too far back, break 
        if commit.committed_datetime > start_date:
            continue
        if commit.committed_datetime < cutoff_date:
            break
        commit_info = {
            'commit_hash': commit.hexsha,
            'author_name': commit.author.name,
            'author_email': commit.author.email,
            'authored_date': commit.authored_datetime,
            'committer_name': commit.committer.name,
            'committer_email': commit.committer.email,
            'commit_date': commit.committed_datetime,
            'message': commit.message,
            'is_merge': len(commit.parents) > 1
        }
        # some more effort to get this information
        commit_info['branches'] = repo.git.branch("--contains", commit_info['commit_hash'])
        #diff information
        diffs = commit.diff(commit.parents[0] if commit.parents else git.NULL_TREE, create_patch=True)
        commit_info['diff_info'] = diff_analysis(diffs)
        #print(commit_info)
        commits_info.append(commit_info)
    return commits_info

def diff_analysis(diffs):
    diff_objects = []
    for diff in diffs:
        diff_info = {
            'lines_added': sum(1 for line in diff.diff.decode('utf-8').split('\n') if line.startswith('+') and not line.startswith('+++')),
            'lines_deleted': sum(1 for line in diff.diff.decode('utf-8').split('\n') if line.startswith('-') and not line.startswith('---')),
            'parent_filepath': diff.a_path,  
            'child_filepath': diff.b_path, 
            'change_type': diff.change_type,  
            'new_file': diff.new_file,  
            'deleted_file': diff.deleted_file, 
            'renamed_file': diff.renamed  
            #'diff': diff.diff.decode('utf-8')  
        }
        diff_objects.append(diff_info)
    return diff_objects