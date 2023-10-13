#!/bin/bash
set -x
cd /root/work/leetcode/tools/lc_notify/
python3 lc_notify.py &
mysqldump -uroot -pqscool --databases leetcode > ./data/leetcode.sql
