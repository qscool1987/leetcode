import sys
import os
import settings
import datetime




def stat_git_info(td):
    git_infos = {}
    td = str(td)
    
    for u in settings.git_users:
        cmd = "cd /root/work/leetcode && git log --since='2022-09-25' --before='"
        cmd += td + "' --author='" 
        cmd += u +"' --pretty=tformat: --numstat"
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
        git_infos[u] = [add_l, add_t]
    return git_infos

def stat_git_info2(td):
    git_infos = []
    td = str(td)
    
    for u in settings.git_users:
        cmd = "cd /root/work/leetcode && git log --since='2022-09-25' --before='"
        cmd += td + "' --author='" 
        cmd += u +"' --pretty=tformat: --numstat"
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
        git_infos.append([u,str(add_l), str(add_t)])
    return git_infos


if __name__ == '__main__':
    res = stat_git_info('2022-10-15')
    print(res)
