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
    leetcode https://leetcode.cn/problems/three-equal-parts/
    思路：该题突破点
    1.每一部分包含的1一定要一样，并且每一部分第一个1到最后一个1之间的形式一样 如10101，
    则每一部分都必须是10101
    2.每一部分最后一个1后面的0的数量必须一样，这个可以从后往前计算，优先确定下来
*/
class Solution {
public:
    /*
        判断[sa, ea] 与 [sb, eb]之间的数字是否完全一样
    */
    bool checkEqual(vector<int>& arr, int sa, int ea, int sb, int eb) {
        // cout << sa << " " << ea << " " << sb << " " << eb << endl;
        if (ea - sa != eb - sb) return false;
        for(; sa <= ea && sb <= eb; ++sa, ++sb) {
            if (arr[sa] != arr[sb]) return false;
        }
        return true;
    }
    vector<int> threeEqualParts(vector<int>& arr) {
        vector<int> ones;
        // 存储数字1的下标
        for(int i = 0; i < arr.size(); ++i) {
            if (arr[i] == 1) ones.push_back(i);
        }
        // 判断是否为3的倍数
        if (ones.size() % 3 != 0) return {-1,-1};
        int n = arr.size();

        // 判断是否为全0的特殊情况
        if (ones.size() == 0) return {0, n-1};
        int cnt = ones.size() / 3;

        int j = n-1;
        int zeros = 0; //先计算后缀0的个数，由后往前
        while(j >= 0 && arr[j] == 0) {
            ++zeros;
            --j;
        }
        vector<int> ans;
        int sz = ones.size();
        int i = sz - cnt;
        // [s_i, e_i] 存储上一部分数字的起始和终止位置
        int s_i = ones[i];
        int e_i = n - 1;
        for(; i >= 0; i -= cnt) {
            if (i == 0) break;
            int gap = ones[i] - ones[i-1] - 1;
            // 两个1之间0的个数是否足够添加后缀0
            if (gap < zeros) return {-1, -1};
            int t = ones[i-1] + zeros;
            // 判断两部分数子是否完全一样
            if (!checkEqual(arr, ones[i-cnt], t, s_i, e_i)) return {-1, -1};
            s_i = ones[i-cnt];
            e_i = t;
            ans.push_back(t);
        }
        swap(ans[0], ans[1]);
        ++ans[1]; // 特别的，按题目意思处理一下
        return ans;
    }
};