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
    using LL = long long;
    // tree的节点总数
    static const int N = 3e6;
    
    // 标记节点是否已开
    static const int INF = INT_MAX;
    struct Node {
        Node():l(INF),r(INF),val(INF/2){}
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
        //节点范围代表的是值域范围，存储[l,r]之间插入的元素数量
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

    /*
     功能：区间更新
     参数1：cur一般为1，表示根索引
     参数2，3：[l, r]表示该节点代表的范围
     参数4,5：待插入区间的左右端点
     返回值：无
     */
    LL insert(int cur, LL l, LL r, LL i, LL j) {
        if (tree[cur].val == r-l+1) { //
            return tree[cur].val;
        }
        if (i <= l && j >= r) {
            tree[cur].val = r-l+1;
            return tree[cur].val;
        }
        pushDown(cur);
        LL m = l + (r - l) / 2;
        LL sum = 0;
        int rd = tree[cur].r;
        int ld = tree[cur].l;
        if (j <= m) {
            sum = insert(tree[cur].l, l, m, i, j) + tree[rd].val;
        } else if (i > m) {
            sum = insert(tree[cur].r, m + 1, r, i, j) + tree[ld].val;
        } else {
            sum = insert(tree[cur].l, l, m, i, m) +
                insert(tree[cur].r, m + 1, r, m+1, j);
        }
        return tree[cur].val = max(tree[cur].val, sum);
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
        LL m = l + (r - l) / 2;
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


class SegmentTree2 {
    /*
    该线断树动态分配节点数目
    */
public:
    struct SegNode {
        long long lo, hi;
        int add;
        SegNode* lchild, *rchild;
        SegNode(long long left, long long right): lo(left), hi(right), add(0), lchild(nullptr), rchild(nullptr) {}
    };
    SegNode *root;
    SegmentTree2(long long L, long long R) {
        root = new SegNode(L, R);
    }
    void insert(long long val) {
        insert(root, val);
    }

    void insert(SegNode* root, long long val) {
        root->add++;
        if (root->lo == root->hi) {
            return;
        }
        long long mid = (root->lo + root->hi) >> 1;
        if (val <= mid) {
            if (!root->lchild) {
                root->lchild = new SegNode(root->lo, mid);
            }
            insert(root->lchild, val);
        }
        else {
            if (!root->rchild) {
                root->rchild = new SegNode(mid + 1, root->hi);
            }
            insert(root->rchild, val);
        }
    }

    int search(long long left, long long right) {
        return search(root, left, right);
    }

    int search(SegNode* root, long long left, long long right) const {
        if (!root) {
            return 0;
        }
        if (left > root->hi || right < root->lo) {
            return 0;
        }
        if (left <= root->lo && root->hi <= right) {
            return root->add;
        }
        return search(root->lchild, left, right) + search(root->rchild, left, right);
    }
};
