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
 leetcode https://leetcode.cn/problems/minimum-add-to-make-parentheses-valid/
 思路：基本栈操作
 */

class Solution {
public:
    int minAddToMakeValid(string s) {
        stack<char> st;
        for(auto c : s) {
            if (st.empty() || c == '(') {
                st.push(c);
            } else {
                if (st.top() == '(') st.pop();
                else st.push(c);
            }
        }
        return st.size();
    }
};

int main(int argc, const char * argv[]) {
    Solution so;
    string s = "()))))))((((())))))";
    auto ans = so.minAddToMakeValid(s);
    cout << ans << endl;
    return 0;
}