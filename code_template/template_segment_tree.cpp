//
//  main.cpp
//  cppcode
//
//  Created by 默认 on 2022/9/6.
//

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
 简介：该线段树适用于动态查询某个范围内的元素个数
 实战题号：lc 6198. 满足不等式的数对数目
 1.线段树的根节点表示的范围为元素的值域范围，该范围由insert接口指定
 2.动态开点，初始化时开辟N个未用节点，insert的时候动态开点
 3.支持单点更新
 4.支持范围查询
 限制：
 1.线段树最多支持1e5个节点插入
 2.根节点表示范围最大为 [INT_MIN, INT_MAX)
 */
class SegmentTree {
public:
    // tree的节点总数
    static const int N = 5e5;
    
    // 标记节点是否已被使用
    static const int INF = INT_MAX;
    
    struct Node {
        Node():l(INF),r(INF),val(0){}
        int l, r;
        long long val;
    };
    Node tree[N];
    
    /*
     功能：向线段树中插入单点
     参数1：cur一般为1，表示根索引
     参数2，3：[l, r]表示该节点代表的范围
     参数4：待插入的值
     返回值：无
     */
    void insert(int cur, int l, int r, int val) {
        auto& nd = tree[cur];
        // nd.l == INF 动态开点
        if (nd.l == INF) {
            nd.l = l;
            nd.r = r;
        }
        nd.val += 1;
        if (val == l && val == r) {
            return;
        }
        int m = l + (r - l) / 2;
        if (val <= m) {
            insert(cur << 1, l, m, val);
        } else {
            insert(cur << 1 | 1, m + 1, r, val);
        }
    }
    
    /*
     功能：查询[i, j]范围内的元素数量
     参数1：cur一般为1，表示根索引
     参数2，3：[l, r]表示该节点代表的范围
     参数4，5：[i, j]待查询的范围
     返回值：long long
     */
    long long search(int cur, int l, int r, int i, int j) {
        auto& nd = tree[cur];
        if (nd.l == INF) return 0;
        if (i <= l && j >= r) return nd.val;
        int m = l + (r - l) / 2;
        if (j <= m) {
            return search(cur << 1, l, m, i, j);
        } else if (i > m) {
            return search(cur << 1 | 1, m + 1, r, i, j);
        } else {
            return search(cur << 1, l, m, i, m) +
                search(cur << 1 | 1, m + 1, r, m + 1, j);
        }
    }
};
