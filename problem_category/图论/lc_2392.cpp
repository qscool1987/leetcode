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

class Solution {
public:
    /*
        本题思路：
        通过拓扑排序确定row和col的编号次序
        凡是需要通过局部顺序来推导全局顺序的，一般都可以使用拓扑排序来解决
    */
    vector<int> topsort(vector<vector<int>>& mat, int k) {
        vector<vector<int>> grap(k);
        vector<int> in(k, 0);
        for(int i = 0; i < mat.size(); ++i) {
            ++in[mat[i][1]-1];
            grap[mat[i][0]-1].push_back(mat[i][1]-1);
        }
        queue<int> que;
        for(int i = 0; i < k; ++i) {
            if (in[i] == 0) que.push(i);
        }
        vector<int> ans;
        while(!que.empty()) {
            int cur = que.front();
            ans.push_back(cur);
            que.pop();
            for(int i = 0; i < grap[cur].size(); ++i) {
                --in[grap[cur][i]];
                if (in[grap[cur][i]] == 0) que.push(grap[cur][i]);
            }
        }
        return ans;
    }

    vector<vector<int>> buildMatrix(int k, vector<vector<int>>& rowConditions, vector<vector<int>>& colConditions) {
        vector<int> rows = topsort(rowConditions, k);
        vector<int> cols = topsort(colConditions, k);
        if (rows.size() < k || cols.size() < k) return {};
        vector<int> tb(k,0);
        for(int i = 0; i < k; ++i) {
            tb[cols[i]] = i;
        }
        vector<vector<int>> ans(k, vector<int>(k,0)); 
        for(int i = 0; i < k; ++i) {
            ans[i][tb[rows[i]]] = rows[i] + 1;
        }
        return ans;
    }
};