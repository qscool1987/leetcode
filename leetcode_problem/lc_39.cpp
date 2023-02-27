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
 leetcode https://leetcode.cn/problems/combination-sum/
 思路：dfs对于求所有组合情况非常适用
 */

class Solution {
public:
    vector<vector<int>> ans;

    /*
    功能：通过递归将所有满足要求的组合存储到 ans中
    退出条件：
        1.sum = target 存储组合
        2.cur == candidates.size()  说明已经访问到末尾
        3.sum > target 剪纸，直接退出
    参数1：输入数组，从其中选择和为target的组合
    参数2：vec用于存储选择的数字
    参数3：当前从cur这个下标还是选择数据
    参数4：sum 是参数2中的元素之后，优化效率
    参数5：target 目标值
    返回值：无
    */
    void dfs(vector<int>& candidates, vector<int> &vec, int cur, int sum,int target) {
        if(sum == target) {
            ans.push_back(vec);
            return;
        }
        // 剪枝
        if(sum > target || cur == candidates.size()) return; 
        // 选择从cur开始，允许重复
        for(int i = cur; i<candidates.size(); ++i) {
            vec.push_back(candidates[i]);
            dfs(candidates, vec, i, sum + candidates[i], target);
            vec.pop_back(); //回溯
        }
    }

    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        vector<int> tmp;
        dfs(candidates,tmp,0,0,target);
        return ans;
    }
};

int main(int argc, const char * argv[]) {
    vector<int> nums = {2, 3, 6, 7};
    int target = 7;
    Solution so;
    auto ans = so.combinationSum(nums, target);
    for(auto& v : ans) {
        for(auto x : v) {
            cout << x << " ";
        }
        cout << endl;
    }
    return 0;
}