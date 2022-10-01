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
 */
bool canTransform(string start, string end) {
    vector<int> sl, sr, el, er;
    string ss, se;
    // 分别存储L，R下标和去掉X后的字串
    for(int i = 0; i < start.length(); ++i) {
        if (start[i] == 'L') {
            ss.push_back(start[i]);
            sl.push_back(i);
        } else if (start[i] == 'R') {
            ss.push_back(start[i]);
            sr.push_back(i);
        }
        if (end[i] == 'L') {
            se.push_back(end[i]);
            el.push_back(i);
        } else if (end[i] == 'R') {
            se.push_back(end[i]);
            er.push_back(i);
        }
    }
    // 判断去掉X和都字串是否相等
    if (ss != se) return false;
    // 判断对应位置L和R的关系
    for(int i = 0; i < sl.size(); ++i) {
        if (sl[i] < el[i]) return false;
    }
    for(int i = 0; i < sr.size(); ++i) {
        if (sr[i] > er[i]) return false;
    }
    return true;
}

int main(int argc, const char * argv[]) {
    string start = "RXXLRXRXL", end = "XRLXXRRLX";
    cout << canTransform(start, end) << endl;
    return 0;
}
