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
    本题的关键是思维转化
    将数组转化为只包含-1，0，1的数组（将<k的变成-1，=k的变为0， >k的变为1）
    则题目就变成了[l-index-r] 这个区间的和为0或者1 [-1,-1,0,0 1 1]
    于是可以用map 记录[index, n-1]之间的和，然后向前枚举l的位置，题目转为为
    sum(l) + sum(r) = 0/1
    */

    int countSubarrays(vector<int>& nums, int k) {
        int i = 0;
        int index = 0;
        for(; i < nums.size(); ++i) {
            if (nums[i] < k) {
                nums[i] = -1;
            } else if (nums[i] > k) {
                nums[i] = 1;
            } else {
                nums[i] = 0;
                index = i;
            }
        }
        unordered_map<int, int> mp;
        for(int j = index - 1; j >= 0; --j) {
            nums[j] += nums[j+1];
        }
        mp[0] = 1;
        for(int j = index + 1; j < nums.size(); ++j) {
            nums[j] += nums[j-1];
            ++mp[nums[j]];
        }
        int ans = 0;
        for(int j = index; j >= 0; --j) {
            int l = nums[j];
            if (mp.find(-l) != mp.end()) {
                ans += mp[-l];
            }
            if (mp.find(-l+1) != mp.end()) {
                ans += mp[-l+1];
            }
        }
        return ans;
    }
};