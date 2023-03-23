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
本模版讨论树形dp问题
作者：灵茶山艾府
链接：https://leetcode.cn/problems/difference-between-maximum-and-minimum-price-sum/solutions/2062782/by-endlesscheng-5l70/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
lc 2538. 最大价值和与最小价值和的差值
*/

class Solution {
public:
    long long maxOutput(int n, vector<vector<int>> &edges, vector<int> &price) {
        vector<vector<int>> g(n);
        for (auto &e : edges) {
            int x = e[0], y = e[1];
            g[x].push_back(y);
            g[y].push_back(x); // 建树
        }

        long ans = 0;
        // 返回带叶子的最大路径和，不带叶子的最大路径和
        function<pair<long, long>(int, int)> dfs = [&](int x, int fa) -> pair<long, long> {
            long p = price[x], max_s1 = p, max_s2 = 0;
            for (int y : g[x])
                if (y != fa) {
                    auto[s1, s2] = dfs(y, x);
                    // 前面最大带叶子的路径和 + 当前不带叶子的路径和
                    // 前面最大不带叶子的路径和 + 当前带叶子的路径和
                    ans = max(ans, max(max_s1 + s2, max_s2 + s1));
                    max_s1 = max(max_s1, s1 + p);
                    max_s2 = max(max_s2, s2 + p); // 这里加上 p 是因为 x 必然不是叶子
                }
            return {max_s1, max_s2};
        };
        dfs(0, -1);
        return ans;
    }
};

/*
    lc 1245. 树的直径
    1.某个节点的两个最长子树的直径相加
    2.要么就向上返回最长的子树直径
*/
class Solution {
public:
    int ans = 0;
    int dfs(vector<vector<int>>& g, int x, int f) {
        int first = 0, second = 0; //记录子树中最长的两条直径
        for(auto y : g[x]) {
            if (f != y) {
                int t = 1 + dfs(g, y, x);
                if (first == 0) {
                    first = t;
                    continue;
                }
                if (t > first) {
                    second = first;
                    first = t;
                } else if (t <= first) {
                    second = max(t, second);
                }
            }
        }
        ans = max(ans, first + second); //更新结果
        return first;
    }
    int treeDiameter(vector<vector<int>>& edges) {
        int n = edges.size();
        vector<vector<int>> g(n+1);
        for(auto& v : edges) {
            g[v[0]].push_back(v[1]);
            g[v[1]].push_back(v[0]);
        }
        dfs(g, 0, -1);
        return ans;
    }
};

/*
lc 337. 打家劫舍 III

*/

class Solution {
public:
    int ans = 0;
    pair<int,int> dfs(TreeNode* root) {
        if (root == nullptr) return {0,0};
        int a = root->val, b = 0; // 返回 包含该节点的最大值和不包含该节点的最大值
        auto l = dfs(root->left);
        auto r = dfs(root->right);
        /*
        l.first 包含子树节点的最大值
        l.second 不包含的最大值
        */
        a += l.second + r.second; //包含该节点
        b = max(l.first, l.second) + max(r.first, r.second); //不包含该节点，则需要将左边最大和左右最大相加
        return {a, b};
    }
    int rob(TreeNode* root) {
        auto [a, b] = dfs(root);
        return max(a, b);
    }
};

/*
lc 2581. 统计可能的树根数目
*/
class Solution {
public:
    int sz = 0;
    int ans = 0;
    
    int rootCount(vector<vector<int>>& edges, vector<vector<int>>& guesses, int k) {
        int n = edges.size() + 1;
        vector<vector<int>> g(n);
        for(auto& v : edges) {
            g[v[0]].push_back(v[1]);
            g[v[1]].push_back(v[0]);
        }
        map<pair<int,int>, int> mp; //key类型为pair<int,int>, 简化运算
        for(auto& v : guesses) {
            mp[{v[0],v[1]}]++;
        }
        function<void(int,int)> f1 = [&](int cur, int f) {
            for(auto x : g[cur]) {
                if (x != f) {
                    if (mp.find({cur, x}) != mp.end()) sz += mp[{cur,x}]; //统计正向的数目
                    f1(x, cur);
                }
            }
        };
        f1(0,-1);
        function<void(int,int)> f2 = [&](int cur, int f) {
            if (sz >= k) ++ans;
            for(auto x : g[cur]) {
                if (x != f) {//已知当先节点下的所有正确数(包括正向和负向),传递给下一个节点，其实只考虑连接的一条边
                    int d = 0; //负向数量
                    if (mp.find({x, cur}) != mp.end()) d += mp[{x,cur}]; 
                    if (mp.find({cur, x}) != mp.end()) d -= mp[{cur, x}];
                    sz += d; //处理子节点之前先加上负向节点，
                    f2(x, cur);
                    sz -= d; //回溯，处理下一个节点
                }
            }
        };
        f2(0, -1);
        return ans;
    }
};

