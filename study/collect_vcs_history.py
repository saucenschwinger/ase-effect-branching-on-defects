import argparse
import os
from pydriller import Repository


def main(repo_name):

    gh_repo = f"https://github.com/apache/{repo_name}.git"
    repo_path = os.path.join("..", "data", "repositories", repo_name)
    if not os.path.exists(repo_path):
        print(f"Downloading {gh_repo} to {repo_path} ...", end="");
        repo = Repository(path_to_repo=gh_repo, clone_repo_to=repo_path)
    else:
        print(f"Loading {gh_repo} in {repo_path} ...", end="");
        repo = Repository(repo_path)

    print("done.\nTraversing repo");
    filename = os.path.join("..", "data", "vcs_records.csv")
    count = 0
    with open(filename, 'w') as commits_file:
        commits_file.write('hash,author_date\n')
        for commit in repo.traverse_commits():
            if commit.merge is True:
                #print(f"{commit.hash[:10]}")
                count += 1
                commits_file.write(commit.hash+","+str(commit.committer_date)+'\n')
        print('processed number of merges: ' + str(count))

if __name__ == "__main__":

    if False:
        msg = "Collect commits from Git."
        parser = argparse.ArgumentParser(description=msg)

        parser.add_argument("repo")
        args = parser.parse_args()

    main("camel")
