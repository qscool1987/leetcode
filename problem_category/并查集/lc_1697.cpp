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
    /*
    解题思路：按距离从小到大对edges排序
    1.固定queries[i]，将edges中边长度小于dis的edge取出来，然后将节点merge在一起
    2.判断querys[i]的两个节点是否连通
    */
public:
    vector<int> parent;

    int find(int x) {
        if (x != parent[x]) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    void merge(int x, int y) {
        int px = find(x), py = find(y);
        int px = find(x), py = find(y);
        parent[py] = px;
    }

    bool connect(int x, int y) {
        return find(x) == find(y);
    }

    vector<bool> distanceLimitedPathsExist(int n, vector<vector<int>>& edgeList, vector<vector<int>>& queries) {
        sort(edgeList.begin(), edgeList.end(), [](const vector<int>& a, const vector<int>& b) {
            return a[2] < b[2];
        });
        parent.resize(n);
        vector<int> index(queries.size()); //索引数组，对queries按v[2]进行排序
        vector<bool> ans(queries.size(), false);
        iota(index.begin(), index.end(), 0);
        sort(index.begin(), index.end(), [&](int i, int j) {
            return queries[i][2] < queries[j][2];
        });
        iota(parent.begin(), parent.end(), 0);
        int k = 0; //记录当前访问到edgeList的下标
        for(int i = 0; i < queries.size(); ++i) { //遍历queries，固定queries[i]，将边长度小于 dis的edge取出来，然后将节点merge在一起
            auto& v = queries[index[i]];
            int f = v[0], t = v[1], dis = v[2];
            while(k < edgeList.size()) {
                auto& edge = edgeList[k];
                if (edge[2] < dis) {
                    merge(edge[0], edge[1]); //将当前比dis小的边的节点merge
                } else break;
                ++k;
            }
            if (connect(f, t)) ans[index[i]] = true; //判断queries[i] 的两个节点是否连通，连通则说明存在
        }
        return ans;
    }
};