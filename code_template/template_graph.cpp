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
#include<limits.h> 
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
最短路径 Floyd 算法
邻接矩阵表示图
*/
void floyd(vector<vector<int>>& g, vector<vector<long long>>& cost) {
    int n = g.size();
    long long UP = 1e17;
    for(int k = 0; k < n; ++k) {
        for(int i = 0; i < n; ++i) {
            for(int j = 0; j < n; ++j) {
                if (cost[i][k] >= UP || cost[k][j] >= UP) continue;
                if (cost[i][k] + cost[k][j] < cost[i][j]) cost[i][j] = cost[i][k] + cost[k][j];
            }
        }
    }
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

/*
判断二分图判断,返回集合顶点个数
*/
typedef pair<long long, long long> P;
vector<int> color;
P dfs(vector<vector<int>>& g, int cur, int c) {
    P ans = {0, 0};
    color[cur] = c;
    if (c == 1) {
        ans.first++;
    } else {
        ans.second++;
    }
    for(auto x : g[cur]) {
        if (color[x] == -c) continue;
        if (color[x] == c) return {-1, -1};
        auto [b, w] = dfs(g, x, -c);
        if (b == -1) return {-1, -1};
        ans.first += b;
        ans.second += w;
    }
    return ans;
}
/*
4 2
3 1
5 2
3 2*/
int main() {
    

    return 0;
}
