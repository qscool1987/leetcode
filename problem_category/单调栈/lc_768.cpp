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
768. 最多能完成排序的块 II
给你一个整数数组 arr 。
将 arr 分割成若干 块 ，并将这些块分别进行排序。之后再连接起来，使得连接的结果和按升序排序后的原数组相同。
返回能将数组分成的最多块数？

输入：arr = [2,1,3,4,4]
输出：4
解释：
可以把它分成两块，例如 [2, 1], [3, 4, 4]。 
然而，分成 [2, 1], [3], [4], [4] 可以得到最多的块数。 
*/

class Solution {
public:
    int maxChunksToSorted(vector<int>& arr) {
        stack<int> st;
        for (auto &num : arr) {
            if (st.empty() || num >= st.top()) {
                st.emplace(num);
            } else { //如果比栈顶元素小，则将合入栈顶所属于的块中
                int mx = st.top(); //记录该块的最大值
                st.pop();
                while (!st.empty() && st.top() > num) {
                    st.pop();
                }
                st.emplace(mx); //将该块的最大值存入栈
            }
        }
        return st.size();
    }
};