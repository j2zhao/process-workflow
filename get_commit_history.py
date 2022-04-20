import subprocess
import os

#git log -p
save_dir = "commit_history"
for dire in os.listdir("valid_repositories"):
    full_dire = os.path.join("valid_repositories", dire)
    if os.path.isdir(full_dire):
        print(full_dire)
        # os.chdir(full_dire)
        #output = subprocess.run(['git', '-C', full_dire, 'log', '-p', ], capture_output = True, shell=True)
        output = subprocess.run(['git -C ./' + full_dire + ' log -p'], capture_output = True, shell=True)
        #output = subprocess.run(['git', '--work-tree', full_dire +'/.git', '--git-dir',  ,'log', '-p'], capture_output = True, shell=True)
        #output = subprocess.run(['ls'], capture_output = True, shell=True)
        #print(output.stdout)
        # print(output.returncode)
        # print(output.stdout)
        #os.system("git status")
        #print('START')
        # os.chdir('..')
        # os.chdir('..')
        saved = os.path.join(save_dir, dire + '.log')
        with open(saved, 'wb') as f:
            f.write(output.stdout)
        print(output.returncode)

