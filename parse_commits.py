import os
import re

import json

def parse(file):
    commit_list = []
    commit_obj = {}
    diff_obj = {}
    msg = False
    for line in file:
        line = str(line, 'utf-8', errors='ignore').strip()
        if line.startswith('commit '):
            if len(commit_obj) != 0:
                if len(diff_obj) != 0:
                    commit_obj['diffs'].append(diff_obj)
                commit_list.append(commit_obj)
            commit_obj = {}
            commit_obj['diffs'] = []
        elif line.startswith("Author:"):
                commit_obj['author'] = line[8:]
        elif line.startswith("Date:"):
                commit_obj['date'] = line[8:]
                msg = True
        elif line == '':
            continue
        elif line.startswith("diff"):
            msg = False
            if len(diff_obj) != 0:
                commit_obj['diffs'].append(diff_obj)
            diff_obj = {}
            diff_obj['files'] = line
            diff_obj['add'] = []
            diff_obj['sub'] = []
        elif msg == True:
            commit_obj['msg'] = line.strip()
            msg == False
        elif line.startswith("---") or line.startswith("+++"):
            continue
        elif line.startswith("-"):
            diff_obj['sub'].append(line)
        elif line.startswith("+"):
            diff_obj['add'].append(line)
        else:
            continue
    if len(commit_obj) != 0:
        if len(diff_obj) != 0:
            commit_obj['diffs'].append(diff_obj)
        commit_list.append(commit_obj)
    return commit_list

# with open('commit_history/saranya-turimella.log', "rb") as f:
#     commit_list = parse(f)
#     for commit in commit_list:
#         print(commit['msg'])
#         print(commit['author'])
#         print(commit['date'])
#         print(len(commit['diffs']))

base_dir = "commit_history"
save_dir = "commit_obj"
for dire in os.listdir(base_dir):
    full_dire = os.path.join(base_dir, dire)
    if dire.endswith(".log"):
        print(dire)
        with open(full_dire, "rb") as f:
            commit_list = parse(f)
            dire2 = dire.split(".")[0]
            full_dire = os.path.join(save_dir, dire2 + ".json")
            with open(full_dire, 'w') as f2:
                json.dump(commit_list, f2)
        
