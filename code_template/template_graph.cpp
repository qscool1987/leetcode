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
 功能：检查是否所有节点都访问过，是则返回true，否则返回false 并且返回当前距离最小的节点
 参数1：visited用于存储节点是否被访问过
 参数2：dis用于存储到达该节点的最短距离，其下标表示节点编号
 参数3：v为出参，返回当前dis列表中距离最小的节点的编号
 返回值：bool
 */
bool check_all_visited(vector<bool>& visited, vector<long long>& dis, int& v) {
    long long  mn = UPLIMIT;
    for (int i = 0; i < visited.size(); ++i) {
        if (!visited[i]) {
            if (mn > dis[i]) {
                v = i;
                mn = dis[i];
            }
        }
    }
    return mn == UPLIMIT;
}

/*
 功能：求出节点v到达其他所有节点的最短距离
 参数1：grid为n*n的矩阵，grid[i][j]表示由节点i到达节点j的距离
 参数2：grap为无向图，用临接矩阵表示，存储节点之间的联通状态
 参数3：visited用于存储节点是否被访问过
 参数4：dis用于存储到达该节点的最短距离，其下标表示节点编号
 参数5：指定的起始节点编号 范围为 [0, visited.size == grap.size]
 返回：void
 */
void shortest_path(vector<vector<int>>& grid, vector<vector<int>>& grap,
                   vector<bool>& visited, vector<long long>& dis, int v) {
    dis[v] = 0;
    while (true) {
        visited[v] = true;
        for (auto x : grap[v]) {
            if (dis[x] > dis[v] + grid[v][x]) {
                dis[x] = dis[v] + grid[v][x];
            }
        }
        if (check_all_visited(visited, dis, v)) break;
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


int main() {
    vector<vector<int>> roads = {{0,6,7},{0,1,2},{1,2,3},{1,3,3},{6,3,3},{3,5,1},{6,5,1},{2,5,1},{0,4,5},{4,6,2}};
    int n = 7;
    vector<long long> dis;
    vector<bool> visited;
    vector<vector<int>> grid;
    vector<vector<int>> grap(n); // 用于最短路径
    vector<vector<int>> grap2(n); // 用于拓扑排序
    grid.resize(n, vector<int>(n, 0));
    dis.resize(n, UPLIMIT);
    visited.resize(n, false);
    for(auto& v : roads) {
        grap[v[0]].push_back(v[1]);
        grap[v[1]].push_back(v[0]);
        grid[v[0]][v[1]] = v[2];
        grid[v[1]][v[0]] = v[2];
        grap2[v[0]].push_back(v[1]);
    }
    shortest_path(grid, grap, visited, dis, 0);
    for(int i = 0; i < dis.size(); ++i) {
        cout << i << ", " << dis[i] << endl;
    }
    auto ans = topology_sort(n, grap2);
    for(auto x : ans) {
        cout << x << " ";
    }
    cout << endl;
    return 0;
}
