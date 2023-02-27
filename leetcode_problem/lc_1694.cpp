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
 leetcode https://leetcode.cn/problems/reformat-phone-number/
 思路：这个题很直接哈，直接遍历一遍然后将数字存储下来
 技巧：需要一个变量cnt来标志什么时候添加 '-' 字符
 特别注意：最后几个字符的处理
 */

string reformatNumber(string number) {
    string ans;
    int cnt = 0;
    // 按3个数字一组存储，满足3个是后面加 -
    for(int i = 0; i < number.length(); ++i) {
        if (number[i] >= '0' && number[i] <= '9') {
            if (ans.length() > 0 && cnt == 0)
                ans.push_back('-');
            ans.push_back(number[i]);
            cnt = (cnt + 1) % 3;
        }
    }
    int len = ans.size();
    // 特别注意cnt==1时，说明最后是4个字符，需要拆分成2个2；cnt=0，2均不需要处理
    if (len > 3 && cnt == 1) swap(ans[len-2], ans[len-3]);
    return ans;
}

int main(int argc, const char * argv[]) {
    string s = "12-11122";
    cout << reformatNumber(s) << endl;
    return 0;
}
