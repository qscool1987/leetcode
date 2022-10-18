import sys
import os


def stat_git_info(td, git_user):
    td = str(td)
    cmd = "cd /root/work/leetcode && git log --since='2022-09-25' --before='"
    cmd += td + "' --author='" 
    cmd += git_user +"' --pretty=tformat: --numstat"
    data = os.popen(cmd)
    add_l = 0
    add_t = 0
    lct = set()
    for line in data:
        items = line.strip().split("\t")
        add_l += int(items[0].strip())
        lct.add(items[2].strip())
    for t in lct:
        if t.startswith("lc_"):
            add_t += 1
    return add_l, add_t


if __name__ == '__main__':
    res = stat_git_info('2022-10-15', 'qscool1987')
    print(res)
