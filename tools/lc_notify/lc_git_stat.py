from curses.ascii import isdigit
import sys
import os

def is_vaild_digit(num_str):
    for ch in num_str:
        if ch < '0' or ch > '9':
            return False
    return True

def stat_git_info(td, git_user):
    td = str(td)
    cmd = "cd /root/work/leetcode && git pull origin master"
    os.system(cmd)
    cmd = "cd /root/work/leetcode && git log --since='2022-09-25' --before='"
    cmd += td + "' --author='" 
    cmd += git_user +"' --pretty=tformat: --numstat"
    data = os.popen(cmd)
    add_l = 0
    add_t = 0
    lct = set()
    for line in data:
        items = line.strip().split("\t")
        if len(items) < 3:
            continue
        num_str = items[0].strip()
        if not is_vaild_digit(num_str):
            continue
        add_l += int(num_str)
        lct.add(items[2].strip())
    for t in lct:
        if t.startswith("lc_"):
            add_t += 1
    return add_l, add_t


if __name__ == '__main__':
    res = stat_git_info('2022-10-18', 'qscool1987')
    print(res)
