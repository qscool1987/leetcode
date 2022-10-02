//
//  main.cpp
//  cppcode
//
//  Created by 默认 on 2022/9/6.
//

#include <iostream>
#include <vector>
#include <stack>
#include <queue>
#include <algorithm>
#include <list>
#include <map>
#include <unordered_map>
#include <set>
#include <unordered_set>
#include <cmath>
using namespace std;

/*
 leetcode https://leetcode.cn/problems/check-if-binary-string-has-at-most-one-segment-of-ones/
 思路：滑动窗口，统计连续1出现的次数，当统计到次数 > 1 或者到达字符串结尾时 退出
 */

bool checkOnesSegment(string s) {
    int l = 0, r = 0, cnt = 0;
    while(r < s.length() && cnt <= 1) {
        // 处理连续0
        while(r < s.length() && s[r] == '0') ++r;
        l = r;
        // 处理连续1
        while(r < s.length() && s[r] == '1') ++r;
        // 特别注意 r > l
        if (r - l > 0) ++cnt;
    }
    return cnt <= 1;
}

int main(int argc, const char * argv[]) {
    string s = "1001";
    cout << checkOnesSegment(s) << endl;
    return 0;
}
