import sys
from github import Github

username = input('GitHub username: ')
password = input('GitHub password: ')
github_user = input('GitHub user/ organization: ')
github_repo = input('GitHub repository name: ')
auto_delete = input('Automatic delete merged repo? (y/n): ')

def validate_bool_input(bool_input):
    if auto_delete is 'y' or auto_delete is 'n':
        return True
    else:
        print('automatic delete must be "y" or "n"!')
        return False

# validate auto delete input
if not validate_bool_input(auto_delete):
    sys.exit(1)

# create GitHub object
g = Github(username, password)

# define repo and pull requests
repo = g.get_user(github_user).get_repo(github_repo)
pulls = repo.get_pulls('closed').reversed

# check branch validity
def check(branch):
    try:
        ref = repo.get_git_ref(branch)
        return ref
    except:
        print('branch ' + branch + ' is not found')
        return None

# delete branch
def delete(ref):
    try:
        ref.delete()
        print(ref.ref + ' has been deleted')
    except:
        print(ref.ref + ' is not found')

for pull in pulls:
    ref_string = 'heads/' + pull.head.ref
    valid_branch = check(ref_string)
    if valid_branch is None:
        continue
    if auto_delete is 'y':
        delete(valid_branch)
    else:
        is_del = input('Do you want to delete branch ' + ref_string + '? (y/n): ')
        if is_del is 'y':
            delete(valid_branch)
