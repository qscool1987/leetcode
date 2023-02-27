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
    并查集
    实战题号 leetcode 305 
    https://leetcode.cn/problems/number-of-islands-ii/
    介绍：并查集广泛用于集合合并相关问题
    如何将问题抽象转化为集合合并问题是难点
    一般的，如果问题由一个大集合能划分为几个小集合，且小集合的问题解决能得到大集合的问题解决
    则适合用并查集
*/

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
