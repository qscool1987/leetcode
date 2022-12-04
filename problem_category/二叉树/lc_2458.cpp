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

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 };

class Solution {
public:
    /*
        本题关键:
        1.树的高度，只需要考虑所有叶子节点的高度
        2.删除节点，就相当于删除了一部分叶子节点，如果将叶子节点用数组存储，那么将删除一个连续区间的叶子节点
        比如叶子节点数组：[0,1,2,3,4,5,6,7] 
        如果删除某个节点，那么相当于连续区间[i,j]的叶子节点被删除了，题目转化为求
        [0,i-1] 和[j, n-1]区间中叶子节点的最大高度， 以及删除节点的父节点的高度，三者取最大值
        所以需要先将叶子节点的高度进行存储，将每一个节点和父节点进行存储，另外还需要存储每个节点作为根节点时包含的叶子简单区间
        删除时可以直接获取
    */
    unordered_map<int, TreeNode*> parent; //记录节点的父亲节点，便于后续查询使用
    vector<int> ans; // 记录结果
    unordered_map<int, vector<int>> mvp; //记录以每一个节点为根节点时，其最左边和最右边叶子节点编号
    int leaf_h[100001] = {0}; //下标表示叶子节点的编号，值为叶子节点的高度，叶子节点编码顺序为中序编列后的顺序
    int harr[100001] = {0}; //记录每一个节点的高度
    int leafnum = 0; //记录叶子节点数量
    
    void dfs(TreeNode* root, int h) {
        harr[root->val] = h;
        mvp[root->val].push_back(leafnum); 
        if (root->left != nullptr) {
            parent[root->left->val] = root;
            dfs(root->left, h+1);
        }
        if (root->right != nullptr) {
            parent[root->right->val] = root;
            dfs(root->right, h+1);
        }
        if (root->left == nullptr && root->right == nullptr) {
            leaf_h[leafnum] = h; //记录叶子节点的高度
            ++leafnum;
        }
        mvp[root->val].push_back(leafnum-1); //最右边的叶子的编号一定要-1
    }
  
    vector<int> treeQueries(TreeNode* root, vector<int>& queries) {
        dfs(root, 0);
        //预处理左边最大和右边最大，O(1)获取左边和右边最大
        vector<int> lm(leafnum), rm(leafnum);
        int mv = 0;
        for(int i = 1; i < leafnum; ++i) {
            mv = max(leaf_h[i-1], mv);
            lm[i] = mv;
        }
        mv = 0;
        for(int i = leafnum-2; i >= 0; --i) {
            mv = max(leaf_h[i+1], mv);
            rm[i] = mv;
        }
        for(int i = 0; i < queries.size(); ++i) {
            int left = mvp[queries[i]][0];
            int right = mvp[queries[i]][1];
            auto p = parent[queries[i]];
            int h = harr[p->val]; // 被删除的节点，需要考虑其父节点的高度
            int t = max(lm[left], rm[right]); //O(1)获取左边和右边最大值
            h =max(t, h);
            ans.push_back(h);
        }
        return ans;
    }
};