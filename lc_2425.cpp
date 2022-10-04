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
 leetcode https://leetcode.cn/problems/bitwise-xor-of-all-pairings/
 思路：
 nums3 = [nums1[0] ^ nums2[0], nums1[0] ^ nums2[1], ..., nums1[0] ^ nums2[m-1]
        nums1[1] ^ nums2[0], nums1[1] ^ nums2[1], ..., nums1[1] ^ nums2[m-1],
        nums1[2] ^ nums2[0], nums1[2] ^ nums2[1], ..., nums1[2] ^ nums2[m-1],
        ...
        nums1[n-1] ^ nums2[0], nums1[n-1] ^ nums2[1], ..., nums1[n-1] ^ nums2[m-1]]
        一共n * m 个元素
 nums3的元素异或和 = (nums1[0] ^ nums1[0] ^ ... ^ nums1[0]) ^ (nums2[0] ^ nums2[1] ^ ... ^ nums2[m-1]) ^
                (nums1[1] ^ nums1[1] ^ ... ^ nums1[1]) ^ (nums2[0] ^ nums2[1] ^ ... ^ nums2[m-1]) ^
                ...
                (nums1[n-1] ^ nums1[n-1] ^ ... ^ nums1[n-1]) ^ (nums2[0] ^ nums2[1] ^ ... ^ nums2[m-1])
                = (nums1[0] ^ nums1[0] ^ ... ^ nums1[0]) ^ (nums2[0] ^ nums2[0] ^ ... ^ nums2[0]) ^
                (nums1[1] ^ nums1[1] ^ ... ^ nums1[1]) ^ (nums2[1] ^ nums2[1] ^ ... ^ nums2[1]) ^
                ...
                (nums1[n-1] ^ nums1[n-1] ^ ... ^ nums1[n-1]) ^ (nums2[m-1] ^ nums2[m-1] ^ ... ^ nums2[m-1])
 已知 nums1[i] ^ nums1[i] = 0
 nums3的元素异或和只与 nums1和nums2的元素个数有关
 */

class Solution {
public:
    int xorAllNums(vector<int>& nums1, vector<int>& nums2) {
        int ans = 0;
        if (nums1.size() % 2) for(auto x : nums2) ans ^= x;
        if (nums2.size() % 2) for(auto x : nums1) ans ^= x;
        return ans;
    }
};

int main(int argc, const char * argv[]) {
    vector<int> nums1 = {2, 1, 3};
    vector<int> nums2 = {10, 2, 5, 0};
    Solution so;
    cout << so.xorAllNums(nums1, nums2) << endl;
    return 0;
}
