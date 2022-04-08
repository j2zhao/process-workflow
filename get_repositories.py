import os


with open('valid_repositories/explore.txt', 'r') as f:
    repos = f.read().splitlines()

# https://github.com/CMSC-21800-Fall-2021/final-project-data-exploration-
# length -> 71
for repo in repos:
    name = repo[71:]
    dire = os.path.join('valid_repositories', name)
    if not os.path.isdir(dire):
        os.mkdir(dire)
    os.system('git clone {} {}'.format(repo, dire))