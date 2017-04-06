from github import Github

username = input('GitHub username: ')
password = input('GitHub password: ')
github_user = input('GitHub user/ organization: ')
github_repo = input('GitHub repository name: ')

g = Github(username, password)

repo = g.get_user(github_user).get_repo(github_repo)
pulls = repo.get_pulls('closed')

for pull in pulls:
    ref_string = 'heads/' + pull.head.ref
    try:
      ref = repo.get_git_ref(ref_string)
      ref.delete()
    except:
      print(ref_string + ' is not found')