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
    leetcode https://leetcode.cn/problems/advantage-shuffle/
    思路：对nums1和nums2进行排序
    技巧：对nums2的索引数组进行排序，排序后的索引数组就是nums2按升序排序后的索引数组
    比较nums1[i] 和 nums2[idx[l]] 就是在按循序比较两个有序数组的元素大小
    如果nums1[i] <= nums2[idx2[l]] 则将 nums2[idx2[r]] = nums1[i] 依次倒序覆盖nums2中的最大值
    注意：代码技巧较高，建议用示例单步调试看看转化
*/

class Solution {
public:
    vector<int> advantageCount(vector<int>& nums1, vector<int>& nums2) {
        int n = nums1.size();
        vector<int> idx2(n, 0);
        // 排序索引数组，索引数组排序后的状态就是nums2排序完后的索引状态
        for (int i = 0; i < n; ++i) {
            idx2[i] = i;
        }
        sort(idx2.begin(), idx2.end(), [&](int i, int j) {
            return nums2[i] < nums2[j];
        });
        sort(nums1.begin(), nums1.end());
        int l = 0, r = n-1;
        // 依次遍历比较
        for (int i = 0; i < n; ++i) {
            if (nums1[i] <= nums2[idx2[l]]) {
                nums2[idx2[r--]] = nums1[i]; // 不满足要求则覆盖最大值
            } else {
                nums2[idx2[l++]] = nums1[i];
            }
        }
        return nums2;
    }
};