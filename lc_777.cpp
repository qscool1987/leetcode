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
 思路：L只能往左移，R只能往右移，
 1.判断去掉X后，start和end剩下的字符串是否形式一样
 2.记录L和R的下标，判断对应位置的L和R的下标，必须保证
 对应位置的L start中 下标需要 大于等于 end
 对应位置的R start中 下标需要 小于等于 end
 ------------------->
 时间优化：遍历一遍
 空间优化：O(1)
 用两个下标分别从start和end的起始位置开始，以此往后遍历,遇到L或者R：
 1.判断是字符值是否相等
 2.判断下标关系是否满足
 依次判断直到遍历完成
 */
bool canTransform(string start, string end) {
    int i = 0, j = 0;
    while(i < start.length() && j < end.length()) {
        while(i < start.length() && start[i] == 'X') ++i;
        while(j < end.length() && end[j] == 'X') ++j;
        // 特别注意: 判断i，j是否已经到达结尾
        if (i >= start.length() || j >= end.length()) break;
        if (start[i] != end[j]) return false;
        if (start[i] == 'L' && i < j) return false;
        if (start[i] == 'R' && i > j) return false;
        ++i;
        ++j;
    }
    auto& s = i >= start.length() ? end : start;
    auto k = i >= start.length() ? j : i;
    for(; k < s.length(); ++k) {
        if (s[k] == 'L' || s[k] == 'R') return false;
    }
    return true;
}

int main(int argc, const char * argv[]) {
    string start = "RXXLRXRXL", end = "XRLXXRRLX";
    cout << canTransform(start, end) << endl;
    return 0;
}
