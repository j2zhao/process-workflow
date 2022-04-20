"""
graph commits vs. number of lines (DONE)
TODO: Look at time of commits (DONE)
TODO: Look for percentage of errors (DONE)

TODO: Look for columns touched 
TODO: Look for popular functions
TODO: Look for number of print statements
TODO: Look for plot statements

"""
from distutils.log import error
import os
import re
import json
import matplotlib.pyplot as plt
from functools import cmp_to_key
import numpy as np

def get_commit_info(commit_list):
    num_commits = 0
    num_adds = 0
    for commit in commit_list:
        if commit['msg'].endswith('start'):
            num_commits += 1
            for diff in commit['diffs']:
                num_adds += len(diff['add'])
    return num_commits, num_adds

def get_commit_times(commit_list):
    times = []
    for commit in commit_list:
        if commit['msg'].endswith('start'):
            time = commit['date'].split(' ')
            month = time[1]
            day = time[2]
            times.append((month, day))
    return times

def compare(time1, time2):
    if time1[0] == 'Dec' and time2[0] == 'Nov':
        return 1
    elif time1[0] == 'Nov' and time2[0] == 'Dec':
        return -1
    else:
        if int(time1[1]) < int(time2[1]):
            return -1
        if int(time1[1]) == int(time2[1]):
            return 0
        if int(time1[1]) > int(time2[1]):
            return 1

def get_time_dots(timess, names):
    # get x-axis
    x_axis = names
    # get y_axis
    y_axis = []
    for times in timess:
        for time in times:
            if time not in y_axis:
                y_axis.append(time)
    y_axis.sort(key= cmp_to_key(compare))
    y_index = {}
    for i, y_a in enumerate(y_axis):
        y_index[y_a] = i
    y_axis2 = [ x[0] + ' ' + x[1] for x in y_axis]    
    # get samples
    X_g = []
    Y_g = []
    X_o = []
    Y_o = []
    X_r = []
    Y_r = []
    for i, times in enumerate(timess):
        y = i
        counts = {}
        for time in times:
            # x = y_index[time]
            # X.append(x)
            # Y.append(y)
            if time in counts:
                counts[time] +=1
            else:
                counts[time] = 1
        for time in counts:
            if counts[time] >50:
                x = y_index[time]
                X_r.append(x)
                Y_r.append(y)
            elif counts[time] > 10:
                x = y_index[time]
                X_o.append(x)
                Y_o.append(y)
            else:
                x = y_index[time]
                X_g.append(x)
                Y_g.append(y)
    return y_axis2, x_axis, X_g, Y_g, X_o, Y_o, X_r, Y_r

def get_error_info(commit_list):
    errors = 0
    success = 0
    for commit in commit_list:
        if commit['msg'].endswith('_end'):
            for diff in commit['diffs']:
                print('a')
                for a in diff['add']:
                    index1 = a.find("error_code: 0")
                    index2 = a.find("error_code: 1")
                    if index1 != -1:
                        errors += 1
                    if index2 != -1:
                        success += 1
            
    return errors, success



if __name__== "__main__":
    base_dir = "commit_obj"
    # errors = []
    # success = []
    names = []
    timess = []
    for dire in os.listdir(base_dir):
        names.append(dire.split('.')[0])
        full_dire = os.path.join(base_dir, dire)
        if dire.endswith(".json"):
            with open(full_dire, "rb") as f:
                commit_list = json.load(f)
                #er, suc = get_error_info(commit_list)
                times = get_commit_times(commit_list)
                # errors.append(er)
                # success.append(suc)
                timess.append(times)
                # a, b = get_commit_info(commit_list)
                # X.append(a)
                # y.append(b)
    x_axis, y_axis, X_g, Y_g, X_o, Y_o, X_r, Y_r = get_time_dots(timess, names)
    plt.scatter(X_g, Y_g, c='g')
    plt.scatter(X_o, Y_o, c='y')
    plt.scatter(X_r, Y_r, c='r')
    #plt.bar(np.asarray(range(len(errors))), errors, 0.4)
    #plt.bar(np.asarray(range(len(success))) + 0.40, success, 0.4)
    #plt.xticks(list(range(len(names))), names, rotation = 90)
    plt.yticks(list(range(len(y_axis))), y_axis)
    plt.xticks(list(range(len(x_axis))), x_axis)
    plt.show()