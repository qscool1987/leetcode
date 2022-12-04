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

long long UPLIMIT = 1LL << 60;

/*
 功能：求出节点start到达其他所有节点的最短距离
 参数1：g.size() 为节点个数， g[i] 存储了与节点i相邻的节点编号和距离
 参数2：start为起始节点
 返回：vector<int> start 到其他节点的最短距离
 */
vector<int> dijkstra(vector<vector<pair<int, int>>> &g, int start) {
    vector<int> dist(g.size(), INT_MAX);
    dist[start] = 0;
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq; //小顶堆，保存到顶点的距离和顶点编号
    pq.emplace(0, start); //初始化 将起始节点入队
    while (!pq.empty()) {
        auto[d, x] = pq.top();
        pq.pop();
        if (d > dist[x]) continue;  //dist[x] 可能已经被更新过了
        for (auto[y, wt] : g[x]) {
            int new_d = dist[x] + wt;
            if (new_d < dist[y]) {
                dist[y] = new_d;
                pq.emplace(new_d, y);
            }
        }
    }
    return dist;
}

/*
 功能：拓扑排序
 参数1：n为节点数目
 参数2：grap为邻接矩阵表示的有向图
 返回：节点的拓扑关系
 */
vector<int> topology_sort(int n, vector<vector<int>>& grap) {
    vector<int> in(n, 0);
    for (auto& v : grap) {
        for (auto x : v) {
            ++in[x];
        }
    }
    queue<int> que;
    for (int i = 0; i < in.size(); ++i) {
        if (in[i] == 0) que.push(i);
    }
    vector<int> ans(n, 0);
    int k = 0;
    while (!que.empty()) {
        int cur = que.front();
        que.pop();
        ans[k++] = cur;
        for (auto x : grap[cur]) {
            if (--in[x] == 0) que.push(x);
        }
    }
    return ans;
}
