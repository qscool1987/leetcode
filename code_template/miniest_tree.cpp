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

class UnionSet {
public:
    // 用于记录每个节点的父亲节点
    vector<int> parent;

    // 统计集合数量
    int count = 0;
    UnionSet(int k) {
        parent.resize(k);
        for(int i = 0; i < parent.size(); ++i) {
            parent[i] = i;
        }
    }

    // 查找指定节点的根节点
    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]); //路径压缩
        }
        return parent[x];
    }

    // 将x所属于的集合S1 与 y所属于的集合S2 合并
    void unionSet(int x, int y) {
        int px = find(x);
        int py = find(y);
        if (px == py) return;
        parent[py] = px;
        --count; // 合并集合，集合数量减1
    }

    bool isConnected(int x, int y) {
        return find(x) == find(y);
    }

    // 更新集合数量
    void addCount() {
        count++;
    }

    // 返回集合数量
    int getCount() {
        return count;
    }
};

/*
描述: 将图转化为最小生成树
参数1: n为定点个数
参数2: 每一个元素为[i, j, cost] 为连通定点i和顶点j所需要的代价
返回值: 返回最小生成树的代价
*/
int genMiniestTree(int n, vector<vector<int>>& edges) {
    UnionSet ut;
    sort(edges.begin(), edges.end(), [](const vector<int>& a, vector<int>& b) {
        return a[2] < b[2];
    });
    int ans = 0;
    for(auto& v : edges) {
        if (ut.find(v[0]) != ut.find(v[1])) {
            ut.unionSet(v[0], v[1]);
            ans += v[2];
        }
    }
    return ans;
}