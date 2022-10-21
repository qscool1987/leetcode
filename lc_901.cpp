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
    思路：用vector模拟单调递减栈，当尾部元素比price小的时候就弹出，直到数组为空
    或者尾部元素比price大为止
    注意：需要记录加入到数组中的元素的编号（编号从0开始）
*/

class StockSpanner {
public:
    vector<pair<int,int>> st; // 用来模拟单调减栈
    int index; // 记录下一个加入数组的元素的编号
    StockSpanner() {
        index = 0;
    }
    
    int next(int price) {
        while(!st.empty() && st.back().first <= price) { // 退出条件
            st.pop_back();
        }
        if (st.empty()) {
            st.push_back({price, index++});
            return index;
        } else {
            int ret = index - st.back().second;
            st.push_back({price, index++});
            return ret;
        }
    }
};

int main() {
    return 0;
}