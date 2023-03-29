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
给你一个非空的字符串 s 和一个整数 k ，你要将这个字符串 s 中的字母进行重新排列，
使得重排后的字符串中相同字母的位置间隔距离 至少 为 k 。如果无法做到，请返回一个空字符串 ""。

输入: s = "aabbcc", k = 3
输出: "abcabc" 
解释: 相同的字母在新的字符串中间隔至少 3 个单位距离。
*/

class Solution {
public:
    /*
    思路：贪心的先排数量最大的字符，优先队列
    用队列控制相同字符之间的间隔
    */
    string rearrangeString(string s, int k) {
        if (k == 0) return s;
        if (k > 26) return "";
        priority_queue<pair<int, char>> pq; //默认是大顶堆
        unordered_map<char, int> mp;
        queue<pair<int, char>> q;
        string ret;
        for (char c : s)  ++mp[c];
        for (auto [c, i] : mp) pq.emplace(i, c); //先全部进优先队列，每次都是取堆顶元素加入ret
        while (!pq.empty()) {
            auto& [i, c] = pq.top();
            ret += c;
            q.emplace(i - 1, c);
            pq.pop();
            if (q.size() == k) { // 队列长度为 k 说明重复元素相距达到了 k， 可以出队
                if (q.front().first > 0) pq.emplace(q.front().first, q.front().second);
                q.pop();
            }
        }
        return ret.size() < s.size() ? "" : ret;
    }
};

/*
f[1] = 1
f[2] = 1
f[3] = 1
dfs(cur, k)
dp[i][k] 跳k步到达f[i]
dp[i][k] = dp[j][k+1] dp[m][k-1]
*/