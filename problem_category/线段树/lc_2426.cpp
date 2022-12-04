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

class SegmentTree {
public:
    using LL = long long;
    // tree的节点总数
    static const int N = 5e5;
    // 标记节点是否已被使用
    static const int INF = INT_MAX;
    struct Node {
        Node():l(INF),r(INF),val(0){}
        int l, r; //左右子树的索引号
        long long val;
    };
    Node tree[N];
    int k = 1; //记录目前动态开了多少个点，下一个点的索引号为k+1
    
    /*
     功能：向线段树中插入单点
     参数1：cur一般为1，表示根索引
     参数2，3：[l, r]表示该节点代表的范围
     参数4：待插入的值
     返回值：无
     */
    void insert(int cur, LL l, LL r, LL val) {
        tree[cur].val += 1;
        if (val == l && val == r) {
            return;
        }
        pushDown(cur);
        LL m = l + (r - l) / 2;
        if (val <= m) {
            insert(tree[cur].l, l, m, val);
        } else {
            insert(tree[cur].r, m + 1, r, val);
        }
    }
    
    void pushDown(int cur) {
        if (tree[cur].l == INF)
            tree[cur].l = ++k;
        if (tree[cur].r == INF)
            tree[cur].r = ++k;
    }
    
    /*
     功能：查询[i, j]范围内的元素数量
     参数1：cur一般为1，表示根索引
     参数2，3：[l, r]表示该节点代表的范围
     参数4，5：[i, j]待查询的范围
     返回值：long long
     */
    long long search(int cur, LL l, LL r, LL i, LL j) {
        if (i <= l && j >= r) return tree[cur].val;
        if (tree[cur].l == INF) return 0;
        int m = l + (r - l) / 2;
        if (j <= m) {
            return search(tree[cur].l, l, m, i, j);
        } else if (i > m) {
            return search(tree[cur].r, m + 1, r, i, j);
        } else {
            return search(tree[cur].l, l, m, i, m) +
                search(tree[cur].r, m + 1, r, m + 1, j);
        }
    }
};

class Solution {
    /*
        1.思维转化, 构造nums1-nums2的数组
        2.固定右端下标i,用线段树动态维护值域区间元素个数 [l, r]区间有多少个元素
    */
public:
    SegmentTree tree;
    long long numberOfPairs(vector<int>& nums1, vector<int>& nums2, int diff) {
        long long L = -2e4, R = 2e4;
        for(int i = 0; i < nums1.size(); ++i) {
            nums1[i] -= nums2[i];
        }
        long long  ans = 0;
        for(int i = 0; i < nums1.size(); ++i) {
            if (i > 0) {
                ans += tree.search(1, L, R, L, nums1[i] + diff);
            }
            tree.insert(1, L, R, nums1[i]);
        }
        return ans;
    }
};