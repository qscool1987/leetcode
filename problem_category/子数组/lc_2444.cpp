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

class Solution {
public:
    /*
        枚举子数组的右边下标r
        i0记录最后一个 < minK || > maxK的元素下标
        f 记录 minK的下标， b记录maxK的下标
        计算以nums[r] 为最后一个元素的子数组数量 
        情况1: [i0,...,f,...,b...r] 为 min(f,b) - i0
        情况2: [f,...,b,...,i0,...r] or [f,...,i0,...b...r] or [f..b..i0..r] 为0
        综合起来就是: max(0, min(f, b) - i0)
    */
    long long countSubarrays(vector<int>& nums, int minK, int maxK) {
        int f = -1, b = -1, i0 = -1, r = 0; 
        int n = nums.size();
        long long ans = 0;
        for(; r < n; ++r) {
            if (nums[r] == minK) f = r;
            if (nums[r] == maxK) b = r;
            if (nums[r] < minK || nums[r] > maxK) i0 = r;
            ans += max(0, min(f, b) - i0);
        }
        return ans;
    }
};