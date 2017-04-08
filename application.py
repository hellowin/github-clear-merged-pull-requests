import sys
from github import Github

username = input('GitHub username: ')
password = input('GitHub password: ')
github_user = input('GitHub user/ organization: ')
github_repo = input('GitHub repository name: ')
per_page = int(input('How many pulls fetched per page? (30) ') or "30")
page = int(input('Pick start page: (0) ') or "0")
auto_delete = input('Automatic delete merged repo? (y/n): ')

def validate_bool_input(bool_input):
    if auto_delete is "y" or auto_delete is "n":
        return True
    else:
        print('automatic delete must be "y" or "n"!')
        return False

# check branch validity
def check(branch):
    try:
        ref = repo.get_git_ref(branch)
        return ref
    except:
        print("branch " + branch + " is not found")
        return None

# delete branch
def delete(ref):
    try:
        ref.delete()
        print(ref.ref + " has been deleted")
    except:
        print(ref.ref + " is not found")

# validate auto delete input
if not validate_bool_input(auto_delete):
    sys.exit(1)

# create GitHub object
g = Github(username, password, per_page=per_page)

# define repo and pull requests
print("get repo from {}/{}".format(github_user, github_repo))
repo = g.get_user(github_user).get_repo(github_repo)

while True:
    print("get pull requests from page {}".format(page))
    pulls = repo.get_pulls("closed").get_page(page)

    print("get head refs")
    refs = ["heads/{}".format(pull.head.ref) for pull in pulls]

    # break the loop
    if len(refs) is 0:
        print("page {} is empty, done cleaning".format(page))
        break

    print("validate {} branche(s)".format(len(refs)))
    check_valids = [check(ref) for ref in refs]

    print("remove invalid branche(s)")
    valids = [val for val in check_valids if val is not None]

    print("perform deletion for {} branche(s)".format(len(valids)))
    for valid in valids:
        if auto_delete is "y":
            delete(valid)
        else:
            is_del = input("Do you want to delete branch " + valid.ref + "? (y/n): ")
            if is_del is "y":
                delete(valid)
    
    page += 1
