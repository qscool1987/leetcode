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
本模版记录有关二分查找算法相关题目
哪些题目适合用二分？
1.一般的，题目要求最大化最小值，最小化最大值可以优先考虑
2.具有二段性的题目可以用二分查找，比如数组先单调增后单调减
3.借助set，map，lower_bound，upper_bound的二分算法
4.一般数据量为1e5量级，时间复杂度不能超过nlogn / nsqrt(n)，二分，dp，贪心或许是可能解

lc 2528. 最大化城市的最小供电站数目
*/
class Solution {
public:
    long long maxPower(vector<int>& s, int r, int k) {
        long long sum = 0;
        int n = s.size();
        vector<long long> pre(n+1);
        vector<long long> ps(n);
        for(int i = 1; i <= n; ++i) {
            pre[i] = s[i-1] + pre[i-1];
        }
        long long mv = 0;
        for(int i = 0; i < n; ++i) {
            int a = max(0, i-r), b = min(i+r, n-1);
            ps[i] = pre[b+1] - pre[a];
            mv = max(mv,  ps[i]);
        }
        int diff[200050] = {0}; // 差分优化
        long long i = 0, j = mv + k;
        long long ans = -1; 
        while(i <= j) { // 二分查找
            long long m = (i + j) / 2;
            long long cnt = 0;
            int index = 0;
            long long sum_d = 0;
            memset(diff, 0, sizeof(diff));
            while(index < n) {
                sum_d += diff[index]; //sum_d表示前面放置的电站在index处的叠加
                long long d = ps[index] + sum_d - m;
                if (d < 0) { // 需要在位置 index+r 处放置 d 个电站
                    cnt += -d;
                    sum_d += -d; // 更新sum_d, [index, index+2*r]
                    diff[index+2*r+1] -= -d; // 更新差分数组
                }
                ++index;
            }
            if (cnt > k) {
                j = m-1;
            } else {
                ans = m;
                i = m+1;
            }
        }
        return ans;
    }
};


