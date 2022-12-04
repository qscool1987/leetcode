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
        本题关键：双单调栈
        本体单个栈只能求出下一最大值，但是无法解决下下一个最大值
        一个栈first存储未找到更大值的下标，一个栈second存储找了一个更大只的下标
        则从second弹出的元素就找到了，从first弹出的元素代表找到了一个，然后压入second
        遍历完成后，first和second中没有弹出的元素就代表没有找到
        小技巧：直接初始化为-1，避免遍历完后将剩余元素出栈的操作
    */
    vector<int> secondGreaterElement(vector<int>& nums) {
        vector<int> ans(nums.size(), -1);
        vector<int> first, second; //first保存未找更大的值，second保持找到1个更大的值
        
        for (int i = 0; i < nums.size(); ++ i) {
            while (!second.empty() && nums[second.back()] < nums[i]) {
                ans[second.back()] = nums[i];
                second.pop_back(); //如果nums[i]比 second中的数大，则弹出
            }
            
            vector<int> tmp;
            while (!first.empty() && nums[first.back()] < nums[i]) {
                tmp.push_back(first.back());
                first.pop_back();
            }
            //保证second单调递减
            for (auto it = tmp.rbegin(); it != tmp.rend(); ++ it) {
                second.push_back(*it);
            }
            
            first.push_back(i);
        }
        
        return ans;
    }
};